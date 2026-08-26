"""Multi-agent tournament execution, benchmarking, and leaderboard compilation."""

from __future__ import annotations
import numpy as np
import random
from dataclasses import dataclass
from typing import Sequence, Optional, Callable
from .match import MatchRunner
from .metrics import PerformanceMetrics, calculate_confidence_interval, update_elo_multiplayer
from ..agents.base import BaseAgent
from ..persistence.db import ExperienceDB
from ..engine.rules import GameRules


@dataclass
class TournamentReport:
    """Consolidated tournament summary and leaderboard."""
    total_matches: int
    leaderboard: list[PerformanceMetrics]
    report_text: str


class TournamentRunner:
    """Runs automated round-robin or repeated matches across multiple AI agent architectures."""

    def __init__(
        self,
        agent_factories: dict[str, Callable[[int], BaseAgent]],
        db: Optional[ExperienceDB] = None,
        rng: Optional[random.Random] = None
    ):
        self.agent_factories = agent_factories
        self.db = db
        self.rng = rng or random.Random()
        self.match_runner = MatchRunner(db=self.db, rng=self.rng)

    def run_tournament(self, num_matches: int = 20, players_per_match: int = 4) -> TournamentReport:
        agent_names = list(self.agent_factories.keys())
        stats: dict[str, dict] = {
            name: {
                "matches_played": 0,
                "matches_won": 0,
                "rounds_won": 0,
                "hand_finishes": 0,
                "scores": [],
                "elo": 1500.0
            }
            for name in agent_names
        }

        rules = GameRules()

        for m_idx in range(num_matches):
            if len(agent_names) >= players_per_match:
                selected_names = self.rng.sample(agent_names, players_per_match)
            else:
                selected_names = [self.rng.choice(agent_names) for _ in range(players_per_match)]

            agents = [self.agent_factories[name](p_id) for p_id, name in enumerate(selected_names)]

            summary = self.match_runner.play_match(agents=agents, rules=rules)

            scores_by_player = [item[2] if len(item) == 3 else item[1] for item in summary.rankings]
            winner_p_id = summary.winner_id
            winner_name = selected_names[winner_p_id]

            curr_elos = [stats[name]["elo"] for name in selected_names]
            new_elos = update_elo_multiplayer(curr_elos, scores_by_player)
            for p_idx, name in enumerate(selected_names):
                stats[name]["elo"] = new_elos[p_idx]

            for p_idx, name in enumerate(selected_names):
                p_score = next(item[2] if len(item) == 3 else item[1] for item in summary.rankings if item[0] == p_idx)
                stats[name]["matches_played"] += 1
                stats[name]["scores"].append(p_score)
                if p_idx == winner_p_id:
                    stats[name]["matches_won"] += 1

                for r_res in summary.round_history:
                    if r_res.winner_id == p_idx:
                        stats[name]["rounds_won"] += 1
                        if r_res.is_hand_finish:
                            stats[name]["hand_finishes"] += 1

        leaderboard: list[PerformanceMetrics] = []
        for name in agent_names:
            st = stats[name]
            played = st["matches_played"]
            won = st["matches_won"]
            win_rate = (won / played) if played > 0 else 0.0
            ci_low, ci_high = calculate_confidence_interval(won, played)
            avg_pts = float(np.mean(st["scores"])) if st["scores"] else 0.0
            std_pts = float(np.std(st["scores"])) if st["scores"] else 0.0

            leaderboard.append(PerformanceMetrics(
                agent_name=name,
                matches_played=played,
                matches_won=won,
                win_rate=round(win_rate, 3),
                win_rate_ci_low=round(ci_low, 3),
                win_rate_ci_high=round(ci_high, 3),
                avg_match_points=round(avg_pts, 1),
                points_std_dev=round(std_pts, 1),
                rounds_won=st["rounds_won"],
                hand_finishes=st["hand_finishes"],
                elo_rating=round(st["elo"], 1)
            ))

        leaderboard.sort(key=lambda m: m.elo_rating, reverse=True)

        lines = [
            f"================ JAWAKER HAND TOURNAMENT LEADERBOARD ================",
            f"Total Matches Played: {num_matches} (5 rounds per match)",
            f"{'Agent':<20} | {'Played':<6} | {'Win Rate (95% CI)':<20} | {'Avg Score':<10} | {'ELO':<7} | {'Hands Won'}",
            "-" * 84
        ]
        for m in leaderboard:
            ci_str = f"{m.win_rate*100:.1f}% [{m.win_rate_ci_low*100:.1f}%-{m.win_rate_ci_high*100:.1f}%]"
            lines.append(
                f"{m.agent_name:<20} | {m.matches_played:<6} | {ci_str:<20} | {m.avg_match_points:<10} | {m.elo_rating:<7} | {m.rounds_won} ({m.hand_finishes} Hands)"
            )
        lines.append("=" * 84)

        return TournamentReport(
            total_matches=num_matches,
            leaderboard=leaderboard,
            report_text="\n".join(lines)
        )
