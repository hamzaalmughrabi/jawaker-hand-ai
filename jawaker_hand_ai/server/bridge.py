"""State and action serializer bridging the Python engine with the Godot 4 client."""

from __future__ import annotations
from typing import Optional, Any
from ..engine.card import Card, Suit, Rank
from ..engine.melds import Meld, MeldType
from ..engine.table import TableState, TableMeld
from ..engine.actions import Action, ActionType
from ..engine.state import GameState, TurnPhase, PlayerView, RoundScoreResult


def card_to_dict(card: Card) -> dict[str, Any]:
    """Convert a Card object to a JSON-serializable dictionary for Godot."""
    if card.is_joker:
        return {
            "id": card.id,
            "rank": 0,
            "rank_str": "JK",
            "suit": "JOKER",
            "suit_char": "JK",
            "deck": card.deck_index,
            "is_joker": True,
            "penalty_value": card.hand_penalty_value,
            "display": card.to_str(show_deck=False),
            "display_full": card.to_str(show_deck=True)
        }
    rank_str = "10" if card.rank == Rank.TEN else (card.rank.char if card.rank is not None else "")
    suit_name = card.suit.name if card.suit is not None else ""
    suit_char = card.suit.char if card.suit is not None else ""
    return {
        "id": card.id,
        "rank": card.rank.value if card.rank is not None else 0,
        "rank_str": rank_str,
        "suit": suit_name,
        "suit_char": suit_char,
        "deck": card.deck_index,
        "is_joker": False,
        "penalty_value": card.hand_penalty_value,
        "display": f"{rank_str}{suit_char}" if suit_char else rank_str,
        "display_full": card.to_str(show_deck=True)
    }


def meld_to_dict(meld: Meld) -> dict[str, Any]:
    """Convert a Meld object to a JSON-serializable dictionary."""
    rep_list = []
    for r, s in zip(meld.represented_ranks, meld.represented_suits):
        r_str = "10" if r == Rank.TEN else r.char
        rep_list.append({"rank": r.value, "rank_char": r_str, "suit": s.name, "suit_char": s.char})

    return {
        "type": meld.type.value,
        "points": meld.points,
        "cards": [card_to_dict(c) for c in meld.cards],
        "card_ids": [c.id for c in meld.cards],
        "represented": rep_list,
        "display": meld.to_str()
    }


def table_meld_to_dict(tm: TableMeld) -> dict[str, Any]:
    """Convert a TableMeld object to a JSON-serializable dictionary."""
    return {
        "meld_id": tm.meld_id,
        "owner_id": tm.owner_id,
        "meld": meld_to_dict(tm.meld)
    }


def action_to_dict(action: Action, action_index: int) -> dict[str, Any]:
    """Convert an Action object to a JSON-serializable dictionary."""
    data: dict[str, Any] = {
        "index": action_index,
        "type": action.action_type.value,
        "display": action.to_str(),
        "card": card_to_dict(action.card) if action.card is not None else None,
        "meld_id": action.meld_id,
        "melds": [meld_to_dict(m) for m in action.melds] if action.melds else [],
        "target_joker": card_to_dict(action.target_joker) if action.target_joker is not None else None
    }
    return data


def player_view_to_dict(view: PlayerView, legal_actions: list[Action]) -> dict[str, Any]:
    """Compile the complete state view for the Godot client including detected hand combos."""
    table_melds = [table_meld_to_dict(tm) for tm in view.table.melds]

    # Detect combos/melds in the player's current hand
    partition = view.best_meld_partition
    melds = partition.melds
    meld_points = partition.total_points

    detected_combos = []
    for c_idx, m in enumerate(melds):
        detected_combos.append({
            "combo_id": c_idx,
            "type": m.type.value,
            "points": m.points,
            "card_ids": [c.id for c in m.cards],
            "display": m.to_str()
        })

    return {
        "player_id": view.player_id,
        "num_players": view.num_players,
        "turn_number": view.turn_number,
        "current_player": view.current_player,
        "phase": view.phase.value,
        "is_my_turn": view.is_my_turn,
        "am_i_opened": view.am_i_opened,
        "hand": [card_to_dict(c) for c in view.hand],
        "hand_combos": detected_combos,
        "hand_meld_points": meld_points,
        "hand_counts": view.player_hand_counts,
        "is_opened": view.player_is_opened,
        "stock_count": view.stock_count,
        "top_discard": card_to_dict(view.top_discard) if view.top_discard is not None else None,
        "discard_count": len(view.discard_pile),
        "table_melds": table_melds,
        "legal_actions": [action_to_dict(act, idx) for idx, act in enumerate(legal_actions)]
    }


def round_result_to_dict(res: RoundScoreResult, player_names: dict[int, str]) -> dict[str, Any]:
    """Convert RoundScoreResult to JSON-serializable dictionary for round end screen."""
    return {
        "winner_id": res.winner_id,
        "winner_name": player_names.get(res.winner_id, f"Player {res.winner_id}") if res.winner_id is not None else "Draw",
        "is_hand_finish": res.is_hand_finish,
        "is_normal_finish": res.is_normal_finish,
        "is_stock_exhausted": res.is_stock_exhausted,
        "round_scores": res.round_scores,
        "unopened_players": list(res.unopened_players),
        "score_breakdown": res.score_breakdown
    }


def trace_to_dict(trace: Any) -> dict[str, Any]:
    """Convert DecisionTrace to JSON dictionary for the in-game AI Lab Inspector."""
    evals = []
    for e in trace.candidate_evaluations:
        evals.append({
            "action": e.action_str,
            "q_value": round(float(e.q_value), 3),
            "probability": round(float(e.probability), 3),
            "visit_count": int(e.visit_count)
        })
    # Sort evals by q_value descending
    evals.sort(key=lambda x: x["q_value"], reverse=True)

    return {
        "trace_id": trace.trace_id,
        "match_id": trace.match_id,
        "round_number": trace.round_number,
        "turn_number": trace.turn_number,
        "player_id": trace.player_id,
        "agent_name": trace.agent_name,
        "phase": trace.phase,
        "hand_cards": trace.hand_cards,
        "is_opened": trace.is_opened,
        "selected_action": trace.selected_action,
        "candidate_evaluations": evals,
        "latency_ms": round(float(trace.execution_latency_ms), 1),
        "created_at": trace.created_at
    }

