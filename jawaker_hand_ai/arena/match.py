"""Match runner for executing complete 5-round competitive matches among named agents."""

from __future__ import annotations
import uuid
import random
from typing import Sequence, Optional
from ..engine.state import GameState, TurnPhase, RoundScoreResult
from ..engine.rules import GameRules, MatchState, MatchSummary
from ..agents.base import BaseAgent
from ..persistence.db import ExperienceDB


class MatchRunner:
    """Orchestrates 5-round competitive Jawaker Hand matches among named AI or human agents."""

    def __init__(self, db: Optional[ExperienceDB] = None, rng: Optional[random.Random] = None):
        self.db = db
        self.rng = rng or random.Random()

    def play_round(
        self,
        agents: Sequence[BaseAgent],
        dealer_id: int = 0,
        match_id: str = "MATCH",
        round_number: int = 1,
        max_turns: int = 120
    ) -> RoundScoreResult:
        num_players = len(agents)
        state = GameState.deal_new_round(num_players=num_players, dealer=dealer_id, rng=self.rng)

        for ag in agents:
            ag.reset_round()

        turn_count = 0
        while not state.is_round_over and turn_count < max_turns:
            curr_p = state.current_player
            agent = agents[curr_p]

            view = state.get_player_view(curr_p)
            legal = state.get_legal_actions()

            if not legal:
                break

            action, trace = agent.select_action(view, legal)

            if self.db is not None:
                trace.match_id = match_id
                trace.round_number = round_number
                self.db.save_decision_trace(trace)

            state.apply_action(action)
            turn_count += 1

        if not state.is_round_over:
            state._resolve_stock_exhausted()

        result = state.round_result
        if self.db is not None and result is not None:
            self.db.save_round(match_id, round_number, dealer_id, result)

        return result

    def play_match(
        self,
        agents: Sequence[BaseAgent],
        rules: Optional[GameRules] = None,
        match_id: Optional[str] = None
    ) -> MatchSummary:
        num_players = len(agents)
        rules = rules or GameRules()
        match_id = match_id or f"match_{uuid.uuid4().hex[:8]}"

        player_names = {idx: ag.name for idx, ag in enumerate(agents)}
        match_state = MatchState(num_players=num_players, rules=rules, player_names=player_names)

        for round_idx in range(1, rules.total_rounds + 1):
            dealer = match_state.current_dealer
            r_res = self.play_round(
                agents=agents,
                dealer_id=dealer,
                match_id=match_id,
                round_number=round_idx
            )
            match_state.record_round_result(r_res)

        summary = match_state.get_final_summary()

        if self.db is not None:
            self.db.save_match(match_id, num_players, summary)

        return summary
