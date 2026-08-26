"""Consistent world determinizer for imperfect information search (PIMC and ISMCTS)."""

from __future__ import annotations
import random
from typing import Optional
from ..engine.card import Card, ALL_CARDS
from ..engine.state import GameState, PlayerView, TurnPhase
from .belief import BayesianBeliefModel


class WorldDeterminizer:
    """Samples complete, consistent ground-truth GameStates matching a player's observation."""

    def __init__(self, rng: Optional[random.Random] = None):
        self.rng = rng or random.Random()

    def sample_world(self, view: PlayerView, belief: BayesianBeliefModel) -> GameState:
        """Construct a concrete GameState with plausible opponent hands and stock pile."""
        # 1. Identify all dead cards
        dead_ids = set(c.id for c in view.hand)
        dead_ids.update(c.id for c in view.discard_pile)
        for tm in view.table.melds:
            dead_ids.update(c.id for c in tm.meld.cards)

        # 2. Known opponent cards
        known_opp: dict[int, set[int]] = {}
        assigned_ids = set(dead_ids)
        for p in range(view.num_players):
            if p != view.player_id:
                opp_known = set(belief.known_cards.get(p, set()))
                known_opp[p] = opp_known
                assigned_ids.update(opp_known)

        # 3. Remaining unseen cards pool
        unassigned_pool = [c for c in ALL_CARDS if c.id not in assigned_ids]
        self.rng.shuffle(unassigned_pool)

        # 4. Fill each opponent's hand to their observed hand size
        hands: dict[int, list[Card]] = {view.player_id: list(view.hand)}

        pool_idx = 0
        for opp in range(view.num_players):
            if opp == view.player_id:
                continue

            target_size = view.player_hand_counts.get(opp, 14)
            opp_hand: list[Card] = [ALL_CARDS[cid] for cid in known_opp.get(opp, set())]

            needed = max(0, target_size - len(opp_hand))
            for _ in range(needed):
                if pool_idx < len(unassigned_pool):
                    opp_hand.append(unassigned_pool[pool_idx])
                    pool_idx += 1

            hands[opp] = sorted(opp_hand, key=lambda c: c.id)

        # 5. Remaining cards in pool form the stock
        stock = unassigned_pool[pool_idx:]

        return GameState(
            num_players=view.num_players,
            hands=hands,
            stock=stock,
            discard_pile=list(view.discard_pile),
            table=view.table.clone(),
            current_player=view.current_player,
            dealer_id=0,
            phase=view.phase,
            turn_number=view.turn_number,
            is_opened=dict(view.player_is_opened),
            opened_turn={p: 1 if view.player_is_opened[p] else None for p in range(view.num_players)},
            drawn_from_discard_this_turn=view.drawn_from_discard_this_turn,
            public_history=list(view.public_history)
        )
