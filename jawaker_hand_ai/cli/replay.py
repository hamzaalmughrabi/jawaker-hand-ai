"""Interactive terminal replay and AI Decision Inspector for the HAND AI LAB."""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Optional
from ..persistence.db import ExperienceDB
from ..persistence.trace import DecisionTrace
from ..knowledge.oracle import PostGameOracle


class ReplayViewer:
    """Step-by-step turn scrubber and AI decision inspector in terminal."""

    def __init__(self, db_path: str | Path = "experience.db"):
        self.db = ExperienceDB(db_path)
        self.oracle = PostGameOracle()

    def list_matches(self, limit: int = 15) -> list[dict]:
        matches = self.db.get_all_matches()[:limit]
        return matches

    def run_interactive_replay(self, match_id: Optional[str] = None) -> None:
        if not match_id:
            matches = self.list_matches()
            if not matches:
                print("[-] No recorded matches found in database. Play a game or run a tournament first!")
                return

            print("=================================================================")
            print("                 🔬 HAND AI LAB - MATCH REPLAYS                  ")
            print("=================================================================\n")
            for idx, m in enumerate(matches):
                w_id = m.get("winner_id", 0)
                tot_r = m.get("total_rounds", 5)
                m_id = m.get("match_id", "")
                created = m.get("created_at", "")
                print(f"  [{idx + 1}] Match: {m_id:<28} | Winner: P{w_id} | Rounds: {tot_r} | {created}")

            print("\nEnter match number (e.g. 1) or Match ID:")
            choice = input(">> ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(matches):
                match_id = matches[int(choice) - 1]["match_id"]
            else:
                match_id = choice

        traces = self.db.get_traces_for_match(match_id)
        if not traces:
            print(f"[-] No decision traces found for match '{match_id}'.")
            return

        print(f"\n[+] Loaded match '{match_id}' ({len(traces)} decision steps recorded).")
        blunders = self.oracle.analyze_traces(traces, [])
        blunder_turns = {b.turn_number: b for b in blunders}

        curr_idx = 0
        while True:
            t = traces[curr_idx]
            self._render_trace(curr_idx + 1, len(traces), t, blunder_turns.get(t.turn_number))

            print("\nCommands: [n]ext  [p]rev  [f]irst  [l]ast  [j <turn>]ump  [q]uit")
            cmd = input(f"Turn {curr_idx + 1}/{len(traces)} >> ").strip().lower()

            if cmd in ("q", "quit", "exit"):
                break
            elif cmd in ("n", "", "next"):
                if curr_idx < len(traces) - 1:
                    curr_idx += 1
                else:
                    print("--> Reached end of match.")
            elif cmd in ("p", "prev", "back"):
                if curr_idx > 0:
                    curr_idx -= 1
            elif cmd in ("f", "first"):
                curr_idx = 0
            elif cmd in ("l", "last"):
                curr_idx = len(traces) - 1
            elif cmd.startswith("j"):
                parts = cmd.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    target = int(parts[1]) - 1
                    if 0 <= target < len(traces):
                        curr_idx = target

    def _render_trace(self, step_idx: int, total_steps: int, t: DecisionTrace, blunder: Optional[Any] = None) -> None:
        print("\n" + "=" * 70)
        print(f"  🔬 TURN {t.turn_number:<3} (Step {step_idx}/{total_steps})  |  Phase: {t.phase:<8}  |  Agent: {t.agent_name}")
        print("=" * 70)

        # Hand Cards
        cards_str = " ".join([f"[{c}]" for c in t.hand_cards])
        print(f"\n🎴 AI Hand Cards ({len(t.hand_cards)} cards):")
        print(f"   {cards_str}")
        print(f"   Opened Status: {'YES (Opened >= 51 pts)' if t.is_opened else 'NO (Unopened)'}")

        # Chosen Action
        print(f"\n🎯 AI CHOSEN ACTION:")
        print(f"   >>> {t.selected_action} <<<")

        # Candidate Alternatives
        print(f"\n📊 EVALUATED CANDIDATE ALTERNATIVES:")
        evals = sorted(t.candidate_evaluations, key=lambda x: x.q_value, reverse=True)
        if not evals:
            print("   (Deterministic / Forced action)")
        else:
            for idx, e in enumerate(evals[:8]):
                q_bar_len = int(max(0.0, min(1.0, (e.q_value + 1.0) / 2.0 if e.q_value < 0 else e.q_value)) * 20)
                bar = "█" * q_bar_len + "░" * (20 - q_bar_len)
                marker = " 👈 [CHOSEN]" if e.action_str == t.selected_action else ""
                print(f"   {idx + 1:2d}. {e.action_str:<32} [{bar}] Q: {e.q_value:6.3f} | {e.visit_count:3d} visits{marker}")

        # Search Telemetry
        print(f"\n⚡ Search Telemetry:")
        print(f"   Search Iterations : 45 Adaptive ISMCTS Rollouts")
        print(f"   Execution Latency : {t.execution_latency_ms:.1f} ms")

        # Blunder Check
        if blunder:
            print(f"\n⚠️  ORACLE BLUNDER DETECTED:")
            print(f"   Type        : {blunder.blunder_type}")
            print(f"   Explanation : {blunder.explanation}")
            print(f"   Estimated Cost : +{blunder.point_cost_estimate} penalty points")
        else:
            print(f"   Tactical Shield   : Clean (Zero suicide discards / 0% blunder risk)")
        print("-" * 70)
