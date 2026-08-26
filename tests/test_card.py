"""Unit tests for 106-card deck structure and point valuations in Jawaker Hand."""

import pytest
from jawaker_hand_ai.engine.card import Card, Suit, Rank, ALL_CARDS


def test_deck_composition():
    assert len(ALL_CARDS) == 106
    # Deck 0
    for i in range(52):
        c = ALL_CARDS[i]
        assert c.deck_index == 0
        assert not c.is_joker
    # Deck 1
    for i in range(52, 104):
        c = ALL_CARDS[i]
        assert c.deck_index == 1
        assert not c.is_joker
    # Jokers
    assert ALL_CARDS[104].is_joker
    assert ALL_CARDS[105].is_joker


def test_hand_penalty_valuation():
    # Ace in hand = 11 pts
    ace = Card.create_standard(Rank.ACE, Suit.HEARTS, deck_index=0)
    assert ace.hand_penalty_value == 11

    # Joker in hand = 15 pts
    joker = Card.create_joker(0)
    assert joker.hand_penalty_value == 15

    # Face cards = 10 pts
    king = Card.create_standard(Rank.KING, Suit.SPADES)
    queen = Card.create_standard(Rank.QUEEN, Suit.CLUBS)
    ten = Card.create_standard(Rank.TEN, Suit.DIAMONDS)
    assert king.hand_penalty_value == 10
    assert queen.hand_penalty_value == 10
    assert ten.hand_penalty_value == 10

    # 2..9 = face value
    seven = Card.create_standard(Rank.SEVEN, Suit.HEARTS)
    two = Card.create_standard(Rank.TWO, Suit.CLUBS)
    assert seven.hand_penalty_value == 7
    assert two.hand_penalty_value == 2


def test_card_string_parsing():
    c1 = Card.from_str("7H")
    assert c1.rank == Rank.SEVEN and c1.suit == Suit.HEARTS

    c2 = Card.from_str("AS#1")
    assert c2.rank == Rank.ACE and c2.suit == Suit.SPADES and c2.deck_index == 1

    c3 = Card.from_str("10D")
    assert c3.rank == Rank.TEN and c3.suit == Suit.DIAMONDS

    c4 = Card.from_str("JK1")
    assert c4.is_joker and c4.id == 104
