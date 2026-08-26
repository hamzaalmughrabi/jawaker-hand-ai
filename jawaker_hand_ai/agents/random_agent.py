"""Random baseline agent."""

from __future__ import annotations
import random
import time
from typing import Sequence, Optional
from .base import BaseAgent
from ..engine.state import PlayerView
from ..engine.actions import Action
from ..persistence.trace import DecisionTrace, ActionEvaluation


class RandomAgent(BaseAgent):
    """Uniform random decision-maker serving as a foundational baseline."""

    def __init__(self, name: str = "RandomAgent", player_id: int = 0, rng: Optional[random.Random] = None):
        super().__init__(name, player_id)
        self.rng = rng or random.Random()

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        selected = self.rng.choice(list(legal_actions))
        latency = (time.perf_counter() - t0) * 1000.0

        evals = [
            ActionEvaluation(
                action_str=a.to_str(),
                q_value=0.0,
                probability=1.0 / len(legal_actions)
            )
            for a in legal_actions
        ]

        trace = self._create_trace(view, selected, evals, latency)
        return selected, trace
