"""Unit tests for WebSocket server bridge and Godot 4 JSON serialization."""

import pytest
import asyncio
import json
from jawaker_hand_ai.engine.state import GameState
from jawaker_hand_ai.server.bridge import player_view_to_dict, round_result_to_dict
from jawaker_hand_ai.server.server import GameSession


def test_bridge_state_serialization():
    state = GameState.deal_new_round(num_players=2, dealer=0)
    legal = state.get_legal_actions()
    view = state.get_player_view(0)

    data = player_view_to_dict(view, legal)
    assert data["player_id"] == 0
    assert len(data["hand"]) in (14, 15)
    assert "stock_count" in data
    assert "legal_actions" in data
    assert len(data["legal_actions"]) == len(legal)

    # Validate JSON serializability
    json_str = json.dumps(data)
    assert len(json_str) > 50


def test_game_session_progression():
    session = GameSession(num_players=2)
    session.start_new_match()
    assert session.state is not None
    assert session.match_state is not None
    assert session.state.num_players == 2
