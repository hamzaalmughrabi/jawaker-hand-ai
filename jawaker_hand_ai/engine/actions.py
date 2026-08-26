"""Action definitions, parameters, and serialization for Jawaker Hand."""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Sequence
from .card import Card, ALL_CARDS
from .melds import Meld


class ActionType(str, Enum):
    DRAW_STOCK = "DRAW_STOCK"
    DRAW_DISCARD = "DRAW_DISCARD"
    INITIAL_MELD = "INITIAL_MELD"
    LAY_MELD = "LAY_MELD"
    ATTACH_CARD = "ATTACH_CARD"
    SWAP_JOKER = "SWAP_JOKER"
    PASS_MELD = "PASS_MELD"
    DISCARD = "DISCARD"


@dataclass(frozen=True, slots=True)
class Action:
    """An action performed by a player during a Jawaker Hand turn."""
    action_type: ActionType
    card: Optional[Card] = None
    melds: Optional[tuple[Meld, ...]] = None
    meld_id: Optional[int] = None
    target_joker: Optional[Card] = None

    @classmethod
    def draw_stock(cls) -> Action:
        return cls(ActionType.DRAW_STOCK)

    @classmethod
    def draw_discard(cls) -> Action:
        return cls(ActionType.DRAW_DISCARD)

    @classmethod
    def initial_meld(cls, melds: Sequence[Meld]) -> Action:
        return cls(ActionType.INITIAL_MELD, melds=tuple(melds))

    @classmethod
    def lay_meld(cls, meld: Meld) -> Action:
        return cls(ActionType.LAY_MELD, melds=(meld,))

    @classmethod
    def attach_card(cls, card: Card, meld_id: int) -> Action:
        return cls(ActionType.ATTACH_CARD, card=card, meld_id=meld_id)

    @classmethod
    def swap_joker(cls, natural_card: Card, meld_id: int, joker_card: Card) -> Action:
        return cls(ActionType.SWAP_JOKER, card=natural_card, meld_id=meld_id, target_joker=joker_card)

    @classmethod
    def pass_meld(cls) -> Action:
        return cls(ActionType.PASS_MELD)

    @classmethod
    def discard(cls, card: Card) -> Action:
        return cls(ActionType.DISCARD, card=card)

    def to_str(self) -> str:
        if self.action_type == ActionType.DISCARD and self.card is not None:
            return f"DISCARD:{self.card.to_str()}"
        elif self.action_type == ActionType.INITIAL_MELD and self.melds:
            m_strs = "+".join(m.to_str() for m in self.melds)
            return f"INITIAL_MELD:{m_strs}"
        elif self.action_type == ActionType.LAY_MELD and self.melds:
            return f"LAY_MELD:{self.melds[0].to_str()}"
        elif self.action_type == ActionType.ATTACH_CARD and self.card is not None:
            return f"ATTACH:{self.card.to_str()}->Meld#{self.meld_id}"
        elif self.action_type == ActionType.SWAP_JOKER and self.card is not None and self.target_joker is not None:
            return f"SWAP_JOKER:{self.card.to_str()}->Meld#{self.meld_id}[{self.target_joker.to_str()}]"
        return self.action_type.value

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Action({self.to_str()})"
