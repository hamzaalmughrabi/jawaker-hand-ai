"""Reinforcement learning TD(λ) linear value function agent."""

from __future__ import annotations
import numpy as np
import time
import random
from typing import Sequence, Optional
from .base import BaseAgent
from ..engine.state import PlayerView, TurnPhase
from ..engine.actions import Action, ActionType
from ..engine.melds import find_best_meld_partition
from ..persistence.trace import DecisionTrace, ActionEvaluation


class RLAgent(BaseAgent):
    """Linear value-function approximation agent trained via Temporal Difference learning."""

    NUM_FEATURES = 10

    def __init__(
        self,
        name: str = "RLAgent",
        player_id: int = 0,
        weights: Optional[np.ndarray] = None,
        learning_rate: float = 0.01,
        gamma: float = 0.95,
        epsilon: float = 0.05,
        rng: Optional[random.Random] = None
    ):
        super().__init__(name, player_id)
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.rng = rng or random.Random()

        # Initialize default calibrated weights if not provided
        if weights is not None:
            self.weights = np.array(weights, dtype=np.float64)
        else:
            # Calibrated strategic prior weights
            self.weights = np.array([
                -0.1,   # 0: Hand deadwood sum (negative is bad)
                0.5,    # 1: Number of melded cards
                0.2,    # 2: Max meld points
                5.0,    # 3: Can open >= 51 pts
                10.0,   # 4: Is opened
                0.3,    # 5: Min opponent cards
                -15.0,  # 6: Unopened risk (opp close to finish while we are unopened)
                1.5,    # 7: Table attachment opportunities
                4.0,    # 8: Number of Jokers in hand
                -2.0    # 9: Discard danger score
            ], dtype=np.float64)

        self.last_features: Optional[np.ndarray] = None
        self.last_val: Optional[float] = None

    def extract_features(self, view: PlayerView, action: Action) -> np.ndarray:
        """Extract a 10-dimensional feature vector representing state-action quality."""
        features = np.zeros(self.NUM_FEATURES, dtype=np.float64)

        hand = view.hand
        best_part = view.best_meld_partition

        # 0: Hand deadwood sum
        features[0] = float(sum(c.hand_penalty_value for c in hand))
        # 1: Number of melded cards
        features[1] = float(len(best_part.used_card_ids))
        # 2: Max meld points
        features[2] = float(best_part.total_points)
        # 3: Can open >= 51
        features[3] = 1.0 if best_part.total_points >= 51 else 0.0
        # 4: Is opened
        features[4] = 1.0 if view.am_i_opened else 0.0

        # 5: Min opponent cards
        opp_counts = [view.player_hand_counts[p] for p in range(view.num_players) if p != self.player_id]
        min_opp = min(opp_counts) if opp_counts else 14
        features[5] = float(min_opp)

        # 6: Unopened risk
        features[6] = 1.0 if (not view.am_i_opened and min_opp <= 5) else 0.0

        # 7: Table attachment opportunities
        attachments = view.table.get_all_attachment_options(hand)
        features[7] = float(len(attachments))

        # 8: Number of Jokers in hand
        features[8] = float(sum(1 for c in hand if c.is_joker))

        # 9: Discard danger score if discarding
        if action.action_type == ActionType.DISCARD and action.card is not None:
            danger = 0.0
            for tm in view.table.melds:
                if view.table.can_attach_card(action.card, tm.meld_id) is not None:
                    danger += 1.0
            features[9] = danger

        return features

    def evaluate_q(self, features: np.ndarray) -> float:
        return float(np.dot(self.weights, features))

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        evaluations: list[ActionEvaluation] = []
        best_action = legal_actions[0]
        best_q = -float("inf")

        for action in legal_actions:
            feat = self.extract_features(view, action)
            q_val = self.evaluate_q(feat)
            evaluations.append(ActionEvaluation(action_str=action.to_str(), q_value=q_val))
            if q_val > best_q:
                best_q = q_val
                best_action = action

        # Epsilon-greedy exploration
        if self.rng.random() < self.epsilon and len(legal_actions) > 1:
            selected = self.rng.choice(list(legal_actions))
        else:
            selected = best_action

        selected_feat = self.extract_features(view, selected)
        self.last_features = selected_feat
        self.last_val = best_q

        latency = (time.perf_counter() - t0) * 1000.0
        trace = self._create_trace(view, selected, evaluations, latency)
        return selected, trace

    def update_weights(self, reward: float, next_val: float) -> None:
        """Perform Temporal Difference TD(0) gradient update."""
        if self.last_features is None or self.last_val is None:
            return

        td_target = reward + self.gamma * next_val
        td_error = td_target - self.last_val
        self.weights += self.learning_rate * td_error * self.last_features
