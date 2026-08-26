"""Structured decision trace telemetry capturing AI evaluations, probabilities, and search trees."""

from __future__ import annotations
import json
from dataclasses import dataclass, asdict, field
from typing import Optional, Any


@dataclass
class ActionEvaluation:
    """Evaluation score and metrics for a candidate action considered by the AI."""
    action_str: str
    q_value: float
    probability: float = 0.0
    visit_count: int = 0
    heuristics: dict[str, float] = field(default_factory=dict)


@dataclass
class DecisionTrace:
    """Complete structured trace of an AI decision for learning, telemetry, and Obsidian inspection."""
    trace_id: str
    match_id: str
    round_number: int
    turn_number: int
    player_id: int
    agent_name: str
    phase: str
    hand_cards: list[str]
    top_discard: Optional[str]
    is_opened: bool
    candidate_evaluations: list[ActionEvaluation]
    selected_action: str
    opponent_belief_summary: dict[str, Any] = field(default_factory=dict)
    neural_telemetry: dict[str, Any] = field(default_factory=dict)
    execution_latency_ms: float = 0.0
    round_outcome_points: Optional[int] = None
    created_at: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DecisionTrace:
        evals = [ActionEvaluation(**e) if isinstance(e, dict) else e for e in data.get("candidate_evaluations", [])]
        data_copy = dict(data)
        data_copy["candidate_evaluations"] = evals
        # Filter fields matching dataclass attributes
        valid_keys = cls.__dataclass_fields__.keys()
        filtered = {k: v for k, v in data_copy.items() if k in valid_keys}
        return cls(**filtered)
