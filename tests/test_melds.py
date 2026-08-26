"""Unit tests for meld validation, point rules (Ace=11 vs Ace=1 in A-2-3), Sets, Runs, Jokers, and 51-pt solver."""

import pytest
from jawaker_hand_ai.engine.card import Card, Suit, Rank
from jawaker_hand_ai.engine.melds import (
    validate_set, validate_run, validate_meld,
    find_valid_opening_melds, find_best_meld_partition,
    MeldType
)


def test_valid_sets():
    # 3-card set: 7S, 7H, 7D
    s1 = [
        Card.create_standard(Rank.SEVEN, Suit.SPADES),
        Card.create_standard(Rank.SEVEN, Suit.HEARTS),
        Card.create_standard(Rank.SEVEN, Suit.DIAMONDS)
    ]
    m1 = validate_set(s1)
    assert m1 is not None
    assert m1.type == MeldType.SET
    assert m1.points == 21  # 7 + 7 + 7

    # 4-card set: 10S, 10H, 10D, 10C
    s2 = [
        Card.create_standard(Rank.TEN, Suit.SPADES),
        Card.create_standard(Rank.TEN, Suit.HEARTS),
        Card.create_standard(Rank.TEN, Suit.DIAMONDS),
        Card.create_standard(Rank.TEN, Suit.CLUBS)
    ]
    m2 = validate_set(s2)
    assert m2 is not None
    assert m2.points == 40

    # 3 Aces set: A = 11 pts each -> 33 pts!
    s3 = [
        Card.create_standard(Rank.ACE, Suit.SPADES),
        Card.create_standard(Rank.ACE, Suit.HEARTS),
        Card.create_standard(Rank.ACE, Suit.CLUBS)
    ]
    m3 = validate_set(s3)
    assert m3 is not None
    assert m3.points == 33

    # Set with Joker: K(S), K(H), Joker -> 30 pts
    s4 = [
        Card.create_standard(Rank.KING, Suit.SPADES),
        Card.create_standard(Rank.KING, Suit.HEARTS),
        Card.create_joker(0)
    ]
    m4 = validate_set(s4)
    assert m4 is not None
    assert m4.points == 30


def test_invalid_sets():
    # Duplicate suit in set (forbidden even with 2 decks)
    s_dup = [
        Card.create_standard(Rank.SEVEN, Suit.SPADES, deck_index=0),
        Card.create_standard(Rank.SEVEN, Suit.SPADES, deck_index=1),
        Card.create_standard(Rank.SEVEN, Suit.HEARTS, deck_index=0)
    ]
    assert validate_set(s_dup) is None

    # Mismatched ranks
    s_mis = [
        Card.create_standard(Rank.SEVEN, Suit.SPADES),
        Card.create_standard(Rank.EIGHT, Suit.HEARTS),
        Card.create_standard(Rank.SEVEN, Suit.DIAMONDS)
    ]
    assert validate_set(s_mis) is None


def test_valid_runs_and_ace_valuation():
    # Ace Low run: A-2-3 -> Ace = 1 pt -> Total = 1 + 2 + 3 = 6 pts
    r_low_ace = [
        Card.create_standard(Rank.ACE, Suit.HEARTS),
        Card.create_standard(Rank.TWO, Suit.HEARTS),
        Card.create_standard(Rank.THREE, Suit.HEARTS)
    ]
    m_low = validate_run(r_low_ace)
    assert m_low is not None
    assert m_low.points == 6

    # Ace High run: J-Q-K-A -> Ace = 11 pts -> Total = 10 + 10 + 10 + 11 = 41 pts!
    r_high_ace = [
        Card.create_standard(Rank.JACK, Suit.SPADES),
        Card.create_standard(Rank.QUEEN, Suit.SPADES),
        Card.create_standard(Rank.KING, Suit.SPADES),
        Card.create_standard(Rank.ACE, Suit.SPADES)
    ]
    m_high = validate_run(r_high_ace)
    assert m_high is not None
    assert m_high.points == 41

    # Run with Joker: 8D, Joker(9D), 10D -> Total = 8 + 9 + 10 = 27 pts
    r_jk = [
        Card.create_standard(Rank.EIGHT, Suit.DIAMONDS),
        Card.create_joker(0),
        Card.create_standard(Rank.TEN, Suit.DIAMONDS)
    ]
    m_jk = validate_run(r_jk)
    assert m_jk is not None
    assert m_jk.points == 27


def test_initial_51_points_opening():
    # Hand with A-A-A (33 pts) + K-K-K (30 pts) = 63 pts (>= 51)
    hand_63 = [
        Card.create_standard(Rank.ACE, Suit.SPADES),
        Card.create_standard(Rank.ACE, Suit.HEARTS),
        Card.create_standard(Rank.ACE, Suit.DIAMONDS),
        Card.create_standard(Rank.KING, Suit.SPADES),
        Card.create_standard(Rank.KING, Suit.HEARTS),
        Card.create_standard(Rank.KING, Suit.CLUBS),
        Card.create_standard(Rank.TWO, Suit.CLUBS),
        Card.create_standard(Rank.THREE, Suit.DIAMONDS)
    ]
    openings = find_valid_opening_melds(hand_63)
    assert len(openings) > 0
    assert any(o.total_points >= 51 for o in openings)

    # Hand with only 7-8-9 (24 pts) + 4-5-6 (15 pts) = 39 pts (< 51)
    hand_39 = [
        Card.create_standard(Rank.SEVEN, Suit.HEARTS),
        Card.create_standard(Rank.EIGHT, Suit.HEARTS),
        Card.create_standard(Rank.NINE, Suit.HEARTS),
        Card.create_standard(Rank.FOUR, Suit.CLUBS),
        Card.create_standard(Rank.FIVE, Suit.CLUBS),
        Card.create_standard(Rank.SIX, Suit.CLUBS),
        Card.create_standard(Rank.TWO, Suit.SPADES)
    ]
    openings_39 = find_valid_opening_melds(hand_39)
    assert len(openings_39) == 0  # Cannot open with < 51 pts!
