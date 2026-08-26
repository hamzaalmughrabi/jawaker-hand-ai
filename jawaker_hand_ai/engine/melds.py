"""Combinatorial logic for validating Jawaker Hand melds (Sets and Runs) and calculating 51-point initial openings."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from itertools import combinations, product
from typing import Sequence, Optional
from .card import Card, Suit, Rank


class MeldType(Enum):
    SET = "SET"
    RUN = "RUN"


@dataclass(frozen=True, slots=True)
class Meld:
    """Represents a validated meld laid on the table."""
    type: MeldType
    cards: tuple[Card, ...]
    represented_ranks: tuple[Rank, ...]
    represented_suits: tuple[Suit, ...]
    points: int

    def __post_init__(self):
        if len(self.cards) != len(self.represented_ranks) or len(self.cards) != len(self.represented_suits):
            raise ValueError("Meld cards and represented properties must have identical lengths")

    @property
    def contains_joker(self) -> bool:
        """Check if any card in this meld is a Joker."""
        return any(c.is_joker for c in self.cards)

    def get_joker_represented_card(self, joker_card: Card) -> Optional[tuple[Rank, Suit]]:
        """Get represented (Rank, Suit) of a Joker card in this meld."""
        for c, r, s in zip(self.cards, self.represented_ranks, self.represented_suits):
            if c.id == joker_card.id:
                return (r, s)
        return None

    def to_str(self) -> str:
        rep_parts = []
        for c, r, s in zip(self.cards, self.represented_ranks, self.represented_suits):
            r_str = "10" if r == Rank.TEN else r.char
            if c.is_joker:
                rep_parts.append(f"{c.to_str()}({r_str}{s.char})")
            else:
                rep_parts.append(f"{r_str}{s.char}")
        return f"{self.type.value}[{' '.join(rep_parts)} -> {self.points}pts]"


def calculate_card_meld_points(rank: Rank, is_ace_low: bool = False) -> int:
    """Calculate point value of a card when contributing to a meld."""
    if rank == Rank.ACE:
        return 1 if is_ace_low else 11
    if rank.value >= 10:
        return 10
    return rank.value


def validate_set(cards: Sequence[Card]) -> Optional[Meld]:
    """Validate whether 3 or 4 cards form a legal Set."""
    n = len(cards)
    if not (3 <= n <= 4):
        return None

    jokers = [c for c in cards if c.is_joker]
    naturals = [c for c in cards if not c.is_joker]

    if not naturals:
        return None

    target_rank = naturals[0].rank
    if any(c.rank != target_rank for c in naturals):
        return None

    used_suits = [c.suit for c in naturals if c.suit is not None]
    if len(set(used_suits)) != len(used_suits):
        return None

    if len(jokers) > 2:
        return None

    all_suits = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES]
    available_suits = [s for s in all_suits if s not in used_suits]

    if len(available_suits) < len(jokers):
        return None

    ordered_cards = list(naturals)
    represented_ranks = [target_rank] * len(naturals)
    represented_suits = list(used_suits)

    for i, j_card in enumerate(jokers):
        ordered_cards.append(j_card)
        represented_ranks.append(target_rank)
        represented_suits.append(available_suits[i])

    pts = 0
    for r in represented_ranks:
        if r == Rank.ACE:
            pts += 11
        elif r.value >= 10:
            pts += 10
        else:
            pts += r.value

    return Meld(
        type=MeldType.SET,
        cards=tuple(ordered_cards),
        represented_ranks=tuple(represented_ranks),
        represented_suits=tuple(represented_suits),
        points=pts
    )


def validate_run(cards: Sequence[Card]) -> Optional[Meld]:
    """Validate whether 3 to 14 cards form a legal single-suit Run."""
    n = len(cards)
    if not (3 <= n <= 14):
        return None

    jokers = [c for c in cards if c.is_joker]
    naturals = [c for c in cards if not c.is_joker]

    if not naturals:
        return None

    target_suit = naturals[0].suit
    if any(c.suit != target_suit for c in naturals):
        return None

    if len(jokers) > 2:
        return None

    # Check for duplicate natural ranks in run
    nat_ranks = [c.rank.value for c in naturals if c.rank is not None]
    if len(set(nat_ranks)) != len(nat_ranks):
        return None

    run_len = len(cards)
    best_meld: Optional[Meld] = None

    # Candidate starts: 1 (Ace-low: A-2-3..) to 12 (Q-K-A is 12-13-14)
    for start_r in range(1, 15 - run_len + 2):
        target_sequence = [start_r + i for i in range(run_len)]
        if target_sequence[-1] > 14:
            continue

        mapped_ranks: list[Rank] = []
        valid_map = True
        for num in target_sequence:
            if num == 1 or num == 14:
                mapped_ranks.append(Rank.ACE)
            else:
                try:
                    mapped_ranks.append(Rank(num))
                except ValueError:
                    valid_map = False
                    break

        if not valid_map:
            continue

        needed_ranks = []
        for num, r_enum in zip(target_sequence, mapped_ranks):
            needed_ranks.append((num, r_enum))

        matched_naturals: list[Optional[Card]] = [None] * run_len
        used_naturals: set[int] = set()

        for idx, (num, r_enum) in enumerate(needed_ranks):
            for c in naturals:
                if c.id not in used_naturals and c.rank == r_enum:
                    matched_naturals[idx] = c
                    used_naturals.add(c.id)
                    break

        if len(used_naturals) == len(naturals):
            joker_idx = 0
            ordered_cards: list[Card] = []
            valid_seq = True

            for idx, c in enumerate(matched_naturals):
                if c is not None:
                    ordered_cards.append(c)
                else:
                    if joker_idx < len(jokers):
                        ordered_cards.append(jokers[joker_idx])
                        joker_idx += 1
                    else:
                        valid_seq = False
                        break

            if valid_seq and len(ordered_cards) == run_len:
                pts = 0
                for r_num, r_rank in zip(target_sequence, mapped_ranks):
                    if r_num == 1:
                        pts += 1
                    elif r_num == 14:
                        pts += 11
                    elif r_rank.value >= 10:
                        pts += 10
                    else:
                        pts += r_rank.value

                represented_suits = tuple(target_suit for _ in range(run_len))
                best_meld = Meld(
                    type=MeldType.RUN,
                    cards=tuple(ordered_cards),
                    represented_ranks=tuple(mapped_ranks),
                    represented_suits=represented_suits,
                    points=pts
                )
                break

    return best_meld


def validate_meld(cards: Sequence[Card]) -> Optional[Meld]:
    """Validate whether cards form a valid Set or Run."""
    if len(cards) < 3:
        return None
    if len(cards) <= 4:
        s_meld = validate_set(cards)
        if s_meld is not None:
            return s_meld
    r_meld = validate_run(cards)
    if r_meld is not None:
        return r_meld
    return None


def find_all_sub_melds(hand: Sequence[Card]) -> list[Meld]:
    """High-speed Rank & Suit bucketing meld generator with duplicate rank preservation."""
    melds: list[Meld] = []
    seen_masks: set[tuple[int, ...]] = set()

    jokers = [c for c in hand if c.is_joker]
    naturals = [c for c in hand if not c.is_joker]

    # Map card IDs to hand index for proximity scoring
    card_idx_map: dict[int, int] = {c.id: i for i, c in enumerate(hand)}

    # 1. Sets Generator (grouped by Rank & Suit)
    rank_groups: dict[Rank, list[Card]] = {}
    for c in naturals:
        if c.rank is not None:
            rank_groups.setdefault(c.rank, []).append(c)

    for rank, cards in rank_groups.items():
        suit_to_cards: dict[Suit, list[Card]] = {}
        for c in cards:
            if c.suit is not None:
                suit_to_cards.setdefault(c.suit, []).append(c)

        unique_suits = list(suit_to_cards.keys())

        # Test set sizes 3 and 4
        for k in (3, 4):
            # 0 Jokers
            if len(unique_suits) >= k:
                for s_comb in combinations(unique_suits, k):
                    for c_tuple in product(*[suit_to_cards[s] for s in s_comb]):
                        m = validate_set(c_tuple)
                        if m is not None:
                            key = tuple(sorted(c.id for c in m.cards))
                            if key not in seen_masks:
                                seen_masks.add(key)
                                melds.append(m)

            # 1 Joker
            if len(jokers) >= 1 and len(unique_suits) >= k - 1 and (k - 1 >= 2):
                for s_comb in combinations(unique_suits, k - 1):
                    for c_tuple in product(*[suit_to_cards[s] for s in s_comb]):
                        cand = list(c_tuple) + [jokers[0]]
                        m = validate_set(cand)
                        if m is not None:
                            key = tuple(sorted(c.id for c in m.cards))
                            if key not in seen_masks:
                                seen_masks.add(key)
                                melds.append(m)

            # 2 Jokers
            if len(jokers) >= 2 and k >= 3 and len(unique_suits) >= k - 2 and (k - 2 >= 1):
                for s_comb in combinations(unique_suits, k - 2):
                    for c_tuple in product(*[suit_to_cards[s] for s in s_comb]):
                        cand = list(c_tuple) + [jokers[0], jokers[1]]
                        m = validate_set(cand)
                        if m is not None:
                            key = tuple(sorted(c.id for c in m.cards))
                            if key not in seen_masks:
                                seen_masks.add(key)
                                melds.append(m)

    # 2. Runs Generator (grouped by Suit & Rank list)
    suit_groups: dict[Suit, dict[int, list[Card]]] = {}
    for c in naturals:
        if c.suit is not None and c.rank is not None:
            suit_groups.setdefault(c.suit, {}).setdefault(c.rank.value, []).append(c)

    for suit, rank_dict in suit_groups.items():
        # Test candidate start ranks from 1 (Ace low) to 11
        for start_r in range(1, 12):
            for L in range(3, min(8, 15 - start_r + 1)):
                target_ranks = [start_r + i for i in range(L)]
                ranks_cards_options: list[list[Card]] = []
                missing_count = 0

                for r_val in target_ranks:
                    check_val = 1 if r_val == 14 else r_val
                    if check_val in rank_dict and rank_dict[check_val]:
                        ranks_cards_options.append(rank_dict[check_val])
                    else:
                        missing_count += 1
                        ranks_cards_options.append([])

                if missing_count <= len(jokers) and (L - missing_count) >= 1:
                    natural_positions = [i for i, opts in enumerate(ranks_cards_options) if opts]
                    opt_lists = [ranks_cards_options[i] for i in natural_positions]

                    for chosen_naturals in product(*opt_lists):
                        cand_cards = list(chosen_naturals) + jokers[:missing_count]
                        m = validate_run(cand_cards)
                        if m is not None:
                            key = tuple(sorted(c.id for c in m.cards))
                            if key not in seen_masks:
                                seen_masks.add(key)
                                melds.append(m)

    # Sort melds by: higher points first, then tighter hand proximity span
    def meld_sort_key(m: Meld) -> tuple[int, int, int]:
        indices = [card_idx_map[c.id] for c in m.cards if c.id in card_idx_map]
        span = (max(indices) - min(indices)) if indices else 0
        return (-m.points, span, len(m.cards))

    melds.sort(key=meld_sort_key)
    return melds


@dataclass(frozen=True, slots=True)
class DisjointMeldCombination:
    """A set of mutually disjoint melds formed from a hand."""
    melds: tuple[Meld, ...]
    total_points: int
    used_card_ids: tuple[int, ...]

    @property
    def satisfies_51_points(self) -> bool:
        return self.total_points >= 51


def find_valid_opening_melds(hand: Sequence[Card]) -> list[DisjointMeldCombination]:
    """Find all disjoint meld combinations from hand that achieve >= 51 points for initial opening."""
    candidate_melds = find_all_sub_melds(hand)
    if not candidate_melds:
        return []

    results: list[DisjointMeldCombination] = []
    seen_card_sets: set[frozenset[int]] = set()

    def search(start_idx: int, current_melds: list[Meld], used_ids: set[int], current_pts: int):
        if current_pts >= 51:
            card_key = frozenset(used_ids)
            if card_key not in seen_card_sets:
                seen_card_sets.add(card_key)
                results.append(DisjointMeldCombination(
                    melds=tuple(current_melds),
                    total_points=current_pts,
                    used_card_ids=tuple(sorted(used_ids))
                ))

        for i in range(start_idx, min(len(candidate_melds), start_idx + 20)):
            m = candidate_melds[i]
            m_card_ids = set(c.id for c in m.cards)
            if not (used_ids & m_card_ids):
                current_melds.append(m)
                search(i + 1, current_melds, used_ids | m_card_ids, current_pts + m.points)
                current_melds.pop()

    search(0, [], set(), 0)
    results.sort(key=lambda c: c.total_points, reverse=True)
    return results


def find_best_meld_partition(hand: Sequence[Card]) -> DisjointMeldCombination:
    """Find the disjoint combination of melds maximizing total points in hand with tightest card adjacency."""
    candidate_melds = find_all_sub_melds(hand)
    if not candidate_melds:
        return DisjointMeldCombination(melds=(), total_points=0, used_card_ids=())

    card_idx_map: dict[int, int] = {c.id: i for i, c in enumerate(hand)}
    best_comb = DisjointMeldCombination(melds=(), total_points=0, used_card_ids=())
    best_total_span = 999999

    def search(start_idx: int, current_melds: list[Meld], used_ids: set[int], current_pts: int):
        nonlocal best_comb, best_total_span
        if current_pts > best_comb.total_points:
            total_span = 0
            for m in current_melds:
                idxs = [card_idx_map[c.id] for c in m.cards if c.id in card_idx_map]
                if idxs:
                    total_span += (max(idxs) - min(idxs))

            best_comb = DisjointMeldCombination(
                melds=tuple(current_melds),
                total_points=current_pts,
                used_card_ids=tuple(sorted(used_ids))
            )
            best_total_span = total_span
        elif current_pts == best_comb.total_points and current_pts > 0:
            total_span = 0
            for m in current_melds:
                idxs = [card_idx_map[c.id] for c in m.cards if c.id in card_idx_map]
                if idxs:
                    total_span += (max(idxs) - min(idxs))

            if total_span < best_total_span:
                best_comb = DisjointMeldCombination(
                    melds=tuple(current_melds),
                    total_points=current_pts,
                    used_card_ids=tuple(sorted(used_ids))
                )
                best_total_span = total_span

        for i in range(start_idx, min(len(candidate_melds), start_idx + 20)):
            m = candidate_melds[i]
            m_card_ids = set(c.id for c in m.cards)
            if not (used_ids & m_card_ids):
                current_melds.append(m)
                search(i + 1, current_melds, used_ids | m_card_ids, current_pts + m.points)
                current_melds.pop()

    search(0, [], set(), 0)
    return best_comb
