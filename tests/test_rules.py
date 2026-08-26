"""Unit tests for Jawaker Hand match scoring, 5-round progression, and dealer rotation."""

import pytest
from jawaker_hand_ai.engine.rules import GameRules, MatchState
from jawaker_hand_ai.engine.state import RoundScoreResult


def test_5_round_match_lowest_score_wins():
    match = MatchState(num_players=4, rules=GameRules(total_rounds=5))
    assert not match.is_match_over

    # Play 5 mock rounds
    for r in range(1, 6):
        scores = {0: 10, 1: 50, 2: 100, 3: -30 if r % 2 == 0 else 20}
        res = RoundScoreResult(
            winner_id=3 if r % 2 == 0 else 0,
            is_hand_finish=False,
            is_normal_finish=True,
            is_stock_exhausted=False,
            round_scores=scores,
            unopened_players=(2,),
            remaining_hands={},
            score_breakdown=f"Round {r} complete."
        )
        match.record_round_result(res)

    assert match.is_match_over
    summary = match.get_final_summary()
    assert summary.total_rounds == 5
    # Winner has lowest score
    lowest_score = summary.rankings[0][2]
    for p, name, score in summary.rankings:
        assert score >= lowest_score
