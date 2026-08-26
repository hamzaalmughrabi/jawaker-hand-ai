"""Interactive human-versus-AI gameplay CLI interface for Jawaker Hand."""

from __future__ import annotations
import sys
import time
import random
from pathlib import Path
from typing import Optional
from ..engine.card import Card
from ..engine.state import GameState, TurnPhase, PlayerView
from ..engine.actions import Action, ActionType
from ..engine.rules import GameRules, MatchState
from ..agents.apex_grandmaster_agent import ApexGrandmasterAgent
from ..agents.base import BaseAgent
from ..persistence.db import ExperienceDB
from ..knowledge.exporter import ObsidianExporter


class InteractiveGameRunner:
    """Interactive console game runner allowing a human player to duel the Apex Grandmaster AI."""

    def __init__(self, db: Optional[ExperienceDB] = None):
        self.db = db

    def play_1v1_human_match(self, total_rounds: int = 5) -> None:
        print("\n" + "=" * 70)
        print("          JAWAKER HAND (هاند جواكر) - HUMAN vs APEX AI DUEL         ")
        print("=" * 70)
        print("Welcome! You are Player 0 (Human). You will duel the Apex Grandmaster AI (Player 1).")
        print(f"Match format: {total_rounds} competitive rounds. Lowest cumulative points wins!\n")

        ai_agent = ApexGrandmasterAgent(name="Apex_Grandmaster", player_id=1, iterations=45)
        match_state = MatchState(
            num_players=2,
            rules=GameRules(total_rounds=total_rounds),
            player_names={0: "You (Human)", 1: "Apex_Grandmaster_AI"}
        )

        match_id = f"human_match_{int(time.time())}"

        for r_num in range(1, total_rounds + 1):
            dealer_id = match_state.current_dealer
            dealer_str = "You (Human)" if dealer_id == 0 else "Apex AI"
            print("\n" + "#" * 70)
            print(f"                  ROUND {r_num} OF {total_rounds} (Dealer: {dealer_str})")
            print("#" * 70 + "\n")

            state = GameState.deal_new_round(num_players=2, dealer=dealer_id)
            ai_agent.reset_round()

            while not state.is_round_over:
                curr_p = state.current_player
                if curr_p == 0:
                    self._handle_human_turn(state)
                else:
                    self._handle_ai_turn(state, ai_agent)

            # Round finished
            res = state.round_result
            if res is not None:
                match_state.record_round_result(res)
                if self.db is not None:
                    self.db.save_round(match_id, r_num, dealer_id, res)

                print("\n" + "-" * 70)
                print(f"★ ROUND {r_num} FINISHED ★")
                print(res.score_breakdown)
                print(f"Current Cumulative Standings:")
                for p, score in match_state.cumulative_scores.items():
                    p_name = "You (Human)" if p == 0 else "Apex AI"
                    print(f"  {p_name}: {score:+d} pts")
                print("-" * 70)

                input("\nPress Enter to continue to next round...")

        # Match complete
        summary = match_state.get_final_summary()
        if self.db is not None:
            self.db.save_match(match_id, 2, summary)

        print("\n" + "=" * 70)
        print("                 🏆 FINAL 5-ROUND MATCH RESULTS 🏆                 ")
        print("=" * 70)
        print(summary.summary_text)
        print("=" * 70 + "\n")

        if self.db is not None:
            exporter = ObsidianExporter(db=self.db)
            exporter.export_vault()
            print("[+] Match record exported to your Obsidian Knowledge Vault!")

    def _display_human_view(self, state: GameState) -> None:
        view = state.get_player_view(0)
        print("\n" + "─" * 65)
        print(f"Turn {state.turn_number:02d} | Phase: {state.phase.value} | Stock: {len(state.stock)} cards | AI Hand: {len(state.hands[1])} cards")
        
        top_d = state.discard_pile[-1].to_str(show_deck=False) if state.discard_pile else "Empty"
        print(f"Fire Pile Top: [{top_d}]")

        if state.table.melds:
            table_strs = " | ".join(f"#{tm.meld_id}: {tm.meld.to_str()}" for tm in state.table.melds)
            print(f"Table Board: {table_strs}")
        else:
            print("Table Board: (No melds open yet)")

        print("\nYour Hand:")
        hand_items = [f"[{idx+1}] {c.to_str(show_deck=False)}" for idx, c in enumerate(view.hand)]
        # Print in lines of 7
        for i in range(0, len(hand_items), 7):
            print("  " + "  ".join(hand_items[i:i+7]))
        
        status_open = "OPENED (نزلت)" if view.am_i_opened else "NOT OPENED (لم تنزل بعد - بحاجة لـ 51 نقطة)"
        print(f"Status: {status_open}")
        print("─" * 65)

    def _handle_human_turn(self, state: GameState) -> None:
        self._display_human_view(state)
        legal_actions = state.get_legal_actions()

        if not legal_actions:
            return

        if state.phase == TurnPhase.DRAW:
            top_d = state.discard_pile[-1].to_str(show_deck=False) if state.discard_pile else "None"
            can_draw_discard = any(a.action_type == ActionType.DRAW_DISCARD for a in legal_actions)

            print("\n[DRAW PHASE] Choose action:")
            print("  (1) Draw from Stock Deck (Face Down)")
            if can_draw_discard:
                print(f"  (2) Draw from Fire Pile [{top_d}]")

            while True:
                choice = input("Enter choice (1 or 2): ").strip()
                if choice == "1":
                    state.apply_action(Action.draw_stock())
                    print("-> You drew from Stock Deck.")
                    break
                elif choice == "2" and can_draw_discard:
                    state.apply_action(Action.draw_discard())
                    print(f"-> You drew [{top_d}] from Fire Pile.")
                    break
                else:
                    print("Invalid choice. Try again.")

        elif state.phase == TurnPhase.MELD:
            while state.phase == TurnPhase.MELD:
                legal = state.get_legal_actions()
                print("\n[MELD PHASE] Available actions:")
                actions_map = {}
                idx = 1
                for a in legal:
                    actions_map[idx] = a
                    print(f"  ({idx}) {a.to_str()}")
                    idx += 1

                while True:
                    choice = input(f"Enter choice (1-{len(actions_map)}): ").strip()
                    if choice.isdigit() and int(choice) in actions_map:
                        chosen_act = actions_map[int(choice)]
                        state.apply_action(chosen_act)
                        print(f"-> Action executed: {chosen_act.to_str()}")
                        break
                    else:
                        print("Invalid choice. Try again.")

                if state.phase != TurnPhase.MELD:
                    break

        elif state.phase == TurnPhase.DISCARD:
            hand = state.hands[0]
            print("\n[DISCARD PHASE] Enter the number of the card you wish to discard:")
            for idx, c in enumerate(hand):
                print(f"  [{idx+1}] {c.to_str(show_deck=False)}", end="  ")
                if (idx + 1) % 7 == 0:
                    print()
            print()

            while True:
                choice = input(f"Enter card number [1-{len(hand)}]: ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(hand):
                    card_to_discard = hand[int(choice) - 1]
                    state.apply_action(Action.discard(card_to_discard))
                    print(f"-> You discarded: {card_to_discard.to_str(show_deck=False)}")
                    break
                else:
                    print("Invalid card number. Try again.")

    def _handle_ai_turn(self, state: GameState, agent: BaseAgent) -> None:
        view = state.get_player_view(state.current_player)
        legal = state.get_legal_actions()
        if not legal:
            return

        act, trace = agent.select_action(view, legal)
        print(f"\n[AI Turn {state.turn_number:02d}] {agent.name} played: {act.to_str()} ({trace.execution_latency_ms:.1f}ms)")
        state.apply_action(act)
