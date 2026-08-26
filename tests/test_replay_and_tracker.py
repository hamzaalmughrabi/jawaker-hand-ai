"""Unit tests for the Replay Viewer, Human Session Tracker, and Discard Draw rule."""

import pytest
from jawaker_hand_ai.engine.card import ALL_CARDS, Card, Suit, Rank
from jawaker_hand_ai.engine.actions import Action, ActionType
from jawaker_hand_ai.engine.state import GameState, TurnPhase
from jawaker_hand_ai.engine.melds import validate_run, validate_set, MeldType
from jawaker_hand_ai.persistence.session_tracker import HumanSessionTracker
from jawaker_hand_ai.cli.replay import ReplayViewer


def test_session_tracker(tmp_path):
    db_path = tmp_path / "test_session.db"
    tracker = HumanSessionTracker(db_path=db_path)

    r_id = tracker.record_match(winner="Hamza", human_score=-30, ai_score=45, rounds=5, notes="AI held Jokers too long")
    assert r_id == 1

    records = tracker.get_all_records()
    assert len(records) == 1
    assert records[0].winner == "Hamza"
    assert records[0].human_score == -30

    report = tracker.print_leaderboard()
    assert "Hamza Wins" in report
    assert "100.0%" in report


def test_discard_draw_rule_must_meld():
    """Test that a player drawing from discard cannot PASS_MELD without melding that card."""
    from jawaker_hand_ai.engine.card import Card, Rank, Suit
    state = GameState.deal_new_round(num_players=2)
    state.phase = TurnPhase.DRAW
    state.current_player = 0

    top_c = Card.create_standard(Rank.KING, Suit.HEARTS)
    state.discard_pile = [top_c]

    # Give player 0 a hand that can open with top_c (King of Hearts)
    state.hands[0] = [
        Card.create_standard(Rank.KING, Suit.DIAMONDS),
        Card.create_standard(Rank.KING, Suit.CLUBS),
        Card.create_standard(Rank.TEN, Suit.SPADES),
        Card.create_standard(Rank.JACK, Suit.SPADES),
        Card.create_standard(Rank.QUEEN, Suit.SPADES),
        Card.create_standard(Rank.TWO, Suit.HEARTS),
    ]

    assert state.can_player_draw_discard(0)
    state.apply_action(Action.draw_discard())
    assert state.phase == TurnPhase.MELD
    assert state.drawn_from_discard_this_turn == top_c

    # Legal actions should only contain INITIAL_MELD (no PASS_MELD)
    legal = state.get_legal_actions()
    assert not any(act.action_type == ActionType.PASS_MELD for act in legal)

    # Trying to pass meld illegally raises ValueError
    with pytest.raises(ValueError, match="Cannot pass meld"):
        state.apply_action(Action.pass_meld())
