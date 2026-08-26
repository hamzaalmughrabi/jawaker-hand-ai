"""Bayesian belief tracking over 106 cards for opponent hands in Jawaker Hand."""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field
from typing import Sequence, Optional
from ..engine.card import Card, ALL_CARDS
from ..engine.state import PlayerView, PublicEvent
from ..engine.actions import ActionType


class BayesianBeliefModel:
    """Maintains posterior probability distributions over hidden cards for each opponent."""

    def __init__(self, my_player_id: int, num_players: int):
        self.my_player_id = my_player_id
        self.num_players = num_players
        self.opponent_ids = [p for p in range(num_players) if p != my_player_id]

        # Probabilities: matrix of shape (num_players, 106)
        # probs[p, c] = P(card c is in player p's hand)
        self.probs = np.zeros((num_players, 106), dtype=np.float64)
        self.known_cards: dict[int, set[int]] = {p: set() for p in range(num_players)}
        self.dead_cards: set[int] = set()

    def update_from_view(self, view: PlayerView) -> None:
        """Update posterior beliefs from public history and current player view."""
        self.dead_cards.clear()
        for p in range(self.num_players):
            self.known_cards[p].clear()

        # 1. Mark my own hand cards
        my_card_ids = set(c.id for c in view.hand)
        self.known_cards[self.my_player_id] = my_card_ids
        self.dead_cards.update(my_card_ids)

        # 2. Mark table melds cards
        for tm in view.table.melds:
            for c in tm.meld.cards:
                self.dead_cards.add(c.id)

        # 3. Mark discard pile cards
        for c in view.discard_pile:
            self.dead_cards.add(c.id)

        # 4. Process public events to identify cards drawn from discard
        for ev in view.public_history:
            if ev.card_drawn is not None:
                # Player drew this card from discard
                if ev.card_drawn.id not in self.dead_cards:
                    self.known_cards[ev.player_id].add(ev.card_drawn.id)

        # Reset probability matrix
        self.probs.fill(0.0)

        # Set 1.0 for known cards
        for p in range(self.num_players):
            for cid in self.known_cards[p]:
                self.probs[p, cid] = 1.0

        # Unassigned cards = all cards minus dead_cards minus known opponent cards
        all_assigned = set(self.dead_cards)
        for p in range(self.num_players):
            all_assigned.update(self.known_cards[p])

        unassigned_cards = [c.id for c in ALL_CARDS if c.id not in all_assigned]
        unassigned_count = len(unassigned_cards)

        if unassigned_count > 0:
            # Distribute remaining cards to match each opponent's remaining hand count
            for p in self.opponent_ids:
                known_count = len(self.known_cards[p])
                target_count = view.player_hand_counts.get(p, 14)
                needed = max(0, target_count - known_count)

                # Total unassigned pool is split between opponents and stock
                total_hidden_needed = sum(
                    max(0, view.player_hand_counts.get(opp, 14) - len(self.known_cards[opp]))
                    for opp in self.opponent_ids
                ) + view.stock_count

                if total_hidden_needed > 0:
                    prob_per_card = needed / total_hidden_needed
                    for cid in unassigned_cards:
                        self.probs[p, cid] = prob_per_card

    def get_opponent_card_probability(self, opp_id: int, card: Card | int) -> float:
        cid = card.id if isinstance(card, Card) else card
        return float(self.probs[opp_id, cid])

    def get_summary(self) -> dict[str, dict[str, float]]:
        """Return human-readable summary of highest-probability cards for each opponent."""
        summary: dict[str, dict[str, float]] = {}
        for opp in self.opponent_ids:
            opp_dict: dict[str, float] = {}
            # Top 5 most likely cards
            sorted_indices = np.argsort(self.probs[opp])[::-1]
            for idx in sorted_indices[:5]:
                if self.probs[opp, idx] > 0.05:
                    card_str = ALL_CARDS[idx].to_str(show_deck=True)
                    opp_dict[card_str] = round(float(self.probs[opp, idx]), 3)
            summary[f"Opponent_{opp}"] = opp_dict
        return summary
