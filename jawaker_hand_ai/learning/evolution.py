"""Apex Evolutionary Self-Play & Multi-Style Sparring Pipeline for Championship-grade Jawaker Hand AI."""

from __future__ import annotations
import copy
import json
import time
import random
import numpy as np
from pathlib import Path
from typing import Optional
from .network import NeuralValueNetwork
from ..agents.deep_rl_agent import DeepRLAgent
from ..agents.heuristic_agent import HeuristicAgent
from ..agents.greedy_agent import GreedyAgent
from ..arena.match import MatchRunner
from ..engine.state import GameState


class EvolutionaryTrainer:
    """Trains multi-generational apex models via adversarial sparring and gated tournament promotion."""

    def __init__(
        self,
        model_dir: str | Path = "models",
        learning_rate: float = 0.002,
        batch_size: int = 64,
        rng: Optional[random.Random] = None
    ):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.rng = rng or random.Random()
        self.runner = MatchRunner(rng=self.rng)

    def run_evolution(
        self,
        generations: int = 4,
        games_per_gen: int = 120,
        eval_matches: int = 8,
        promotion_threshold: float = 0.60
    ) -> list[dict]:
        print("=" * 80, flush=True)
        print("    APEX CHAMPIONSHIP EVOLUTIONARY PIPELINE (Multi-Style Sparring Pool)", flush=True)
        print("=" * 80, flush=True)
        print(f"Generations: {generations} | Games/Gen: {games_per_gen} | Promotion Threshold: {promotion_threshold*100:.0f}%\n", flush=True)

        current_champ_net = NeuralValueNetwork(seed=42)
        current_gen = 0
        champ_path = self.model_dir / f"gen_{current_gen}.json"
        current_champ_net.save(champ_path)

        evolution_log = []
        heuristic_sparring = HeuristicAgent("Sparring_Heuristic", 1)
        greedy_sparring = GreedyAgent("Sparring_Greedy", 1)

        for gen in range(1, generations + 1):
            t_gen_start = time.perf_counter()
            print(f"[*] Training Generation {gen}/{generations}...", flush=True)

            candidate_net = NeuralValueNetwork()
            candidate_net.load(champ_path)

            experience_buffer: list[tuple[np.ndarray, float]] = []

            for g_idx in range(1, games_per_gen + 1):
                eps = max(0.02, 0.12 * (1.0 - g_idx / games_per_gen))
                cand_agent = DeepRLAgent(f"Cand_Gen{gen}", 0, network=candidate_net, epsilon=eps, rng=self.rng)

                # 50% Self-play, 35% Heuristic sparring, 15% Greedy sparring
                roll = self.rng.random()
                if roll < 0.50:
                    opp_agent = DeepRLAgent(f"Champ_Gen{current_gen}", 1, network=current_champ_net, epsilon=eps, rng=self.rng)
                elif roll < 0.85:
                    opp_agent = heuristic_sparring
                else:
                    opp_agent = greedy_sparring

                state = GameState.deal_new_round(num_players=2, dealer=g_idx % 2, rng=self.rng)
                traj: list[np.ndarray] = []

                while not state.is_round_over and state.turn_number < 90:
                    curr_p = state.current_player
                    ag = cand_agent if curr_p == 0 else opp_agent
                    view = state.get_player_view(curr_p)
                    legal = state.get_legal_actions()
                    if not legal:
                        break

                    act, _ = ag.select_action(view, legal)
                    if curr_p == 0:
                        feat = cand_agent.extract_features(view, act)
                        traj.append(feat)

                    state.apply_action(act)

                if not state.is_round_over:
                    state._resolve_stock_exhausted()

                res = state.round_result
                if res is not None:
                    final_score = float(res.round_scores.get(0, 50))
                    for f in traj:
                        experience_buffer.append((f, final_score))

            # Train candidate on multi-style experience replay
            if len(experience_buffer) >= self.batch_size:
                for _ in range(60):
                    batch = self.rng.sample(experience_buffer, self.batch_size)
                    X_batch = np.array([item[0] for item in batch], dtype=np.float64)
                    y_batch = np.array([item[1] for item in batch], dtype=np.float64)
                    candidate_net.train_step(X_batch, y_batch, lr=self.learning_rate)

            # Gatekeeper Tournament (Candidate vs Incumbent)
            eval_cand = DeepRLAgent(f"Cand_Gen{gen}", 0, network=candidate_net, epsilon=0.0)
            eval_champ = DeepRLAgent(f"Champ_Gen{current_gen}", 1, network=current_champ_net, epsilon=0.0)

            wins = 0
            for m_idx in range(eval_matches):
                p0_seat = m_idx % 2
                p1_seat = 1 - p0_seat

                agents = [eval_cand, eval_champ] if p0_seat == 0 else [eval_champ, eval_cand]
                summary = self.runner.play_match(agents=agents)
                if summary.winner_id == p0_seat:
                    wins += 1

            win_rate = wins / eval_matches
            promoted = (win_rate >= promotion_threshold)

            status_str = "PROMOTED ★" if promoted else "REJECTED (Rolled back)"
            gen_dur = time.perf_counter() - t_gen_start
            print(f"  -> Gen {gen} Gatekeeper Evaluation: {wins}/{eval_matches} wins ({win_rate*100:.1f}%) | Time: {gen_dur:.1f}s -> {status_str}", flush=True)

            if promoted:
                current_gen += 1
                current_champ_net = candidate_net
                champ_path = self.model_dir / f"gen_{current_gen}.json"
                candidate_net.save(champ_path)
                candidate_net.save(self.model_dir / "gen_apex.json")
                candidate_net.save(self.model_dir / "jawaker_champion_v1.json")

            evolution_log.append({
                "gen": gen,
                "win_rate": win_rate,
                "promoted": promoted,
                "active_champion_gen": current_gen
            })

        print("\n" + "=" * 80, flush=True)
        print(f"[+] Evolutionary run complete! Apex Model: Gen {current_gen} saved to 'models/gen_apex.json'", flush=True)
        print("=" * 80, flush=True)
        return evolution_log
