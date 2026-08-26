"""Unit tests for Jawaker Hand game state transitions, dealing, Hand vs Normal finish, and penalties."""

import pytest
import random
from jawaker_hand_ai.engine.card import Card, Suit, Rank
from jawaker_hand_ai.engine.state import GameState, TurnPhase
from jawaker_hand_ai.engine.actions import Action
from jawaker_hand_ai.engine.melds import validate_set, validate_run


def test_dealing_and_first_player():
    state = GameState.deal_new_round(num_players=4, dealer=0, rng=random.Random(42))
    # Player 1 (dealer + 1) has 15 cards
    assert len(state.hands[1]) == 15
    # Other players have 14 cards
    assert len(state.hands[0]) == 14
    assert len(state.hands[2]) == 14
    assert len(state.hands[3]) == 14

    # First player starts in DISCARD phase
    assert state.current_player == 1
    assert state.phase == TurnPhase.DISCARD

    # First player discards 1 card
    card_to_discard = state.hands[1][0]
    state.apply_action(Action.discard(card_to_discard))

    # After first discard: hand has 14 cards, turn goes to Player 2 in DRAW phase
    assert len(state.hands[1]) == 14
    assert state.current_player == 2
    assert state.phase == TurnPhase.DRAW


def test_normal_finish_and_unopened_penalties():
    state = GameState.deal_new_round(num_players=4, dealer=0)

    # Set player 0 with an already opened state
    state.is_opened[0] = True
    state.opened_turn[0] = 1

    # Player 0 has 1 card left
    discard_card = Card.create_standard(Rank.TWO, Suit.HEARTS)
    state.hands[0] = [discard_card]
    state.current_player = 0
    state.phase = TurnPhase.DISCARD
    state.turn_number = 10

    # Other players: P1 opened (holds King=10), P2 and P3 unopened (holds 14 cards)
    state.is_opened[1] = True
    state.hands[1] = [Card.create_standard(Rank.KING, Suit.SPADES)]
    state.is_opened[2] = False
    state.is_opened[3] = False

    # Player 0 discards final card -> Normal finish!
    state.apply_action(Action.discard(discard_card))

    assert state.is_round_over
    res = state.round_result
    assert res is not None
    assert res.winner_id == 0
    assert res.is_normal_finish
    assert not res.is_hand_finish

    # Winner gets -30
    assert res.round_scores[0] == -30
    # Opened loser P1 gets hand penalty (King = 10 pts)
    assert res.round_scores[1] == 10
    # Unopened losers P2 and P3 get +100 penalty
    assert res.round_scores[2] == 100
    assert res.round_scores[3] == 100


def test_hand_finish_doubled_penalties():
    state = GameState.deal_new_round(num_players=4, dealer=0)

    # Player 0 opens and finishes in the EXACT SAME turn (Hand finish!)
    state.current_player = 0
    state.phase = TurnPhase.DISCARD
    state.turn_number = 5
    state.is_opened[0] = True
    state.opened_turn[0] = 5  # opened on turn 5 and finishing on turn 5!

    discard_card = Card.create_standard(Rank.TWO, Suit.HEARTS)
    state.hands[0] = [discard_card]

    # Other players: P1 opened (King=10), P2 unopened
    state.is_opened[1] = True
    state.hands[1] = [Card.create_standard(Rank.KING, Suit.SPADES)]
    state.is_opened[2] = False
    state.is_opened[3] = False

    state.apply_action(Action.discard(discard_card))

    assert state.is_round_over
    res = state.round_result
    assert res.is_hand_finish

    # Winner gets -60 pts on Hand finish
    assert res.round_scores[0] == -60
    # Opened loser P1 gets doubled penalty (10 * 2 = 20 pts)
    assert res.round_scores[1] == 20
    # Unopened losers P2 and P3 get doubled unopened penalty (+200 pts)
    assert res.round_scores[2] == 200
    assert res.round_scores[3] == 200
