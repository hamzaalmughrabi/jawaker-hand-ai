"""Hamza vs AI 100-Match Session Tracker and Learning Analyzer."""

from __future__ import annotations
import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class HumanMatchRecord:
    match_num: int
    winner: str
    human_score: int
    ai_score: int
    rounds: int
    weaknesses_noted: str
    created_at: str


class HumanSessionTracker:
    """Manages the 100-match benchmark between Hamza and the Apex Grandmaster AI."""

    def __init__(self, db_path: str | Path = "experience.db"):
        self.db_path = str(db_path)
        self._init_table()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_table(self) -> None:
        conn = self._get_connection()
        try:
            with conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS human_sessions (
                        match_num INTEGER PRIMARY KEY AUTOINCREMENT,
                        winner TEXT NOT NULL,
                        human_score INTEGER NOT NULL,
                        ai_score INTEGER NOT NULL,
                        rounds INTEGER NOT NULL,
                        weaknesses_noted TEXT,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
        finally:
            conn.close()

    def record_match(self, winner: str, human_score: int, ai_score: int, rounds: int = 5, notes: str = "") -> int:
        conn = self._get_connection()
        try:
            with conn:
                cursor = conn.execute(
                    """
                    INSERT INTO human_sessions (winner, human_score, ai_score, rounds, weaknesses_noted)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (winner, human_score, ai_score, rounds, notes)
                )
                return cursor.lastrowid
        finally:
            conn.close()

    def get_all_records(self) -> list[HumanMatchRecord]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM human_sessions ORDER BY match_num ASC")
            records = []
            for r in cursor.fetchall():
                records.append(HumanMatchRecord(
                    match_num=r["match_num"],
                    winner=r["winner"],
                    human_score=r["human_score"],
                    ai_score=r["ai_score"],
                    rounds=r["rounds"],
                    weaknesses_noted=r["weaknesses_noted"] or "",
                    created_at=r["created_at"]
                ))
            return records
        finally:
            conn.close()

    def print_leaderboard(self) -> str:
        records = self.get_all_records()
        total = len(records)
        if total == 0:
            return "No Human vs AI matches recorded yet. Play a match to start your 100-match challenge!"

        human_wins = sum(1 for r in records if "hamza" in r.winner.lower() or "human" in r.winner.lower())
        ai_wins = sum(1 for r in records if "ai" in r.winner.lower() or "apex" in r.winner.lower())
        draws = total - human_wins - ai_wins

        human_wr = (human_wins / total) * 100
        ai_wr = (ai_wins / total) * 100

        lines = [
            "=================================================================",
            "           🏆 HAMZA VS APEX GRANDMASTER AI (100-MATCH LOG)        ",
            "=================================================================",
            f"Total Matches Played : {total} / 100",
            f"  Hamza Wins         : {human_wins} ({human_wr:.1f}%)",
            f"  AI Wins            : {ai_wins} ({ai_wr:.1f}%)",
            f"  Draws              : {draws}",
            "-----------------------------------------------------------------",
            f"{'#':<4} {'Winner':<12} {'Hamza Pts':<12} {'AI Pts':<10} {'Notes / Weaknesses'}",
            "-----------------------------------------------------------------"
        ]

        for r in records[-15:]:
            lines.append(f"{r.match_num:<4} {r.winner:<12} {r.human_score:<12} {r.ai_score:<10} {r.weaknesses_noted[:40]}")

        lines.append("=================================================================")
        return "\n".join(lines)
