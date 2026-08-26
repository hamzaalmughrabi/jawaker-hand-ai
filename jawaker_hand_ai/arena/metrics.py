"""Statistical performance metrics, ELO rating updates, and confidence intervals."""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Sequence


@dataclass
class PerformanceMetrics:
    """Aggregated performance metrics for an agent across tournament matches."""
    agent_name: str
    matches_played: int
    matches_won: int
    win_rate: float
    win_rate_ci_low: float
    win_rate_ci_high: float
    avg_match_points: float
    points_std_dev: float
    rounds_won: int
    hand_finishes: int
    elo_rating: float = 1500.0


def calculate_confidence_interval(successes: int, total: int, confidence: float = 0.95) -> tuple[float, float]:
    """Calculate Wilson score interval for binomial proportion."""
    if total == 0:
        return 0.0, 0.0
    z = 1.96 if confidence == 0.95 else 2.576
    p = successes / total
    denom = 1 + (z ** 2) / total
    center = (p + (z ** 2) / (2 * total)) / denom
    margin = (z * math.sqrt((p * (1 - p) + (z ** 2) / (4 * total)) / total)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def update_elo_multiplayer(
    ratings: list[float],
    scores: list[int],
    k_factor: float = 32.0
) -> list[float]:
    """Update ELO ratings for a multiplayer match based on score rankings (lower score is better)."""
    n = len(ratings)
    new_ratings = list(ratings)

    # Convert scores to ranks (rank 1 is best)
    # Compare each pair (i, j)
    for i in range(n):
        delta = 0.0
        for j in range(n):
            if i == j:
                continue
            r_i = ratings[i]
            r_j = ratings[j]
            expected_i = 1.0 / (1.0 + 10.0 ** ((r_j - r_i) / 400.0))

            # Actual outcome: 1.0 if score[i] < score[j] (i won), 0.5 if tie, 0.0 if score[i] > score[j]
            if scores[i] < scores[j]:
                actual_i = 1.0
            elif scores[i] == scores[j]:
                actual_i = 0.5
            else:
                actual_i = 0.0

            delta += (k_factor / (n - 1)) * (actual_i - expected_i)
        new_ratings[i] += delta

    return new_ratings
