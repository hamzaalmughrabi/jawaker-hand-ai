"""Perfect Information Monte Carlo (PIMC) search agent."""

from __future__ import annotations
import time
import random
from typing import Sequence, Optional
from .base import BaseAgent
from ..engine.state import PlayerView, GameState, TurnPhase
from ..engine.actions import Action, ActionType
from ..opponent.belief import BayesianBeliefModel
from ..opponent.sampler import WorldDeterminizer
from ..persistence.trace import DecisionTrace, ActionEvaluation


class PIMCAgent(BaseAgent):
    """Perfect Information Monte Carlo (PIMC) search across sampled belief worlds."""

    def __init__(
        self,
        name: str = "PIMCAgent",
        player_id: int = 0,
        num_world_samples: int = 5,
        rng: Optional[random.Random] = None
    ):
        super().__init__(name, player_id)
        self.num_world_samples = num_world_samples
        self.rng = rng or random.Random()
        self.determinizer = WorldDeterminizer(self.rng)
        self.belief = BayesianBeliefModel(player_id, 4)

    def select_action(self, view: PlayerView, legal_actions: Sequence[Action]) -> tuple[Action, DecisionTrace]:
        t0 = time.perf_counter()
        if not legal_actions:
            raise ValueError("No legal actions available.")

        if self.belief.num_players != view.num_players:
            self.belief = BayesianBeliefModel(self.player_id, view.num_players)
        self.belief.update_from_view(view)

        # Fast path if only 1 action
        if len(legal_actions) == 1:
            trace = self._create_trace(view, legal_actions[0], [], 0.1)
            return legal_actions[0], trace

        action_scores: dict[str, float] = {a.to_str(): 0.0 for a in legal_actions}
        action_map = {a.to_str(): a for a in legal_actions}

        # Sample K worlds
        for _ in range(self.num_world_samples):
            world = self.determinizer.sample_world(view, self.belief)

            for action in legal_actions:
                world_clone = world.clone()
                try:
                    world_clone.apply_action(action)
                    score = self._evaluate_state(world_clone, self.player_id)
                except Exception:
                    score = -1000.0
                action_scores[action.to_str()] += score

        evaluations: list[ActionEvaluation] = []
        best_action_str = max(action_scores.keys(), key=lambda k: action_scores[k])
        best_action = action_map[best_action_str]

        for a_str, total_score in action_scores.items():
            avg_score = total_score / self.num_world_samples
            evaluations.append(ActionEvaluation(action_str=a_str, q_value=avg_score))

        latency = (time.perf_counter() - t0) * 1000.0
        belief_summary = self.belief.get_summary()
        trace = self._create_trace(view, best_action, evaluations, latency, belief_summary)
        return best_action, trace

    def _evaluate_state(self, state: GameState, player_id: int) -> float:
        """Heuristic value of a determinized state from perspective of player_id."""
        if state.is_round_over and state.round_result is not None:
            round_score = state.round_result.round_scores.get(player_id, 0)
            # Lower score is better in Jawaker Hand! Convert to positive utility
            return -float(round_score)

        hand = state.hands[player_id]
        hand_penalties = sum(c.hand_penalty_value for c in hand)
        is_opened = state.is_opened[player_id]

        score = -float(hand_penalties)
        if is_opened:
            score += 150.0  # Safe from unopened penalty
        else:
            score -= 100.0  # Threat of unopened penalty

        # Opponent threat: check if any opponent is close to emptying hand
        min_opp_cards = min(
            len(state.hands[p]) for p in range(state.num_players) if p != player_id
        )
        if min_opp_cards <= 3 and not is_opened:
            score -= 200.0  # Immediate danger of taking 100/200 pts penalty!

        return score
