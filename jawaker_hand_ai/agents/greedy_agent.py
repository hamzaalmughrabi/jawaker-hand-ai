"""Greedy deadwood-minimization and immediate-meld agent."""

from __future__ import annotations
import time
from typing import Sequence
from .base import BaseAgent
from ..engine.state import PlayerView, TurnPhase
from ..engine.actions import Action, ActionType
from ..engine.melds import find_best_meld_partition
from ..persistence.trace import DecisionTrace, ActionEvaluation


class GreedyAgent(BaseAgent):
    """Deterministic greedy agent that maximizes immediate points and minimizes unmelded penalties."""

    def __init__(self, name: str = "GreedyAgent", player_id: int = 0):
        super().__init__(name, player_id)

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        evaluations: list[ActionEvaluation] = []
        best_action = legal_actions[0]
        best_score = -float("inf")

        for action in legal_actions:
            score = self._evaluate_action(view, action)
            evaluations.append(ActionEvaluation(action_str=action.to_str(), q_value=score))
            if score > best_score:
                best_score = score
                best_action = action

        latency = (time.perf_counter() - t0) * 1000.0
        trace = self._create_trace(view, best_action, evaluations, latency)
        return best_action, trace

    def _evaluate_action(self, view: PlayerView, action: Action) -> float:
        if action.action_type == ActionType.DRAW_DISCARD:
            return 100.0  # High preference for known useful card
        elif action.action_type == ActionType.DRAW_STOCK:
            return 50.0

        elif action.action_type == ActionType.INITIAL_MELD:
            pts = sum(m.points for m in action.melds) if action.melds else 0
            return 500.0 + pts  # High reward for opening >= 51

        elif action.action_type == ActionType.SWAP_JOKER:
            return 400.0  # High value in liberating a Joker

        elif action.action_type == ActionType.ATTACH_CARD:
            pts = action.card.hand_penalty_value if action.card else 10
            return 300.0 + pts

        elif action.action_type == ActionType.LAY_MELD:
            pts = sum(m.points for m in action.melds) if action.melds else 0
            return 200.0 + pts

        elif action.action_type == ActionType.PASS_MELD:
            return 0.0

        elif action.action_type == ActionType.DISCARD:
            if action.card is None:
                return 0.0
            # Identify which cards are in best melds
            best_part = view.best_meld_partition
            is_melded = action.card.id in best_part.used_card_ids
            # We want to discard unmelded cards with high penalty value!
            if not is_melded:
                return 50.0 + action.card.hand_penalty_value
            else:
                return -50.0 + action.card.hand_penalty_value

        return 0.0
