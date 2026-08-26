"""Unit tests for card conservation invariants and DeepRLAgent neural evaluations."""

import pytest
import random
from jawaker_hand_ai.engine.state import GameState, TurnPhase
from jawaker_hand_ai.engine.actions import Action
from jawaker_hand_ai.agents.deep_rl_agent import DeepRLAgent
from jawaker_hand_ai.agents.hybrid_search_agent import HybridSearchAgent
from jawaker_hand_ai.learning.network import NeuralValueNetwork
from jawaker_hand_ai.learning.trainer import SelfPlayTrainer


def test_strict_106_card_conservation_invariant():
    """Verify that across random 1v1 and 4-player games, all 106 card IDs are conserved with zero leaks or duplicates."""
    for num_players in (2, 4):
        state = GameState.deal_new_round(num_players=num_players, dealer=0, rng=random.Random(123))
        state.verify_invariants()

        turn_count = 0
        while not state.is_round_over and turn_count < 60:
            legal = state.get_legal_actions()
            if not legal:
                break
            act = random.choice(legal)
            # Apply action with invariant verification on every single turn!
            state.apply_action(act, verify_invariants=True)
            turn_count += 1


def test_neural_value_network_forward_and_backward():
    net = NeuralValueNetwork(seed=42)
    # Synthetic batch
    X = np_data = random.Random(42)
    import numpy as np
    X_batch = np.random.randn(16, 32)
    y_target = np.random.randn(16, 1) * 30.0

    initial_loss = net.train_step(X_batch, y_target, lr=0.01)
    assert initial_loss > 0

    # Loss should decrease after training steps
    for _ in range(50):
        final_loss = net.train_step(X_batch, y_target, lr=0.01)

    assert final_loss < initial_loss


def test_deep_rl_agent_and_hybrid_search_selection():
    state = GameState.deal_new_round(num_players=2, dealer=0)
    view = state.get_player_view(state.current_player)
    legal = state.get_legal_actions()

    deep_rl = DeepRLAgent(name="DeepRL", player_id=state.current_player)
    act_rl, trace_rl = deep_rl.select_action(view, legal)
    assert act_rl in legal
    assert len(trace_rl.candidate_evaluations) == len(legal)

    hybrid = HybridSearchAgent(name="Hybrid", player_id=state.current_player, iterations=10)
    act_hy, trace_hy = hybrid.select_action(view, legal)
    assert act_hy in legal
