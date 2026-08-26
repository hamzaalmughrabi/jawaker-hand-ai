"""SQLite persistence client for storing match accounting, decision traces, and player profiles."""

from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from typing import Optional, Any
from .schema import create_schema
from .trace import DecisionTrace, ActionEvaluation
from ..engine.state import RoundScoreResult
from ..engine.rules import MatchSummary


class ExperienceDB:
    """Encapsulates thread-safe SQLite operations for match experience and telemetry."""

    def __init__(self, db_path: str | Path = "experience.db"):
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        try:
            create_schema(conn)
        finally:
            conn.close()

    def save_match(self, match_id: str, num_players: int, summary: MatchSummary) -> None:
        conn = self._get_connection()
        try:
            final_scores = {}
            for item in summary.rankings:
                if len(item) == 3:
                    p, _, score = item
                else:
                    p, score = item
                final_scores[p] = score

            final_scores_json = json.dumps(final_scores)

            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO matches (match_id, num_players, total_rounds, winner_id, final_scores, summary)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        match_id,
                        num_players,
                        summary.total_rounds,
                        summary.winner_id,
                        final_scores_json,
                        summary.summary_text
                    )
                )
        finally:
            conn.close()

    def save_round(self, match_id: str, round_number: int, dealer_id: int, result: RoundScoreResult) -> None:
        conn = self._get_connection()
        try:
            round_scores_json = json.dumps(result.round_scores)
            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO rounds (
                        round_id, match_id, round_number, dealer_id, winner_id,
                        is_hand_finish, is_normal_finish, is_stock_exhausted,
                        round_scores, score_breakdown
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        f"{match_id}_R{round_number}",
                        match_id,
                        round_number,
                        dealer_id,
                        result.winner_id,
                        int(result.is_hand_finish),
                        int(result.is_normal_finish),
                        int(result.is_stock_exhausted),
                        round_scores_json,
                        result.score_breakdown
                    )
                )
        finally:
            conn.close()

    def save_decision_trace(self, trace: DecisionTrace) -> None:
        conn = self._get_connection()
        try:
            evals_json = json.dumps([
                {
                    "action_str": e.action_str,
                    "q_value": e.q_value,
                    "probability": e.probability,
                    "visit_count": e.visit_count
                }
                for e in trace.candidate_evaluations
            ])
            belief_json = json.dumps(trace.opponent_belief_summary or {})
            hand_json = json.dumps(trace.hand_cards)

            with conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO decision_traces (
                        trace_id, match_id, round_number, turn_number,
                        player_id, agent_name, phase, hand_cards,
                        is_opened, selected_action, candidate_evaluations,
                        opponent_belief_summary, execution_latency_ms
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        trace.trace_id,
                        trace.match_id,
                        trace.round_number,
                        trace.turn_number,
                        trace.player_id,
                        trace.agent_name,
                        trace.phase,
                        hand_json,
                        int(trace.is_opened),
                        trace.selected_action,
                        evals_json,
                        belief_json,
                        trace.execution_latency_ms
                    )
                )
        finally:
            conn.close()

    def get_all_matches(self) -> list[dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM matches ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_traces_for_match(self, match_id: str) -> list[DecisionTrace]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM decision_traces WHERE match_id = ? ORDER BY round_number ASC, turn_number ASC",
                (match_id,)
            )
            rows = cursor.fetchall()
            traces = []
            for r in rows:
                raw_evals = json.loads(r["candidate_evaluations"]) if r["candidate_evaluations"] else []
                evals = []
                for e in raw_evals:
                    if isinstance(e, dict):
                        act_str = e.get("action_str") or e.get("action", "")
                        evals.append(ActionEvaluation(
                            action_str=act_str,
                            q_value=e.get("q_value", 0.0),
                            probability=e.get("probability", 0.0),
                            visit_count=e.get("visit_count", 0)
                        ))

                trace = DecisionTrace(
                    trace_id=r["trace_id"],
                    match_id=r["match_id"],
                    round_number=r["round_number"],
                    turn_number=r["turn_number"],
                    player_id=r["player_id"],
                    agent_name=r["agent_name"],
                    phase=r["phase"],
                    hand_cards=json.loads(r["hand_cards"]) if r["hand_cards"] else [],
                    top_discard=None,
                    is_opened=bool(r["is_opened"]),
                    candidate_evaluations=evals,
                    selected_action=r["selected_action"],
                    opponent_belief_summary=json.loads(r["opponent_belief_summary"]) if r["opponent_belief_summary"] else {},
                    execution_latency_ms=r["execution_latency_ms"]
                )
                traces.append(trace)
            return traces
        finally:
            conn.close()
