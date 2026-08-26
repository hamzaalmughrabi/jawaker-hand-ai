"""Strategic heuristic agent balancing 51-pt opening, Hand finishes, and discard safety."""

from __future__ import annotations
import time
from typing import Sequence
from .base import BaseAgent
from ..engine.state import PlayerView, TurnPhase
from ..engine.actions import Action, ActionType
from ..engine.melds import find_best_meld_partition
from ..opponent.belief import BayesianBeliefModel
from ..persistence.trace import DecisionTrace, ActionEvaluation


class HeuristicAgent(BaseAgent):
    """Strategic AI agent incorporating Hand-vs-Open valuation and discard safety calculations."""

    def __init__(self, name: str = "HeuristicAgent", player_id: int = 0):
        super().__init__(name, player_id)
        self.belief: BayesianBeliefModel = BayesianBeliefModel(player_id, 4)

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        # Update opponent belief
        if self.belief.num_players != view.num_players:
            self.belief = BayesianBeliefModel(self.player_id, view.num_players)
        self.belief.update_from_view(view)

        evaluations: list[ActionEvaluation] = []
        best_action = legal_actions[0]
        best_score = -float("inf")

        for action in legal_actions:
            score, heuristics = self._evaluate_action(view, action)
            evaluations.append(ActionEvaluation(
                action_str=action.to_str(),
                q_value=score,
                heuristics=heuristics
            ))
            if score > best_score:
                best_score = score
                best_action = action

        latency = (time.perf_counter() - t0) * 1000.0
        belief_summary = self.belief.get_summary()
        trace = self._create_trace(view, best_action, evaluations, latency, belief_summary)
        return best_action, trace

    def _evaluate_action(self, view: PlayerView, action: Action) -> tuple[float, dict[str, float]]:
        heuristics: dict[str, float] = {}

        if action.action_type == ActionType.DRAW_DISCARD:
            return 120.0, {"draw_priority": 120.0}

        elif action.action_type == ActionType.DRAW_STOCK:
            return 60.0, {"draw_priority": 60.0}

        elif action.action_type == ActionType.INITIAL_MELD:
            # Check if we should hold for "Hand" finish
            # Conditions to hold: No opponent opened yet AND we have >= 12 melded cards
            any_opp_opened = any(view.player_is_opened[opp] for opp in range(view.num_players) if opp != self.player_id)
            opp_min_cards = min(view.player_hand_counts[opp] for opp in range(view.num_players) if opp != self.player_id)

            best_part = view.best_meld_partition
            total_melded_cards = len(best_part.used_card_ids)

            pts = sum(m.points for m in action.melds) if action.melds else 0

            if not any_opp_opened and opp_min_cards > 8 and total_melded_cards >= 13:
                # High chance of going Hand in 1-2 turns! Suppress early opening
                heuristics["hand_ambition"] = -200.0
                return -50.0, heuristics

            # Otherwise, open to avoid unopened 100-pt penalty!
            score = 600.0 + pts
            heuristics["open_urgency"] = 600.0
            heuristics["meld_points"] = float(pts)
            return score, heuristics

        elif action.action_type == ActionType.SWAP_JOKER:
            return 450.0, {"swap_joker": 450.0}

        elif action.action_type == ActionType.ATTACH_CARD:
            pts = action.card.hand_penalty_value if action.card else 10
            return 350.0 + pts, {"attachment_pts": float(pts)}

        elif action.action_type == ActionType.LAY_MELD:
            pts = sum(m.points for m in action.melds) if action.melds else 0
            return 250.0 + pts, {"lay_meld_pts": float(pts)}

        elif action.action_type == ActionType.PASS_MELD:
            return 0.0, {"pass": 0.0}

        elif action.action_type == ActionType.DISCARD:
            card = action.card
            if card is None:
                return 0.0, {}

            best_part = view.best_meld_partition
            is_melded = card.id in best_part.used_card_ids

            # Discard safety calculation
            # Check if card can attach to any table meld (DANGEROUS if opponent has opened)
            table_attach_danger = 0.0
            for tm in view.table.melds:
                if view.table.can_attach_card(card, tm.meld_id) is not None:
                    table_attach_danger += 40.0

            # Card penalty value
            penalty_val = float(card.hand_penalty_value)

            # High score for discarding unmelded, safe, high-penalty cards
            base_score = 100.0 if not is_melded else -100.0
            safety_score = base_score + (penalty_val * 2.0) - table_attach_danger

            heuristics["is_unmelded"] = 1.0 if not is_melded else 0.0
            heuristics["penalty_val"] = penalty_val
            heuristics["table_attach_danger"] = table_attach_danger

            return safety_score, heuristics

        return 0.0, {}
