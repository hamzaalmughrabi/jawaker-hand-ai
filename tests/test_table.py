"""Unit tests for table melds, card attachments, and Joker substitutions."""

import pytest
from jawaker_hand_ai.engine.card import Card, Suit, Rank
from jawaker_hand_ai.engine.melds import validate_run, validate_set
from jawaker_hand_ai.engine.table import TableState


def test_table_card_attachment():
    table = TableState()

    # Place a run: 4H-5H-6H
    r1 = validate_run([
        Card.create_standard(Rank.FOUR, Suit.HEARTS),
        Card.create_standard(Rank.FIVE, Suit.HEARTS),
        Card.create_standard(Rank.SIX, Suit.HEARTS)
    ])
    m_id = table.add_meld(player_id=0, meld=r1)

    # Attach 7H (high end)
    card_7h = Card.create_standard(Rank.SEVEN, Suit.HEARTS)
    assert table.can_attach_card(card_7h, m_id) is not None
    updated = table.attach_card(player_id=1, card=card_7h, meld_id=m_id)
    assert len(updated.cards) == 4
    assert updated.points == 4 + 5 + 6 + 7

    # Attach 3H (low end)
    card_3h = Card.create_standard(Rank.THREE, Suit.HEARTS)
    assert table.can_attach_card(card_3h, m_id) is not None
    updated_2 = table.attach_card(player_id=2, card=card_3h, meld_id=m_id)
    assert len(updated_2.cards) == 5


def test_joker_substitution():
    table = TableState()

    # Place a run with Joker: 8D - Joker(9D) - 10D
    joker = Card.create_joker(0)
    r_jk = validate_run([
        Card.create_standard(Rank.EIGHT, Suit.DIAMONDS),
        joker,
        Card.create_standard(Rank.TEN, Suit.DIAMONDS)
    ])
    m_id = table.add_meld(player_id=0, meld=r_jk)

    # Natural 9D can replace Joker
    natural_9d = Card.create_standard(Rank.NINE, Suit.DIAMONDS)
    assert table.can_swap_joker(natural_9d, m_id, joker)

    # Swap Joker!
    liberated_joker = table.swap_joker(player_id=1, natural_card=natural_9d, meld_id=m_id, joker_card=joker)
    assert liberated_joker.id == joker.id

    # Table meld is now pure naturals 8D-9D-10D
    tm = table.get_table_meld(m_id)
    assert not tm.meld.contains_joker
    assert tm.meld.points == 8 + 9 + 10
