"""Apex Hybrid ISMCTS search agent powered by Neural Value Network leaf evaluations and Tactical Blunder Shielding."""

from __future__ import annotations
import math
import time
import random
import numpy as np
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
class HybridMCTSNode:
    parent: Optional[HybridMCTSNode]
    action: Optional[Action]
    player_id: int
    visits: int = 0
    total_rewards: dict[int, float] = field(default_factory=dict)
    children: list[HybridMCTSNode] = field(default_factory=list)

    def ucb1(self, player_id: int, c_param: float = 1.414) -> float:
        if self.visits == 0:
            return float("inf")
        avg_reward = self.total_rewards.get(player_id, 0.0) / self.visits
        parent_visits = self.parent.visits if self.parent else self.visits
        exploration = c_param * math.sqrt(math.log(max(1, parent_visits)) / self.visits)
        return avg_reward + exploration


class HybridSearchAgent(BaseAgent):
    """World-class Apex Search Agent combining Information Set MCTS, Neural Value evaluations, and Tactical Blunder Shielding."""

    def __init__(
        self,
        name: str = "Hybrid_ISMCTS_RL",
        player_id: int = 0,
        network: Optional[NeuralValueNetwork] = None,
        iterations: int = 35,
        rng: Optional[random.Random] = None
    ):
        super().__init__(name, player_id)
        self.iterations = iterations
        self.network = network or NeuralValueNetwork(seed=player_id + 500)
        self.feature_agent = DeepRLAgent(name="extractor", player_id=player_id, network=self.network)
        self.rng = rng or random.Random()
        self.determinizer = WorldDeterminizer(self.rng)
        self.belief = BayesianBeliefModel(player_id, 4)

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        # Fast path for deterministic choices
        if len(legal_actions) == 1:
            trace = self._create_trace(view, legal_actions[0], [], 0.1)
            return legal_actions[0], trace

        # Tactical Blunder Shield: In DISCARD phase, prune suicidal discards (cards that directly attach to table)
        candidate_actions = list(legal_actions)
        if view.phase == TurnPhase.DISCARD and len(candidate_actions) > 1 and view.table.melds:
            safe_actions = []
            for act in candidate_actions:
                if act.card is not None:
                    # Check if card attaches to any table meld
                    attaches = any(view.table.can_attach_card(act.card, tm.meld_id) is not None for tm in view.table.melds)
                    if not attaches:
                        safe_actions.append(act)
            if safe_actions:
                candidate_actions = safe_actions

        if self.belief.num_players != view.num_players:
            self.belief = BayesianBeliefModel(self.player_id, view.num_players)
        self.belief.update_from_view(view)

        root = HybridMCTSNode(parent=None, action=None, player_id=view.current_player)
        for act in candidate_actions:
            root.children.append(HybridMCTSNode(parent=root, action=act, player_id=view.current_player))

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
            curr: Optional[HybridMCTSNode] = node
            while curr is not None:
                curr.visits += 1
                for p, r in rewards.items():
                    curr.total_rewards[p] = curr.total_rewards.get(p, 0.0) + r
                curr = curr.parent

        best_child = max(root.children, key=lambda c: c.visits)
        best_action = best_child.action or candidate_actions[0]

        evaluations: list[ActionEvaluation] = []
        total_visits = sum(c.visits for c in root.children) or 1
        for c in root.children:
            if c.action is not None:
                q_val = (c.total_rewards.get(self.player_id, 0.0) / c.visits) if c.visits > 0 else 0.0
                evaluations.append(ActionEvaluation(
                    action_str=c.action.to_str(),
                    q_value=round(q_val, 2),
                    probability=c.visits / total_visits,
                    visit_count=c.visits
                ))

        latency = (time.perf_counter() - t0) * 1000.0
        belief_summary = self.belief.get_summary()
        trace = self._create_trace(view, best_action, evaluations, latency, belief_summary)
        return best_action, trace
