"""Card representations, suits, ranks, 106-card deck structure, and Jawaker point valuations."""

from __future__ import annotations
from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, Sequence, Iterable


class Suit(IntEnum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    @property
    def symbol(self) -> str:
        return ["♣", "♦", "♥", "♠"][self.value]

    @property
    def char(self) -> str:
        return ["C", "D", "H", "S"][self.value]

    @classmethod
    def from_char(cls, char: str) -> Suit:
        mapping = {
            "C": cls.CLUBS, "c": cls.CLUBS, "♣": cls.CLUBS,
            "D": cls.DIAMONDS, "d": cls.DIAMONDS, "♦": cls.DIAMONDS,
            "H": cls.HEARTS, "h": cls.HEARTS, "♥": cls.HEARTS,
            "S": cls.SPADES, "s": cls.SPADES, "♠": cls.SPADES,
        }
        if char not in mapping:
            raise ValueError(f"Invalid suit character: {char}")
        return mapping[char]


class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @property
    def char(self) -> str:
        if self.value == 1:
            return "A"
        elif self.value == 10:
            return "T"
        elif self.value == 11:
            return "J"
        elif self.value == 12:
            return "Q"
        elif self.value == 13:
            return "K"
        return str(self.value)

    @classmethod
    def from_char(cls, char: str) -> Rank:
        char_upper = char.upper()
        mapping = {
            "A": cls.ACE, "1": cls.ACE,
            "2": cls.TWO, "3": cls.THREE, "4": cls.FOUR, "5": cls.FIVE,
            "6": cls.SIX, "7": cls.SEVEN, "8": cls.EIGHT, "9": cls.NINE,
            "T": cls.TEN, "10": cls.TEN,
            "J": cls.JACK, "Q": cls.QUEEN, "K": cls.KING
        }
        if char_upper not in mapping:
            raise ValueError(f"Invalid rank character: {char}")
        return mapping[char_upper]


@dataclass(frozen=True, slots=True)
class Card:
    """A card in a 106-card Jawaker Hand deck.
    
    Card IDs 0..105:
      0..51:   Deck 0 (Standard 52 cards)
      52..103: Deck 1 (Standard 52 cards)
      104:     Joker 1 (Wild card)
      105:     Joker 2 (Wild card)
    """
    id: int

    def __post_init__(self):
        if not 0 <= self.id < 106:
            raise ValueError(f"Card ID must be in 0..105, got {self.id}")

    @property
    def is_joker(self) -> bool:
        return self.id in (104, 105)

    @property
    def deck_index(self) -> int:
        if self.is_joker:
            return self.id - 104
        return self.id // 52

    @property
    def canonical_id(self) -> int:
        """Normalized ID (0..51 for standard cards, 104 for Jokers)."""
        if self.is_joker:
            return 104
        return self.id % 52

    @property
    def suit(self) -> Optional[Suit]:
        if self.is_joker:
            return None
        return Suit((self.canonical_id // 13))

    @property
    def rank(self) -> Optional[Rank]:
        if self.is_joker:
            return None
        return Rank((self.canonical_id % 13) + 1)

    @property
    def hand_penalty_value(self) -> int:
        """Penalty points if card remains in hand at round end in Jawaker Hand.
        
        Ace = 11, Joker = 15, 10/J/Q/K = 10, 2..9 = face value.
        """
        if self.is_joker:
            return 15
        if self.rank == Rank.ACE:
            return 11
        if self.rank.value >= 10:
            return 10
        return self.rank.value

    @classmethod
    def create_standard(cls, rank: Rank | int, suit: Suit | int, deck_index: int = 0) -> Card:
        r = rank.value if isinstance(rank, Rank) else rank
        s = suit.value if isinstance(suit, Suit) else suit
        if not (1 <= r <= 13):
            raise ValueError(f"Invalid rank: {r}")
        if not (0 <= s <= 3):
            raise ValueError(f"Invalid suit: {s}")
        if not (0 <= deck_index <= 1):
            raise ValueError(f"Invalid deck_index: {deck_index}")
        canonical = s * 13 + (r - 1)
        return cls(deck_index * 52 + canonical)

    @classmethod
    def create_joker(cls, joker_index: int = 0) -> Card:
        if joker_index not in (0, 1):
            raise ValueError("Joker index must be 0 or 1")
        return cls(104 + joker_index)

    @classmethod
    def from_str(cls, s: str, deck_index: int = 0) -> Card:
        s = s.strip()
        if s.upper() in ("JK", "JOKER", "JK1"):
            return cls.create_joker(0)
        if s.upper() == "JK2":
            return cls.create_joker(1)
        
        if s.endswith("#0") or s.endswith("#1"):
            deck_index = int(s[-1])
            s = s[:-2]

        if len(s) == 2:
            rank = Rank.from_char(s[0])
            suit = Suit.from_char(s[1])
        elif len(s) == 3 and s.startswith("10"):
            rank = Rank.TEN
            suit = Suit.from_char(s[2])
        else:
            raise ValueError(f"Cannot parse card string: {s}")

        return cls.create_standard(rank, suit, deck_index)

    def to_str(self, show_deck: bool = False, use_symbol: bool = False) -> str:
        if self.is_joker:
            jk_num = self.id - 103
            return f"JK{jk_num}"
        s_char = self.suit.symbol if use_symbol else self.suit.char
        base = f"{self.rank.char}{s_char}"
        if show_deck:
            return f"{base}#{self.deck_index}"
        return base

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f"Card({self.to_str(show_deck=True)})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Card):
            return self.id == other.id
        return False

    def __hash__(self) -> int:
        return self.id


# Pre-allocated 106 cards
ALL_CARDS: tuple[Card, ...] = tuple(Card(i) for i in range(106))
