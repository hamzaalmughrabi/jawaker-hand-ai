"""Unit tests for agent decision making, persistence, and Obsidian knowledge export."""

import pytest
import tempfile
import gc
from pathlib import Path
from jawaker_hand_ai.engine.state import GameState
from jawaker_hand_ai.agents.random_agent import RandomAgent
from jawaker_hand_ai.agents.greedy_agent import GreedyAgent
from jawaker_hand_ai.agents.heuristic_agent import HeuristicAgent
from jawaker_hand_ai.agents.pimc_agent import PIMCAgent
from jawaker_hand_ai.agents.ismcts_agent import ISMCTSAgent
from jawaker_hand_ai.agents.rl_agent import RLAgent
from jawaker_hand_ai.persistence.db import ExperienceDB
from jawaker_hand_ai.knowledge.exporter import ObsidianExporter
from jawaker_hand_ai.arena.match import MatchRunner


def test_agent_action_selection():
    state = GameState.deal_new_round(num_players=4, dealer=0)
    view = state.get_player_view(state.current_player)
    legal = state.get_legal_actions()

    agents = [
        RandomAgent("R", 0),
        GreedyAgent("G", 0),
        HeuristicAgent("H", 0),
        PIMCAgent("P", 0, num_world_samples=2),
        ISMCTSAgent("I", 0, iterations=10),
        RLAgent("RL", 0)
    ]

    for ag in agents:
        act, trace = ag.select_action(view, legal)
        assert act in legal
        assert trace.agent_name == ag.name


def test_end_to_end_match_and_obsidian_export():
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        db_path = Path(tmp_dir) / "test_exp.db"
        vault_path = Path(tmp_dir) / "obsidian_vault"

        db = ExperienceDB(db_path)
        agents = [
            GreedyAgent("Greedy_0", 0),
            HeuristicAgent("Heuristic_1", 1),
            RandomAgent("Random_2", 2),
            RandomAgent("Random_3", 3)
        ]

        runner = MatchRunner(db=db)
        summary = runner.play_match(agents=agents)
        assert summary.total_rounds == 5

        # Export Obsidian Vault
        exporter = ObsidianExporter(db=db, vault_dir=vault_path)
        counts = exporter.export_vault()

        assert counts["strategies"] > 0
        assert counts["games"] == 1
        assert (vault_path / "Index.md").exists()
        assert (vault_path / "Strategy" / "Opening 51 Points Strategy.md").exists()

        del db
        del runner
        del exporter
        gc.collect()
