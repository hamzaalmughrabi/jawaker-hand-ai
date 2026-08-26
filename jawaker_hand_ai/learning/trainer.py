"""Self-Play and Curriculum Reinforcement Learning training pipeline for championship-level agents."""

from __future__ import annotations
import random
import time
import numpy as np
from pathlib import Path
from typing import Optional
from .network import NeuralValueNetwork
from ..agents.deep_rl_agent import DeepRLAgent
from ..agents.greedy_agent import GreedyAgent
from ..agents.heuristic_agent import HeuristicAgent
from ..engine.state import GameState
from ..arena.match import MatchRunner
from ..engine.rules import GameRules


class SelfPlayTrainer:
    """Trains DeepRLAgent via self-play and expert curriculum against HeuristicGrandmaster."""

    def __init__(
        self,
        network: Optional[NeuralValueNetwork] = None,
        learning_rate: float = 0.002,
        batch_size: int = 64,
        save_path: str | Path = "models/jawaker_champion_v1.json",
        rng: Optional[random.Random] = None
    ):
        self.network = network or NeuralValueNetwork(seed=42)
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.save_path = Path(save_path)
        self.rng = rng or random.Random()
        self.feature_extractor = DeepRLAgent(name="extractor", player_id=0, network=self.network)

    def train_curriculum(
        self,
        num_games: int = 300,
        num_players: int = 2,
        eval_interval: int = 50
    ) -> dict[str, list[float]]:
        """Curriculum learning: interleaves self-play with sparring against HeuristicGrandmaster."""
        print(f"[*] Starting Championship Curriculum Training: {num_games} games ({num_players} players/match)...", flush=True)
        self.save_path.parent.mkdir(parents=True, exist_ok=True)

        history: dict[str, list[float]] = {"loss": [], "eval_winrate": []}
        experience_buffer: list[tuple[np.ndarray, float]] = []

        start_time = time.perf_counter()
        heuristic_sparring = HeuristicAgent(name="Sparring_Heuristic", player_id=1)

        for game_idx in range(1, num_games + 1):
            eps = max(0.01, 0.12 * (1.0 - game_idx / num_games))

            # 50% Self-play, 50% Sparring against Heuristic Master
            if game_idx % 2 == 0:
                agents = [
                    DeepRLAgent(name="DeepRL_P0", player_id=0, network=self.network, epsilon=eps, rng=self.rng),
                    DeepRLAgent(name="DeepRL_P1", player_id=1, network=self.network, epsilon=eps, rng=self.rng)
                ]
            else:
                agents = [
                    DeepRLAgent(name="DeepRL_P0", player_id=0, network=self.network, epsilon=eps, rng=self.rng),
                    heuristic_sparring
                ]

            state = GameState.deal_new_round(num_players=num_players, dealer=game_idx % num_players, rng=self.rng)
            game_trajectories: dict[int, list[np.ndarray]] = {0: []}

            while not state.is_round_over and state.turn_number < 90:
                curr_p = state.current_player
                agent = agents[curr_p]
                view = state.get_player_view(curr_p)
                legal = state.get_legal_actions()
                if not legal:
                    break

                act, _ = agent.select_action(view, legal)
                if curr_p == 0:
                    feat = self.feature_extractor.extract_features(view, act)
                    game_trajectories[0].append(feat)

                state.apply_action(act)

            if not state.is_round_over:
                state._resolve_stock_exhausted()

            res = state.round_result
            if res is not None:
                final_score = float(res.round_scores.get(0, 50))
                for feat in game_trajectories[0]:
                    experience_buffer.append((feat, final_score))

            # Mini-batch gradient update
            if len(experience_buffer) >= self.batch_size:
                batch = self.rng.sample(experience_buffer, self.batch_size)
                X_batch = np.array([item[0] for item in batch], dtype=np.float64)
                y_batch = np.array([item[1] for item in batch], dtype=np.float64)

                loss = self.network.train_step(X_batch, y_batch, lr=self.learning_rate)
                history["loss"].append(loss)

                if len(experience_buffer) > 4000:
                    experience_buffer = experience_buffer[-2000:]

            if game_idx % 25 == 0 or game_idx == num_games:
                elapsed = time.perf_counter() - start_time
                avg_loss = float(np.mean(history["loss"][-20:])) if history["loss"] else 0.0
                speed = game_idx / max(0.001, elapsed)
                print(
                    f"  -> Progress: {game_idx:03d}/{num_games:03d} games | Loss: {avg_loss:.2f} | Speed: {speed:.1f} games/sec",
                    flush=True
                )

            if game_idx % eval_interval == 0 or game_idx == num_games:
                win_rate = self._evaluate_against_baselines(num_rounds=10, num_players=num_players)
                history["eval_winrate"].append(win_rate)
                print(f"  [Checkpoint {game_idx:03d}] WinRate vs Greedy: {win_rate*100:.1f}%", flush=True)
                self.network.save(self.save_path)

        total_time = time.perf_counter() - start_time
        print(f"\n[+] Curriculum training completed in {total_time:.1f}s! Checkpoint saved to '{self.save_path}'", flush=True)
        return history

    def _evaluate_against_baselines(self, num_rounds: int = 10, num_players: int = 2) -> float:
        eval_agent = DeepRLAgent(name="DeepRL_Eval", player_id=0, network=self.network, epsilon=0.0)
        opp_agent = GreedyAgent(name="Greedy_Opp", player_id=1)
        runner = MatchRunner(rng=self.rng)
        wins = 0

        for r_idx in range(num_rounds):
            r_res = runner.play_round(agents=[eval_agent, opp_agent], round_number=r_idx + 1)
            if r_res.winner_id == 0:
                wins += 1

        return wins / num_rounds
