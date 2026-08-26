"""Deep Reinforcement Learning Agent using Neural Value Network evaluation."""

from __future__ import annotations
import time
import random
import numpy as np
from typing import Sequence, Optional
from .base import BaseAgent
from ..engine.state import PlayerView, TurnPhase
from ..engine.actions import Action, ActionType
from ..engine.melds import find_best_meld_partition
from ..learning.network import NeuralValueNetwork
from ..persistence.trace import DecisionTrace, ActionEvaluation


class DeepRLAgent(BaseAgent):
    """World-class Deep Reinforcement Learning Agent with a 32-dim neural state-action evaluator."""

    FEATURE_DIM = 32

    def __init__(
        self,
        name: str = "DeepRLAgent",
        player_id: int = 0,
        network: Optional[NeuralValueNetwork] = None,
        epsilon: float = 0.05,
        rng: Optional[random.Random] = None
    ):
        super().__init__(name, player_id)
        self.network = network or NeuralValueNetwork(seed=player_id + 100)
        self.epsilon = epsilon
        self.rng = rng or random.Random()

    def extract_features(self, view: PlayerView, action: Action) -> np.ndarray:
        """Extract a comprehensive 32-dimensional strategic feature vector."""
        vec = np.zeros(self.FEATURE_DIM, dtype=np.float64)
        hand = view.hand
        best_part = view.best_meld_partition

        deadwood_sum = sum(c.hand_penalty_value for c in hand)
        melded_count = len(best_part.used_card_ids)

        opp_counts = [view.player_hand_counts[p] for p in range(view.num_players) if p != self.player_id]
        min_opp = min(opp_counts) if opp_counts else 14
        opp_opened_cnt = sum(1 for p in range(view.num_players) if p != self.player_id and view.player_is_opened[p])

        # Core features
        vec[0] = deadwood_sum / 100.0
        vec[1] = melded_count / 14.0
        vec[2] = best_part.total_points / 100.0
        vec[3] = 1.0 if best_part.total_points >= 51 else 0.0
        vec[4] = 1.0 if view.am_i_opened else 0.0
        vec[5] = min_opp / 14.0
        vec[6] = 1.0 if (not view.am_i_opened and min_opp <= 5) else 0.0

        attachments = view.table.get_all_attachment_options(hand)
        joker_swaps = view.table.get_all_joker_swap_options(hand)
        vec[7] = len(attachments) / 10.0
        vec[8] = sum(1 for c in hand if c.is_joker) / 2.0
        vec[9] = 1.0 if len(joker_swaps) > 0 else 0.0

        vec[10] = min(1.0, view.turn_number / 40.0)
        vec[11] = len(hand) / 15.0

        # Suit distribution
        for c in hand:
            if not c.is_joker and c.suit is not None:
                vec[12 + c.suit.value] += 0.1

        # Card composition
        vec[16] = sum(1 for c in hand if not c.is_joker and c.rank.value == 1) / 4.0  # Aces
        vec[17] = sum(1 for c in hand if not c.is_joker and c.rank.value >= 10) / 8.0  # Face cards

        # Discard danger
        if action.action_type == ActionType.DISCARD and action.card is not None:
            danger = 0.0
            for tm in view.table.melds:
                if view.table.can_attach_card(action.card, tm.meld_id) is not None:
                    danger += 1.0
            vec[18] = danger / 4.0
            vec[19] = action.card.hand_penalty_value / 15.0
            vec[20] = 1.0 if action.card.id not in best_part.used_card_ids else 0.0

        # Game context
        vec[21] = 1.0 if view.num_players == 2 else 0.0  # 1v1 flag
        vec[22] = opp_opened_cnt / max(1, view.num_players - 1)
        vec[23] = max(0.0, 1.0 - (view.stock_count / 80.0))
        vec[24] = 1.0 if (not view.am_i_opened and melded_count >= 13) else 0.0  # Hand ambition
        vec[25] = len(view.table.melds) / 10.0

        # Action type encoding
        action_codes = {
            ActionType.DRAW_DISCARD: 0.1,
            ActionType.DRAW_STOCK: 0.2,
            ActionType.INITIAL_MELD: 0.5,
            ActionType.SWAP_JOKER: 0.7,
            ActionType.ATTACH_CARD: 0.8,
            ActionType.LAY_MELD: 0.9,
            ActionType.DISCARD: 1.0,
            ActionType.PASS_MELD: 0.0
        }
        vec[26] = action_codes.get(action.action_type, 0.0)
        vec[27] = 1.0  # Bias term

        return vec

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        evaluations: list[ActionEvaluation] = []
        best_action = legal_actions[0]
        best_q = -float("inf")

        # Feature matrix for batch forward pass
        features_list = [self.extract_features(view, a) for a in legal_actions]
        X = np.array(features_list, dtype=np.float64)

        # Batch forward pass through Neural Value Network
        y_preds = self.network.forward(X)[0].flatten()

        for idx, action in enumerate(legal_actions):
            # In Jawaker Hand, lower penalty is better! Convert predicted score to positive utility
            predicted_score = float(y_preds[idx])
            utility = -predicted_score

            # Additional strategic action boost
            if action.action_type == ActionType.INITIAL_MELD:
                utility += 15.0
            elif action.action_type == ActionType.SWAP_JOKER:
                utility += 20.0

            evaluations.append(ActionEvaluation(action_str=action.to_str(), q_value=round(utility, 2)))
            if utility > best_q:
                best_q = utility
                best_action = action

        # Epsilon-greedy exploration
        if self.rng.random() < self.epsilon and len(legal_actions) > 1:
            selected = self.rng.choice(list(legal_actions))
        else:
            selected = best_action

        latency = (time.perf_counter() - t0) * 1000.0
        trace = self._create_trace(view, selected, evaluations, latency)
        return selected, trace
