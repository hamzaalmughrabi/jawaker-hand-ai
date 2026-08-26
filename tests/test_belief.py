"""Unit tests for Bayesian opponent belief tracking."""

import pytest
from jawaker_hand_ai.engine.card import Card, Suit, Rank
from jawaker_hand_ai.engine.state import GameState, PublicEvent
from jawaker_hand_ai.engine.actions import Action
from jawaker_hand_ai.opponent.belief import BayesianBeliefModel
from jawaker_hand_ai.opponent.sampler import WorldDeterminizer


def test_bayesian_belief_updates_and_determinizer():
    state = GameState.deal_new_round(num_players=4, dealer=0)
    view = state.get_player_view(0)

    belief = BayesianBeliefModel(my_player_id=0, num_players=4)
    belief.update_from_view(view)

    # My own cards should have 0 probability of being in opponent's hand
    for my_card in view.hand:
        for opp in range(1, 4):
            assert belief.get_opponent_card_probability(opp, my_card) == 0.0

    # Determinizer sample produces valid consistent state
    det = WorldDeterminizer()
    sampled_world = det.sample_world(view, belief)
    assert len(sampled_world.hands[0]) == len(view.hand)
    for opp in range(1, 4):
        assert len(sampled_world.hands[opp]) == view.player_hand_counts[opp]
