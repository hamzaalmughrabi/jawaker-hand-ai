"""Asynchronous exporter from SQLite ExperienceDB to Obsidian-compatible Markdown vault with descriptive agent names."""

from __future__ import annotations
import os
import json
from pathlib import Path
from typing import Optional
from .templates import (
    DISCARD_STRATEGY_TEMPLATE,
    OPENING_51_STRATEGY_TEMPLATE,
    MISTAKE_UNOPENED_TEMPLATE,
    STRATEGY_1V1_TEMPLATE,
    JOKER_MASTERY_TEMPLATE
)
from .oracle import PostGameOracle, BlunderRecord
from ..persistence.db import ExperienceDB


class ObsidianExporter:
    """Exports SQLite experience database and strategic models to an Obsidian Markdown vault."""

    def __init__(self, db: ExperienceDB, vault_dir: str | Path = "obsidian_vault"):
        self.db = db
        self.vault_dir = Path(vault_dir)
        self.oracle = PostGameOracle()

    def export_vault(self) -> dict[str, int]:
        strategy_dir = self.vault_dir / "Strategy"
        opponents_dir = self.vault_dir / "Opponents"
        mistakes_dir = self.vault_dir / "Mistakes"
        games_dir = self.vault_dir / "Games"
        patterns_dir = self.vault_dir / "Learned Patterns"

        for d in [strategy_dir, opponents_dir, mistakes_dir, games_dir, patterns_dir]:
            d.mkdir(parents=True, exist_ok=True)

        counts = {
            "strategies": 0,
            "mistakes": 0,
            "games": 0,
            "opponents": 0,
            "patterns": 0
        }

        # 1. Export Strategy Guides
        (strategy_dir / "Discard Strategy.md").write_text(DISCARD_STRATEGY_TEMPLATE, encoding="utf-8")
        (strategy_dir / "Opening 51 Points Strategy.md").write_text(OPENING_51_STRATEGY_TEMPLATE, encoding="utf-8")
        (strategy_dir / "1v1 Championship Duel Strategy.md").write_text(STRATEGY_1V1_TEMPLATE, encoding="utf-8")
        counts["strategies"] = 3

        # 2. Export Patterns
        (patterns_dir / "Joker Mastery.md").write_text(JOKER_MASTERY_TEMPLATE, encoding="utf-8")
        counts["patterns"] = 1

        # 3. Export Mistakes
        (mistakes_dir / "Unopened Hand Penalty.md").write_text(MISTAKE_UNOPENED_TEMPLATE, encoding="utf-8")
        counts["mistakes"] = 1

        # 4. Export Matches & Games
        matches = self.db.get_all_matches()
        all_blunders: list[BlunderRecord] = []

        for m in matches:
            m_id = m["match_id"]
            traces = self.db.get_traces_for_match(m_id)
            game_doc = self._generate_game_doc(m, traces)
            (games_dir / f"{m_id}.md").write_text(game_doc, encoding="utf-8")
            counts["games"] += 1

            # Detect blunders
            blunders = self.oracle.analyze_traces(traces, [])
            all_blunders.extend(blunders)

        # Write Blunder Summary
        blunder_doc = self._generate_blunder_summary_doc(all_blunders)
        (mistakes_dir / "Blunder Log.md").write_text(blunder_doc, encoding="utf-8")
        counts["mistakes"] += 1

        # 5. Export Learned Patterns & Vault Index
        index_doc = self._generate_index_doc(counts, matches)
        (self.vault_dir / "Index.md").write_text(index_doc, encoding="utf-8")

        return counts

    def _generate_game_doc(self, match: dict, traces: list) -> str:
        m_id = match["match_id"]
        num_p = match["num_players"]
        match_type_str = "1v1 Championship Duel" if num_p == 2 else f"{num_p}-Player Table"

        # Parse agent names from traces
        player_agents: dict[int, str] = {}
        for t in traces:
            if t.player_id not in player_agents:
                player_agents[t.player_id] = t.agent_name

        winner_id = match["winner_id"]
        winner_name = player_agents.get(winner_id, f"Player {winner_id}")

        lines = [
            f"# Match Record: {m_id}",
            "",
            f"**Match Type**: {match_type_str}",
            f"**Date**: {match.get('created_at', 'N/A')}",
            f"**Winner**: **{winner_name}** (P{winner_id})",
            f"**Total Rounds**: {match['total_rounds']}",
            "",
            "## Participating Agents",
            "| Player Seat | Agent Architecture | Name |",
            "|---|---|---|"
        ]
        for p in range(num_p):
            a_name = player_agents.get(p, f"Agent_P{p}")
            lines.append(f"| P{p} | `{a_name.split('_')[0]}` | **{a_name}** |")

        lines.extend([
            "",
            "## Final Score Accounting",
            f"```\n{match.get('summary', '')}\n```",
            "",
            "## AI Decision Traces Sample",
            f"Total AI Decisions Recorded: {len(traces)}",
            "",
            "| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |",
            "|---|---|---|---|---|---|---|"
        ])
        for t in traces[:35]:
            lines.append(f"| R{t.round_number} | T{t.turn_number} | P{t.player_id} | **{t.agent_name}** | {t.phase} | `{t.selected_action}` | {t.execution_latency_ms:.1f}ms |")

        lines.extend([
            "",
            "## Strategy & Analysis Links",
            "- [[1v1 Championship Duel Strategy]]",
            "- [[Opening 51 Points Strategy]]",
            "- [[Discard Strategy]]",
            "- [[Joker Mastery]]",
            "- [[Unopened Hand Penalty]]"
        ])
        return "\n".join(lines)

    def _generate_blunder_summary_doc(self, blunders: list[BlunderRecord]) -> str:
        lines = [
            "# Post-Game Blunder Analysis Log",
            "",
            f"Total Blunders Detected by Oracle: {len(blunders)}",
            "",
            "| Round | Turn | Player | Blunder Type | Action Taken | Recommended Action | Cost Est. |",
            "|---|---|---|---|---|---|---|"
        ]
        for b in blunders[:50]:
            lines.append(f"| R{b.round_number} | T{b.turn_number} | P{b.player_id} | **{b.blunder_type}** | `{b.action_taken}` | `{b.recommended_action}` | +{b.point_cost_estimate} pts |")
        return "\n".join(lines)

    def _generate_index_doc(self, counts: dict[str, int], matches: list) -> str:
        lines = [
            "# Jawaker Hand AI Knowledge Vault",
            "",
            "Welcome to the long-term knowledge base, game logs, and inspection layer for the **Jawaker Hand AI System**.",
            "",
            "## Strategy Guides",
            "- [[1v1 Championship Duel Strategy]] - Strategic principles and tempo control in 1v1 duels.",
            "- [[Opening 51 Points Strategy]] - Mathematical valuation of initial melds and Ace point rules.",
            "- [[Discard Strategy]] - Safe discard calculation and table layoff defense.",
            "- [[Joker Mastery]] - Tactical Joker substitution and liberation patterns.",
            "",
            "## Mistake Analysis",
            "- [[Unopened Hand Penalty]] - Post-mortem analysis on unopened round losses (+100/+200 pts).",
            "- [[Blunder Log]] - Oracle blunder detection across completed matches.",
            "",
            "## Vault Statistics",
            f"- Matches Archived: {len(matches)}",
            f"- Documented Strategies: {counts['strategies']}",
            f"- Documented Mistakes: {counts['mistakes']}",
            f"- Discovered Patterns: {counts['patterns']}",
            "",
            "## Recent Match Logs"
        ]
        for m in matches[:15]:
            m_id = m["match_id"]
            lines.append(f"- [[{m_id}]] (Winner: Player {m['winner_id']})")

        return "\n".join(lines)
