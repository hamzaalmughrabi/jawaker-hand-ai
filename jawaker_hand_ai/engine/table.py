"""Table state management: public melds on board, card attachments/layoffs, and Joker substitutions."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Sequence
from .card import Card, Suit, Rank
from .melds import Meld, MeldType, validate_set, validate_run, validate_meld


@dataclass
class TableMeld:
    """A public meld placed on the table."""
    meld_id: int
    owner_id: int
    meld: Meld

    def clone(self) -> TableMeld:
        return TableMeld(
            meld_id=self.meld_id,
            owner_id=self.owner_id,
            meld=self.meld
        )


@dataclass
class TableState:
    """The collective table board holding all melds laid down by opened players."""
    melds: list[TableMeld] = field(default_factory=list)
    next_meld_id: int = 1

    def clone(self) -> TableState:
        return TableState(
            melds=[m.clone() for m in self.melds],
            next_meld_id=self.next_meld_id
        )

    def add_meld(self, player_id: int, meld: Meld) -> int:
        """Place a newly laid down meld onto the table."""
        m_id = self.next_meld_id
        self.next_meld_id += 1
        self.melds.append(TableMeld(meld_id=m_id, owner_id=player_id, meld=meld))
        return m_id

    def get_table_meld(self, meld_id: int) -> Optional[TableMeld]:
        for tm in self.melds:
            if tm.meld_id == meld_id:
                return tm
        return None

    def can_attach_card(self, card: Card, meld_id: int) -> Optional[Meld]:
        """Check if `card` can be legally attached to table meld `meld_id` to extend it."""
        tm = self.get_table_meld(meld_id)
        if tm is None:
            return None

        current_cards = list(tm.meld.cards)
        candidate_cards = current_cards + [card]

        if tm.meld.type == MeldType.SET:
            return validate_set(candidate_cards)
        elif tm.meld.type == MeldType.RUN:
            return validate_run(candidate_cards)

        return None

    def attach_card(self, player_id: int, card: Card, meld_id: int) -> Meld:
        """Attach a card to an existing table meld."""
        tm = self.get_table_meld(meld_id)
        if tm is None:
            raise ValueError(f"Table meld {meld_id} not found.")

        new_meld = self.can_attach_card(card, meld_id)
        if new_meld is None:
            raise ValueError(f"Card {card} cannot be legally attached to meld {tm.meld}.")

        tm.meld = new_meld
        return new_meld

    def can_swap_joker(self, natural_card: Card, meld_id: int, joker_card: Card) -> bool:
        """Check if `natural_card` can replace `joker_card` in table meld `meld_id`."""
        if natural_card.is_joker or not joker_card.is_joker:
            return False

        tm = self.get_table_meld(meld_id)
        if tm is None:
            return False

        rep = tm.meld.get_joker_represented_card(joker_card)
        if rep is None:
            return False

        rep_rank, rep_suit = rep
        return natural_card.rank == rep_rank and natural_card.suit == rep_suit

    def swap_joker(self, player_id: int, natural_card: Card, meld_id: int, joker_card: Card) -> Card:
        """Replace `joker_card` with `natural_card` in table meld `meld_id`, returning the Joker."""
        tm = self.get_table_meld(meld_id)
        if tm is None:
            raise ValueError(f"Table meld {meld_id} not found.")

        if not self.can_swap_joker(natural_card, meld_id, joker_card):
            raise ValueError(f"Cannot swap Joker {joker_card} with {natural_card} in {tm.meld}")

        # Replace joker in cards list
        new_cards = [natural_card if c.id == joker_card.id else c for c in tm.meld.cards]
        validated = validate_meld(new_cards)
        if validated is None:
            raise ValueError(f"Meld invalid after Joker swap: {new_cards}")

        tm.meld = validated
        return joker_card

    def get_all_attachment_options(self, hand: Sequence[Card]) -> list[tuple[Card, int, Meld]]:
        """Find all (card, meld_id, new_meld) combinations from hand onto table."""
        options: list[tuple[Card, int, Meld]] = []
        for card in hand:
            for tm in self.melds:
                extended = self.can_attach_card(card, tm.meld_id)
                if extended is not None:
                    options.append((card, tm.meld_id, extended))
        return options

    def get_all_joker_swap_options(self, hand: Sequence[Card]) -> list[tuple[Card, int, Card]]:
        """Find all (natural_card, meld_id, joker_card) substitution opportunities."""
        options: list[tuple[Card, int, Card]] = []
        for natural_card in hand:
            if natural_card.is_joker:
                continue
            for tm in self.melds:
                for c in tm.meld.cards:
                    if c.is_joker and self.can_swap_joker(natural_card, tm.meld_id, c):
                        options.append((natural_card, tm.meld_id, c))
        return options
