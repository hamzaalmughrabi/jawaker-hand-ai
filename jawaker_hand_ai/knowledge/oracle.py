"""Post-game perfect-information oracle for detecting blunders and suboptimal plays."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence, Optional
from ..engine.state import GameState, RoundScoreResult
from ..persistence.trace import DecisionTrace


@dataclass
class BlunderRecord:
    """A detected strategic blunder identified via post-game oracle analysis."""
    trace_id: str
    round_number: int
    turn_number: int
    player_id: int
    blunder_type: str
    action_taken: str
    recommended_action: str
    point_cost_estimate: int
    explanation: str


class PostGameOracle:
    """Analyzes completed matches to identify blunders against perfect-information hindsight."""

    def analyze_traces(
        self,
        traces: Sequence[DecisionTrace],
        round_results: Sequence[RoundScoreResult]
    ) -> list[BlunderRecord]:
        blunders: list[BlunderRecord] = []

        for trace in traces:
            # Check 1: Held >= 51 points without opening when an opponent was about to finish
            if not trace.is_opened and trace.phase == "MELD":
                # Check candidate evaluations
                opening_evals = [e for e in trace.candidate_evaluations if e.action_str.startswith("INITIAL_MELD")]
                if opening_evals and trace.selected_action == "PASS_MELD":
                    # If this round ended with this player unopened (+100 penalty)
                    r_res = round_results[trace.round_number - 1] if trace.round_number <= len(round_results) else None
                    if r_res and trace.player_id in r_res.unopened_players:
                        blunders.append(BlunderRecord(
                            trace_id=trace.trace_id,
                            round_number=trace.round_number,
                            turn_number=trace.turn_number,
                            player_id=trace.player_id,
                            blunder_type="Failed to Open with >= 51 Available",
                            action_taken="PASS_MELD",
                            recommended_action=opening_evals[0].action_str,
                            point_cost_estimate=100,
                            explanation="Passed meld phase despite holding >= 51 valid meld points, resulting in +100 unopened penalty when round ended."
                        ))

            # Check 2: Discarded high-value Ace (11 pts) or Joker (15 pts) instead of low card
            if trace.phase == "DISCARD":
                if "JK" in trace.selected_action:
                    blunders.append(BlunderRecord(
                        trace_id=trace.trace_id,
                        round_number=trace.round_number,
                        turn_number=trace.turn_number,
                        player_id=trace.player_id,
                        blunder_type="Discarded Wild Joker",
                        action_taken=trace.selected_action,
                        recommended_action="Keep Joker to complete sets/runs",
                        point_cost_estimate=30,
                        explanation="Discarded a Wild Joker (valued at 15 penalty points and universal wild card utility)."
                    ))

        return blunders
