"""Jawaker Hand match rules, 5-round progression, descriptive agent names, and cumulative lowest-score ranking."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from .state import RoundScoreResult


@dataclass(frozen=True, slots=True)
class GameRules:
    """Official Jawaker Hand rules and scoring parameters."""
    total_rounds: int = 5
    initial_meld_min_points: int = 51
    normal_finish_points: int = -30
    hand_finish_points: int = -60
    unopened_penalty: int = 100
    unopened_hand_penalty: int = 200
    joker_hand_penalty: int = 15
    ace_hand_penalty: int = 11


@dataclass
class MatchSummary:
    """End-of-match 5-round accounting, descriptive names, and final ranking."""
    winner_id: int
    winner_name: str
    rankings: list[tuple[int, str, int]]  # (player_id, player_name, total_score)
    total_rounds: int
    round_history: list[RoundScoreResult]
    player_names: dict[int, str]
    summary_text: str


@dataclass
class MatchState:
    """Tracks cumulative scores, agent names, and dealer rotation across 5 rounds."""
    num_players: int = 4
    rules: GameRules = field(default_factory=GameRules)
    player_names: dict[int, str] = field(default_factory=dict)
    cumulative_scores: dict[int, int] = field(default_factory=dict)
    round_history: list[RoundScoreResult] = field(default_factory=list)
    current_dealer: int = 0

    def __post_init__(self):
        if not self.cumulative_scores:
            self.cumulative_scores = {p: 0 for p in range(self.num_players)}
        if not self.player_names:
            self.player_names = {p: f"Player_{p}" for p in range(self.num_players)}

    @property
    def rounds_played(self) -> int:
        return len(self.round_history)

    @property
    def is_match_over(self) -> bool:
        return self.rounds_played >= self.rules.total_rounds

    @property
    def leading_player(self) -> int:
        return min(self.cumulative_scores.keys(), key=lambda p: self.cumulative_scores[p])

    def record_round_result(self, result: RoundScoreResult) -> None:
        self.round_history.append(result)
        for p, score in result.round_scores.items():
            self.cumulative_scores[p] += score
        self.current_dealer = (self.current_dealer + 1) % self.num_players

    def get_final_summary(self) -> MatchSummary:
        if not self.is_match_over:
            raise ValueError("Match is not completed yet.")

        # Sort by total score ascending (lowest score wins!)
        sorted_players = sorted(self.cumulative_scores.keys(), key=lambda p: self.cumulative_scores[p])
        rankings = [(p, self.player_names.get(p, f"Player_{p}"), self.cumulative_scores[p]) for p in sorted_players]
        winner_id = rankings[0][0]
        winner_name = rankings[0][1]

        summary_lines = [f"--- JAWAKER HAND 5-ROUND MATCH RESULTS ---"]
        for rank, (p, name, score) in enumerate(rankings, 1):
            is_win_tag = " [WINNER!]" if rank == 1 else ""
            summary_lines.append(f"Rank {rank}: {name} (P{p}) -> {score} pts{is_win_tag}")

        return MatchSummary(
            winner_id=winner_id,
            winner_name=winner_name,
            rankings=rankings,
            total_rounds=self.rounds_played,
            round_history=list(self.round_history),
            player_names=dict(self.player_names),
            summary_text="\n".join(summary_lines)
        )
