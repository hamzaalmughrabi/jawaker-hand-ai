"""Jawaker Hand GameState state machine, turn resolution, table interactions, and player observation views."""

from __future__ import annotations
import random
from functools import cached_property
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Sequence
from .card import Card, ALL_CARDS, Suit, Rank
from .melds import Meld, DisjointMeldCombination, find_valid_opening_melds, find_all_sub_melds, find_best_meld_partition
from .table import TableState, TableMeld
from .actions import Action, ActionType


class TurnPhase(str, Enum):
    DRAW = "DRAW"
    MELD = "MELD"
    DISCARD = "DISCARD"
    ROUND_OVER = "ROUND_OVER"


@dataclass(frozen=True, slots=True)
class PublicEvent:
    player_id: int
    turn_number: int
    action: Action
    card_drawn: Optional[Card] = None


@dataclass(frozen=True, slots=True)
class RoundScoreResult:
    winner_id: Optional[int]
    is_hand_finish: bool
    is_normal_finish: bool
    is_stock_exhausted: bool
    round_scores: dict[int, int]
    unopened_players: tuple[int, ...]
    remaining_hands: dict[int, tuple[Card, ...]]
    score_breakdown: str


@dataclass
class GameState:
    num_players: int
    hands: dict[int, list[Card]]
    stock: list[Card]
    discard_pile: list[Card]
    table: TableState
    current_player: int
    dealer_id: int
    phase: TurnPhase
    turn_number: int
    is_opened: dict[int, bool]
    opened_turn: dict[int, Optional[int]]
    drawn_from_discard_this_turn: Optional[Card] = None
    last_action: Optional[Action] = None
    round_result: Optional[RoundScoreResult] = None
    public_history: list[PublicEvent] = field(default_factory=list)

    def verify_invariants(self) -> None:
        stock_ids = [c.id for c in self.stock]
        discard_ids = [c.id for c in self.discard_pile]
        hand_ids = [c.id for p in self.hands for c in self.hands[p]]
        table_ids = [c.id for tm in self.table.melds for c in tm.meld.cards]

        all_ids = stock_ids + discard_ids + hand_ids + table_ids

        if len(all_ids) != 106:
            raise AssertionError(f"Invariant Violation: Total card count is {len(all_ids)}, expected 106!")

        if len(set(all_ids)) != 106:
            seen = set()
            duplicates = set()
            for cid in all_ids:
                if cid in seen:
                    duplicates.add(cid)
                seen.add(cid)
            dup_strs = [ALL_CARDS[cid].to_str(show_deck=True) for cid in duplicates]
            raise AssertionError(f"Invariant Violation: Duplicate cards detected: {dup_strs}")

    @classmethod
    def deal_new_round(cls, num_players: int = 4, dealer: int = 0, rng: Optional[random.Random] = None) -> GameState:
        if not (2 <= num_players <= 5):
            raise ValueError(f"Jawaker Hand supports 2 to 5 players, got {num_players}")

        if rng is None:
            rng = random.Random()

        deck = list(ALL_CARDS)
        rng.shuffle(deck)

        hands: dict[int, list[Card]] = {}
        first_player = (dealer + 1) % num_players

        card_idx = 0
        for p in range(num_players):
            count = 15 if p == first_player else 14
            p_cards = sorted(deck[card_idx:card_idx + count], key=lambda c: c.id)
            hands[p] = p_cards
            card_idx += count

        upcard = deck[card_idx]
        card_idx += 1
        discard_pile = [upcard]
        stock = deck[card_idx:]

        is_opened = {p: False for p in range(num_players)}
        opened_turn = {p: None for p in range(num_players)}

        return cls(
            num_players=num_players,
            hands=hands,
            stock=stock,
            discard_pile=discard_pile,
            table=TableState(),
            current_player=first_player,
            dealer_id=dealer,
            phase=TurnPhase.DISCARD,
            turn_number=1,
            is_opened=is_opened,
            opened_turn=opened_turn,
            public_history=[]
        )

    def clone(self) -> GameState:
        return GameState(
            num_players=self.num_players,
            hands={p: list(cards) for p, cards in self.hands.items()},
            stock=list(self.stock),
            discard_pile=list(self.discard_pile),
            table=self.table.clone(),
            current_player=self.current_player,
            dealer_id=self.dealer_id,
            phase=self.phase,
            turn_number=self.turn_number,
            is_opened=dict(self.is_opened),
            opened_turn=dict(self.opened_turn),
            drawn_from_discard_this_turn=self.drawn_from_discard_this_turn,
            last_action=self.last_action,
            round_result=self.round_result,
            public_history=list(self.public_history)
        )

    @property
    def is_round_over(self) -> bool:
        return self.phase == TurnPhase.ROUND_OVER

    def can_player_draw_discard(self, player_id: int) -> bool:
        if not self.discard_pile:
            return False
        top_card = self.discard_pile[-1]
        hand = self.hands[player_id]
        hand_with_card = hand + [top_card]
        opened = self.is_opened[player_id]

        if not opened:
            openings = find_valid_opening_melds(hand_with_card)
            for o in openings:
                if top_card.id in o.used_card_ids and len(hand_with_card) - len(o.used_card_ids) >= 1:
                    return True
            return False
        else:
            # Player already opened: can draw if top_card can be immediately laid in a meld or attached
            for m in find_all_sub_melds(hand_with_card):
                if top_card in m.cards and len(hand_with_card) - len(m.cards) >= 1:
                    return True
            attachments = self.table.get_all_attachment_options(hand_with_card)
            for card, m_id, _ in attachments:
                if card.id == top_card.id:
                    return True
            return False

    def get_legal_actions(self) -> list[Action]:
        if self.phase == TurnPhase.ROUND_OVER:
            return []

        p_id = self.current_player
        hand = self.hands[p_id]
        opened = self.is_opened[p_id]

        if self.phase == TurnPhase.DRAW:
            actions: list[Action] = []
            if self.stock:
                actions.append(Action.draw_stock())
            if self.can_player_draw_discard(p_id):
                actions.append(Action.draw_discard())
            return actions

        elif self.phase == TurnPhase.MELD:
            actions: list[Action] = []

            if not opened:
                valid_openings = find_valid_opening_melds(hand)
                if self.drawn_from_discard_this_turn is not None:
                    req_id = self.drawn_from_discard_this_turn.id
                    valid_openings = [o for o in valid_openings if req_id in o.used_card_ids]

                # Must keep at least 1 card in hand to discard!
                valid_openings = [o for o in valid_openings if len(hand) - len(o.used_card_ids) >= 1]

                for opening in valid_openings:
                    actions.append(Action.initial_meld(opening.melds))

                if self.drawn_from_discard_this_turn is None:
                    actions.append(Action.pass_meld())

                return actions
            else:
                if self.drawn_from_discard_this_turn is not None:
                    req_card = self.drawn_from_discard_this_turn
                    for m in find_all_sub_melds(hand):
                        if req_card in m.cards and len(hand) - len(m.cards) >= 1:
                            actions.append(Action.lay_meld(m))

                    if len(hand) >= 2:
                        attachments = self.table.get_all_attachment_options(hand)
                        for card, m_id, _ in attachments:
                            if card.id == req_card.id:
                                actions.append(Action.attach_card(card, m_id))
                    # Note: Cannot PASS_MELD if discard card has not yet been melded/attached
                else:
                    for m in find_all_sub_melds(hand):
                        if len(hand) - len(m.cards) >= 1:
                            actions.append(Action.lay_meld(m))

                    if len(hand) >= 2:
                        attachments = self.table.get_all_attachment_options(hand)
                        for card, m_id, _ in attachments:
                            actions.append(Action.attach_card(card, m_id))

                    joker_swaps = self.table.get_all_joker_swap_options(hand)
                    for nat_card, m_id, j_card in joker_swaps:
                        actions.append(Action.swap_joker(nat_card, m_id, j_card))

                    actions.append(Action.pass_meld())
                return actions

        elif self.phase == TurnPhase.DISCARD:
            return [Action.discard(c) for c in hand]

        return []

    def apply_action(self, action: Action, verify_invariants: bool = False) -> None:
        if self.phase == TurnPhase.ROUND_OVER:
            raise ValueError("Cannot apply action in ROUND_OVER phase.")

        p_id = self.current_player
        hand = self.hands[p_id]

        if self.phase == TurnPhase.DRAW:
            if action.action_type == ActionType.DRAW_STOCK:
                if not self.stock:
                    raise ValueError("Cannot draw from empty stock.")
                card = self.stock.pop()
                hand.append(card)
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
                self.last_action = action
                self.phase = TurnPhase.MELD
                return

            elif action.action_type == ActionType.DRAW_DISCARD:
                if not self.can_player_draw_discard(p_id):
                    raise ValueError("Cannot draw from discard pile: top card does not enable opening or attaching.")
                card = self.discard_pile.pop()
                hand.append(card)
                self.drawn_from_discard_this_turn = card
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, card))
                self.last_action = action
                self.phase = TurnPhase.MELD
                return

            elif action.action_type == ActionType.DISCARD:
                if self.stock:
                    card = self.stock.pop()
                    hand.append(card)
                self.phase = TurnPhase.DISCARD
                self.apply_action(action)
                return

        elif self.phase == TurnPhase.MELD:
            if action.action_type == ActionType.DISCARD:
                self.drawn_from_discard_this_turn = None
                self.phase = TurnPhase.DISCARD
                self.apply_action(action)
                return

            elif action.action_type == ActionType.PASS_MELD:
                if self.drawn_from_discard_this_turn is not None and self.drawn_from_discard_this_turn in hand:
                    raise ValueError("Cannot pass meld: card drawn from discard must be melded or attached.")
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
                self.last_action = action
                self.phase = TurnPhase.DISCARD
                return

            elif action.action_type == ActionType.INITIAL_MELD:
                if action.melds is None:
                    raise ValueError("Initial meld action must contain melds.")
                used_cards: list[Card] = []
                for m in action.melds:
                    for c in m.cards:
                        if c not in hand:
                            raise ValueError(f"Card {c} for meld not in hand.")
                        used_cards.append(c)

                if len(hand) - len(used_cards) < 1:
                    raise ValueError("Cannot meld all cards: must keep at least 1 card in hand to discard.")

                for c in used_cards:
                    hand.remove(c)

                for m in action.melds:
                    self.table.add_meld(p_id, m)

                self.is_opened[p_id] = True
                self.opened_turn[p_id] = self.turn_number
                if self.drawn_from_discard_this_turn is not None and self.drawn_from_discard_this_turn not in hand:
                    self.drawn_from_discard_this_turn = None
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
                self.last_action = action
                return

            elif action.action_type == ActionType.LAY_MELD:
                if action.melds is None or not action.melds:
                    raise ValueError("Lay meld action must contain a meld.")
                m = action.melds[0]
                if len(hand) - len(m.cards) < 1:
                    raise ValueError("Cannot lay meld: must keep at least 1 card in hand to discard.")
                for c in m.cards:
                    if c not in hand:
                        raise ValueError(f"Card {c} not in hand.")
                    hand.remove(c)
                self.table.add_meld(p_id, m)
                if self.drawn_from_discard_this_turn is not None and self.drawn_from_discard_this_turn not in hand:
                    self.drawn_from_discard_this_turn = None
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
                self.last_action = action
                return

            elif action.action_type == ActionType.ATTACH_CARD:
                if action.card is None or action.meld_id is None:
                    raise ValueError("Attach action requires card and meld_id.")
                if len(hand) <= 1:
                    raise ValueError("Cannot attach final card: must discard the last card to finish.")
                if action.card not in hand:
                    raise ValueError(f"Card {action.card} not in hand.")
                hand.remove(action.card)
                self.table.attach_card(p_id, action.card, action.meld_id)
                if self.drawn_from_discard_this_turn is not None and self.drawn_from_discard_this_turn not in hand:
                    self.drawn_from_discard_this_turn = None
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
                self.last_action = action
                return

            elif action.action_type == ActionType.SWAP_JOKER:
                if action.card is None or action.meld_id is None or action.target_joker is None:
                    raise ValueError("Swap Joker requires card, meld_id, target_joker.")
                if action.card not in hand:
                    raise ValueError(f"Natural card {action.card} not in hand.")
                hand.remove(action.card)
                liberated_joker = self.table.swap_joker(p_id, action.card, action.meld_id, action.target_joker)
                hand.append(liberated_joker)
                self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
                self.last_action = action
                return

        elif self.phase == TurnPhase.DISCARD:
            if action.action_type != ActionType.DISCARD or action.card is None:
                raise ValueError("Must discard a card in DISCARD phase.")
            if action.card not in hand:
                raise ValueError(f"Card {action.card} not in hand to discard.")

            hand.remove(action.card)
            self.discard_pile.append(action.card)
            self.public_history.append(PublicEvent(p_id, self.turn_number, action, None))
            self.last_action = action

            if len(hand) == 0:
                self._resolve_player_finish(p_id)
                return

            self.current_player = (self.current_player + 1) % self.num_players
            self.drawn_from_discard_this_turn = None
            self.phase = TurnPhase.DRAW
            self.turn_number += 1
            return

        raise ValueError(f"Invalid action {action} in phase {self.phase}")

    def _resolve_player_finish(self, winner_id: int) -> None:
        is_hand = (self.opened_turn[winner_id] == self.turn_number)

        round_scores: dict[int, int] = {}
        unopened_players: list[int] = []
        rem_hands: dict[int, tuple[Card, ...]] = {}

        for p in range(self.num_players):
            rem_cards = tuple(sorted(self.hands[p], key=lambda c: c.id))
            rem_hands[p] = rem_cards

            if p == winner_id:
                round_scores[p] = -60 if is_hand else -30
            else:
                if not self.is_opened[p]:
                    unopened_players.append(p)
                    round_scores[p] = 200 if is_hand else 100
                else:
                    raw_sum = sum(c.hand_penalty_value for c in rem_cards)
                    round_scores[p] = raw_sum * 2 if is_hand else raw_sum

        breakdown = (
            f"Winner: Player {winner_id} with {'HAND (-60 pts)' if is_hand else 'NORMAL finish (-30 pts)'}! "
            f"Scores: {round_scores}"
        )

        self.round_result = RoundScoreResult(
            winner_id=winner_id,
            is_hand_finish=is_hand,
            is_normal_finish=not is_hand,
            is_stock_exhausted=False,
            round_scores=round_scores,
            unopened_players=tuple(unopened_players),
            remaining_hands=rem_hands,
            score_breakdown=breakdown
        )
        self.phase = TurnPhase.ROUND_OVER

    def _resolve_stock_exhausted(self) -> None:
        round_scores: dict[int, int] = {}
        rem_hands: dict[int, tuple[Card, ...]] = {}
        unopened_players: list[int] = []

        for p in range(self.num_players):
            rem_cards = tuple(sorted(self.hands[p], key=lambda c: c.id))
            rem_hands[p] = rem_cards
            if not self.is_opened[p]:
                unopened_players.append(p)
                round_scores[p] = 100
            else:
                round_scores[p] = sum(c.hand_penalty_value for c in rem_cards)

        self.round_result = RoundScoreResult(
            winner_id=None,
            is_hand_finish=False,
            is_normal_finish=False,
            is_stock_exhausted=True,
            round_scores=round_scores,
            unopened_players=tuple(unopened_players),
            remaining_hands=rem_hands,
            score_breakdown=f"Stock exhausted. Round scores: {round_scores}"
        )
        self.phase = TurnPhase.ROUND_OVER

    def get_player_view(self, player_id: int) -> PlayerView:
        my_hand = tuple(sorted(self.hands[player_id], key=lambda c: c.id))
        hand_counts = {p: len(self.hands[p]) for p in range(self.num_players)}

        return PlayerView(
            player_id=player_id,
            num_players=self.num_players,
            hand=my_hand,
            table=self.table.clone(),
            discard_pile=tuple(self.discard_pile),
            top_discard=self.discard_pile[-1] if self.discard_pile else None,
            stock_count=len(self.stock),
            player_hand_counts=hand_counts,
            player_is_opened=dict(self.is_opened),
            turn_number=self.turn_number,
            current_player=self.current_player,
            phase=self.phase,
            drawn_from_discard_this_turn=self.drawn_from_discard_this_turn,
            public_history=tuple(self.public_history)
        )


@dataclass(frozen=True)
class PlayerView:
    player_id: int
    num_players: int
    hand: tuple[Card, ...]
    table: TableState
    discard_pile: tuple[Card, ...]
    top_discard: Optional[Card]
    stock_count: int
    player_hand_counts: dict[int, int]
    player_is_opened: dict[int, bool]
    turn_number: int
    current_player: int
    phase: TurnPhase
    drawn_from_discard_this_turn: Optional[Card]
    public_history: tuple[PublicEvent, ...]

    @property
    def is_my_turn(self) -> bool:
        return self.current_player == self.player_id

    @property
    def am_i_opened(self) -> bool:
        return self.player_is_opened[self.player_id]

    @cached_property
    def best_meld_partition(self) -> DisjointMeldCombination:
        return find_best_meld_partition(self.hand)
