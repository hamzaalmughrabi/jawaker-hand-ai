"""Abstract base agent interface for Jawaker Hand."""

from __future__ import annotations
import uuid
import time
from abc import ABC, abstractmethod
from typing import Sequence
from ..engine.state import PlayerView
from ..engine.actions import Action
from ..persistence.trace import DecisionTrace, ActionEvaluation


class BaseAgent(ABC):
    """Abstract interface for all algorithmic and learning agents."""

    def __init__(self, name: str, player_id: int = 0):
        self.name = name
        self.player_id = player_id

    @abstractmethod
    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        """Select an action from legal_actions given the current view and return decision trace."""
        pass

    def reset_round(self) -> None:
        """Reset internal round-specific state."""
        pass

    def _create_trace(
        self,
        view: PlayerView,
        selected_action: Action,
        evaluations: list[ActionEvaluation],
        latency_ms: float,
        belief_summary: dict = None,
        neural_telemetry: dict = None
    ) -> DecisionTrace:
        return DecisionTrace(
            trace_id=str(uuid.uuid4()),
            match_id="MATCH",
            round_number=1,
            turn_number=view.turn_number,
            player_id=self.player_id,
            agent_name=self.name,
            phase=view.phase.value,
            hand_cards=[c.to_str(show_deck=True) for c in view.hand],
            top_discard=view.top_discard.to_str(show_deck=True) if view.top_discard else None,
            is_opened=view.am_i_opened,
            candidate_evaluations=evaluations,
            selected_action=selected_action.to_str(),
            opponent_belief_summary=belief_summary or {},
            neural_telemetry=neural_telemetry or {},
            execution_latency_ms=latency_ms
        )
