"""Information Set Monte Carlo Tree Search (ISMCTS) agent."""

from __future__ import annotations
import math
import time
import random
from dataclasses import dataclass, field
from typing import Sequence, Optional
from .base import BaseAgent
from ..engine.state import PlayerView, GameState, TurnPhase
from ..engine.actions import Action, ActionType
from ..opponent.belief import BayesianBeliefModel
from ..opponent.sampler import WorldDeterminizer
from ..persistence.trace import DecisionTrace, ActionEvaluation


@dataclass
class ISMCTSNode:
    """Node in the Information Set search tree."""
    parent: Optional[ISMCTSNode]
    action: Optional[Action]
    player_id: int
    visits: int = 0
    total_rewards: dict[int, float] = field(default_factory=dict)
    children: list[ISMCTSNode] = field(default_factory=list)

    def ucb1(self, player_id: int, c_param: float = 1.414) -> float:
        if self.visits == 0:
            return float("inf")
        avg_reward = self.total_rewards.get(player_id, 0.0) / self.visits
        parent_visits = self.parent.visits if self.parent else self.visits
        exploration = c_param * math.sqrt(math.log(max(1, parent_visits)) / self.visits)
        return avg_reward + exploration


class ISMCTSAgent(BaseAgent):
    """Multi-player Information Set Monte Carlo Tree Search (ISMCTS) agent."""

    def __init__(
        self,
        name: str = "ISMCTSAgent",
        player_id: int = 0,
        iterations: int = 40,
        rollout_depth: int = 8,
        rng: Optional[random.Random] = None
    ):
        super().__init__(name, player_id)
        self.iterations = iterations
        self.rollout_depth = rollout_depth
        self.rng = rng or random.Random()
        self.determinizer = WorldDeterminizer(self.rng)
        self.belief = BayesianBeliefModel(player_id, 4)

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        if len(legal_actions) == 1:
            trace = self._create_trace(view, legal_actions[0], [], 0.1)
            return legal_actions[0], trace

        if self.belief.num_players != view.num_players:
            self.belief = BayesianBeliefModel(self.player_id, view.num_players)
        self.belief.update_from_view(view)

        root = ISMCTSNode(parent=None, action=None, player_id=view.current_player)

        # Populate root children with legal actions
        for act in legal_actions:
            child = ISMCTSNode(parent=root, action=act, player_id=view.current_player)
            root.children.append(child)

        # MCTS Iterations
        for _ in range(self.iterations):
            # 1. Determinize
            world = self.determinizer.sample_world(view, self.belief)

            # 2. Select / Expand
            node = root
            sim_state = world.clone()

            while node.children and not sim_state.is_round_over:
                # Find children that are legal in this determinization
                det_legal = sim_state.get_legal_actions()
                det_legal_strs = set(a.to_str() for a in det_legal)
                valid_children = [c for c in node.children if c.action and c.action.to_str() in det_legal_strs]

                if not valid_children:
                    break

                # Select best using UCB1
                node = max(valid_children, key=lambda c: c.ucb1(sim_state.current_player))
                if node.action is not None:
                    sim_state.apply_action(node.action)

            # 3. Rollout / Simulation
            rewards = self._simulate_rollout(sim_state)

            # 4. Backpropagation
            curr: Optional[ISMCTSNode] = node
            while curr is not None:
                curr.visits += 1
                for p, r in rewards.items():
                    curr.total_rewards[p] = curr.total_rewards.get(p, 0.0) + r
                curr = curr.parent

        # Select best root child by visit count
        evaluations: list[ActionEvaluation] = []
        best_child = max(root.children, key=lambda c: c.visits)
        best_action = best_child.action or legal_actions[0]

        total_root_visits = sum(c.visits for c in root.children) or 1
        for c in root.children:
            if c.action is not None:
                q_val = (c.total_rewards.get(self.player_id, 0.0) / c.visits) if c.visits > 0 else 0.0
                prob = c.visits / total_root_visits
                evaluations.append(ActionEvaluation(
                    action_str=c.action.to_str(),
                    q_value=q_val,
                    probability=prob,
                    visit_count=c.visits
                ))

        latency = (time.perf_counter() - t0) * 1000.0
        belief_summary = self.belief.get_summary()
        trace = self._create_trace(view, best_action, evaluations, latency, belief_summary)
        return best_action, trace

    def _simulate_rollout(self, state: GameState) -> dict[int, float]:
        """Fast heuristic rollout for a limited number of plies."""
        steps = 0
        while not state.is_round_over and steps < self.rollout_depth:
            legal = state.get_legal_actions()
            if not legal:
                break
            # Heuristic / random move
            act = self.rng.choice(legal)
            state.apply_action(act)
            steps += 1

        rewards: dict[int, float] = {}
        if state.is_round_over and state.round_result is not None:
            for p, score in state.round_result.round_scores.items():
                rewards[p] = -float(score)  # Lower score is higher reward
        else:
            # Intermediate state evaluation
            for p in range(state.num_players):
                penalties = sum(c.hand_penalty_value for c in state.hands[p])
                score = -float(penalties)
                if state.is_opened[p]:
                    score += 100.0
                else:
                    score -= 100.0
                rewards[p] = score

        return rewards
