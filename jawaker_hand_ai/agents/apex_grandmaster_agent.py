"""Apex Grandmaster Agent combining Deep Neural Valuation, Adaptive ISMCTS, Bayesian Card Tracking, and Tactical Shielding."""

from __future__ import annotations
import math
import time
import random
import numpy as np
from pathlib import Path
from dataclasses import dataclass, field
from typing import Sequence, Optional
from .base import BaseAgent
from .deep_rl_agent import DeepRLAgent
from ..engine.state import PlayerView, GameState, TurnPhase
from ..engine.actions import Action, ActionType
from ..opponent.belief import BayesianBeliefModel
from ..opponent.sampler import WorldDeterminizer
from ..learning.network import NeuralValueNetwork
from ..persistence.trace import DecisionTrace, ActionEvaluation


@dataclass
class ApexMCTSNode:
    parent: Optional[ApexMCTSNode]
    action: Optional[Action]
    player_id: int
    visits: int = 0
    total_rewards: dict[int, float] = field(default_factory=dict)
    children: list[ApexMCTSNode] = field(default_factory=list)

    def ucb1(self, player_id: int, c_param: float = 1.414) -> float:
        if self.visits == 0:
            return float("inf")
        avg_reward = self.total_rewards.get(player_id, 0.0) / self.visits
        parent_visits = self.parent.visits if self.parent else self.visits
        exploration = c_param * math.sqrt(math.log(max(1, parent_visits)) / self.visits)
        return avg_reward + exploration


class ApexGrandmasterAgent(BaseAgent):
    """The Superhuman Jawaker Hand AI Agent: Neural Value Network + Deep ISMCTS + Bayesian Card Counting + Tactical Defense Matrix."""

    def __init__(
        self,
        name: str = "AI Grandmaster",
        player_id: int = 0,
        network: Optional[NeuralValueNetwork] = None,
        iterations: int = 60,
        rng: Optional[random.Random] = None
    ):
        super().__init__(name, player_id)
        self.iterations = iterations
        self.rng = rng or random.Random()

        # Load apex model if available
        if network is None:
            network = NeuralValueNetwork(seed=player_id + 777)
            for path in [Path("models/gen_apex.json"), Path("models/jawaker_champion_v1.json"), Path("models/gen_10k.json")]:
                if path.exists():
                    try:
                        network.load(path)
                        break
                    except Exception:
                        pass

        self.network = network
        self.feature_agent = DeepRLAgent(name="extractor", player_id=player_id, network=self.network)
        self.determinizer = WorldDeterminizer(self.rng)
        self.belief = BayesianBeliefModel(player_id, 4)

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        # 1. Deterministic single choice fast-exit
        if len(legal_actions) == 1:
            trace = self._create_trace(view, legal_actions[0], [ActionEvaluation(legal_actions[0].to_str(), 100.0)], 0.1)
            return legal_actions[0], trace

        # Update Bayesian Belief Model
        if self.belief.num_players != view.num_players:
            self.belief = BayesianBeliefModel(self.player_id, view.num_players)
        self.belief.update_from_view(view)

        # 2. Priority Rule: Snatch and liberate Jokers immediately
        joker_swaps = [a for a in legal_actions if a.action_type == ActionType.SWAP_JOKER]
        if joker_swaps:
            chosen = joker_swaps[0]
            trace = self._create_trace(view, chosen, [ActionEvaluation(chosen.to_str(), 100.0)], 0.2)
            return chosen, trace

        # 3. Tactical Discard Safety Filtering
        candidate_actions = list(legal_actions)
        if view.phase == TurnPhase.DISCARD and len(candidate_actions) > 1 and view.table.melds:
            safe_actions = []
            for act in candidate_actions:
                if act.card is not None:
                    attaches = any(view.table.can_attach_card(act.card, tm.meld_id) is not None for tm in view.table.melds)
                    if not attaches:
                        safe_actions.append(act)
            if safe_actions:
                candidate_actions = safe_actions

        # 4. Expert Heuristic Action Valuation
        heuristic_scores: dict[str, float] = {}
        for act in candidate_actions:
            heuristic_scores[act.to_str()] = self._evaluate_action_expert(view, act)

        # 5. Deep Adaptive ISMCTS with Neural Leaf Valuation
        root = ApexMCTSNode(parent=None, action=None, player_id=view.current_player)
        for act in candidate_actions:
            node = ApexMCTSNode(parent=root, action=act, player_id=view.current_player)
            # Seed with prior heuristic value
            node.total_rewards[self.player_id] = heuristic_scores.get(act.to_str(), 0.0) * 0.1
            node.visits = 1
            root.children.append(node)

        for _ in range(self.iterations):
            world = self.determinizer.sample_world(view, self.belief)
            node = root
            sim_state = world.clone()

            # Selection
            while node.children and not sim_state.is_round_over:
                det_legal = sim_state.get_legal_actions()
                det_legal_strs = set(a.to_str() for a in det_legal)
                valid_children = [c for c in node.children if c.action and c.action.to_str() in det_legal_strs]

                if not valid_children:
                    break

                node = max(valid_children, key=lambda c: c.ucb1(sim_state.current_player))
                if node.action is not None:
                    sim_state.apply_action(node.action)

            # Neural Value Leaf Evaluation
            rewards: dict[int, float] = {}
            if sim_state.is_round_over and sim_state.round_result is not None:
                for p, score in sim_state.round_result.round_scores.items():
                    rewards[p] = -float(score)
            else:
                for p in range(sim_state.num_players):
                    p_view = sim_state.get_player_view(p)
                    feat = self.feature_agent.extract_features(p_view, Action.pass_meld())
                    pred_score = self.network.predict(feat)
                    rewards[p] = -pred_score

            # Backpropagation
            curr: Optional[ApexMCTSNode] = node
            while curr is not None:
                curr.visits += 1
                for p, r in rewards.items():
                    curr.total_rewards[p] = curr.total_rewards.get(p, 0.0) + r
                curr = curr.parent

        if not root.children:
            chosen = candidate_actions[0] if candidate_actions else legal_actions[0]
            trace = self._create_trace(view, chosen, [], (time.perf_counter() - t0) * 1000.0)
            return chosen, trace

        # Combine MCTS visit quality with expert heuristics
        def composite_score(child: ApexMCTSNode) -> float:
            act_s = child.action.to_str() if child.action else ""
            h_score = heuristic_scores.get(act_s, 0.0)
            mcts_q = (child.total_rewards.get(self.player_id, 0.0) / max(1, child.visits))
            return (mcts_q * 0.6) + (h_score * 0.4)

        best_child = max(root.children, key=composite_score)
        best_action = best_child.action or candidate_actions[0]

        evaluations: list[ActionEvaluation] = []
        total_visits = sum(c.visits for c in root.children) or 1
        for c in root.children:
            if c.action is not None:
                c_score = composite_score(c)
                evaluations.append(ActionEvaluation(
                    action_str=c.action.to_str(),
                    q_value=round(c_score, 2),
                    probability=c.visits / total_visits,
                    visit_count=c.visits
                ))

        latency = (time.perf_counter() - t0) * 1000.0
        belief_summary = self.belief.get_summary()

        # Compute exact real neural network activations for this state
        feat = self.feature_agent.extract_features(view, best_action)
        y_pred, h2, h1, _ = self.network.forward(feat)
        neural_telemetry = {
            "inputs": [round(float(v), 3) for v in feat],
            "h1": [round(float(v), 3) for v in h1],
            "h2": [round(float(v), 3) for v in h2],
            "output": round(float(y_pred), 2)
        }

        trace = self._create_trace(view, best_action, evaluations, latency, belief_summary, neural_telemetry)
        return best_action, trace

    def _evaluate_action_expert(self, view: PlayerView, action: Action) -> float:
        """Grandmaster heuristic valuation assessing hand combos, safety, deadwood, and opponents."""
        if action.action_type == ActionType.DRAW_DISCARD:
            return 160.0

        elif action.action_type == ActionType.DRAW_STOCK:
            return 60.0

        elif action.action_type == ActionType.SWAP_JOKER:
            return 500.0

        elif action.action_type == ActionType.ATTACH_CARD:
            pts = action.card.hand_penalty_value if action.card else 10
            return 350.0 + (pts * 3.0)

        elif action.action_type == ActionType.LAY_MELD:
            pts = sum(m.points for m in action.melds) if action.melds else 0
            return 260.0 + pts

        elif action.action_type == ActionType.INITIAL_MELD:
            pts = sum(m.points for m in action.melds) if action.melds else 0
            any_opp_opened = any(view.player_is_opened[opp] for opp in range(view.num_players) if opp != self.player_id)
            opp_min_cards = min(view.player_hand_counts[opp] for opp in range(view.num_players) if opp != self.player_id)
            total_melded = len(view.best_meld_partition.used_card_ids)

            # Hold for Hand Finish if safe and high combo count
            if not any_opp_opened and opp_min_cards > 7 and total_melded >= 13:
                return -50.0
            return 600.0 + pts

        elif action.action_type == ActionType.PASS_MELD:
            return 0.0

        elif action.action_type == ActionType.DISCARD:
            card = action.card
            if card is None:
                return 0.0

            best_part = view.best_meld_partition
            is_melded = card.id in best_part.used_card_ids

            # Compute card synergy with remaining hand
            synergy = 0.0
            hand_without = [c for c in view.hand if c.id != card.id]
            for c in hand_without:
                if c.rank == card.rank and c.suit != card.suit:
                    synergy += 25.0  # Pair / Set potential
                elif c.suit == card.suit and abs(c.rank.value - card.rank.value) == 1:
                    synergy += 30.0  # Suited connector (run)
                elif c.suit == card.suit and abs(c.rank.value - card.rank.value) == 2:
                    synergy += 15.0  # Inside straight gap

            # Check if card is dangerous to opponents
            danger = 0.0
            for tm in view.table.melds:
                if view.table.can_attach_card(card, tm.meld_id) is not None:
                    danger += 200.0

            # Check dead cards: if other copies are already seen, it's safer
            seen_copies = sum(1 for c in view.discard_pile if c.rank == card.rank and c.suit == card.suit)
            for tm in view.table.melds:
                seen_copies += sum(1 for c in tm.meld.cards if c.rank == card.rank and c.suit == card.suit)
            dead_bonus = 20.0 * seen_copies

            # Penalty weight: dump high-rank deadwood to avoid 10-pt penalties
            penalty_val = float(card.hand_penalty_value)

            base = 120.0 if not is_melded else -120.0
            score = base + (penalty_val * 2.0) + dead_bonus - (synergy * 1.5) - danger
            return score

        return 0.0
