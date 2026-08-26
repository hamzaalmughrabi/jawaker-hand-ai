"""CLI interface for Jawaker Hand tournaments, WebSocket server for Godot 4, and training."""

from __future__ import annotations
import sys
import time
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from ..engine.rules import GameRules
from ..engine.state import GameState, TurnPhase
from ..agents.random_agent import RandomAgent
from ..agents.greedy_agent import GreedyAgent
from ..agents.heuristic_agent import HeuristicAgent
from ..agents.pimc_agent import PIMCAgent
from ..agents.ismcts_agent import ISMCTSAgent
from ..agents.rl_agent import RLAgent
from ..agents.deep_rl_agent import DeepRLAgent
from ..agents.hybrid_search_agent import HybridSearchAgent
from ..agents.apex_grandmaster_agent import ApexGrandmasterAgent
from ..learning.network import NeuralValueNetwork
from ..learning.trainer import SelfPlayTrainer
from ..learning.evolution import EvolutionaryTrainer
from ..learning.massive_trainer import MassiveScaleTrainer
from ..server.server import run_server
from ..persistence.db import ExperienceDB
from ..arena.tournament import TournamentRunner
from ..arena.ablation import AblationStudyRunner
from ..knowledge.exporter import ObsidianExporter
from .interactive import InteractiveGameRunner
from .replay import ReplayViewer
from ..persistence.session_tracker import HumanSessionTracker


def replay_cmd(args: argparse.Namespace) -> None:
    """Launch interactive AI Decision Inspector and turn replayer."""
    viewer = ReplayViewer(db_path=args.db)
    viewer.run_interactive_replay(match_id=args.match_id)


def track_cmd(args: argparse.Namespace) -> None:
    """View or record Human vs AI 100-match challenge leaderboard."""
    tracker = HumanSessionTracker(db_path=args.db)
    if args.record:
        tracker.record_match(winner=args.winner, human_score=args.human_score, ai_score=args.ai_score, rounds=args.rounds, notes=args.notes)
        print(f"[+] Match recorded successfully!")
    print(tracker.print_leaderboard())


def serve_cmd(args: argparse.Namespace) -> None:
    """Start WebSocket server for Godot 4 client."""
    run_server(host=args.host, port=args.port, db_path=args.db)


def play_cmd(args: argparse.Namespace) -> None:
    """Launch interactive Human vs Apex AI duel in terminal."""
    db = ExperienceDB(args.db)
    runner = InteractiveGameRunner(db=db)
    runner.play_1v1_human_match(total_rounds=args.rounds)


def run_tournament_cmd(args: argparse.Namespace) -> None:
    db = ExperienceDB(args.db)
    print(f"[*] Initializing Jawaker Hand tournament: {args.matches} matches, {args.players} players/match...", flush=True)

    net = NeuralValueNetwork()
    model_path = Path("models/gen_apex.json")
    if not model_path.exists():
        model_path = Path("models/jawaker_champion_v1.json")

    if model_path.exists():
        try:
            net.load(model_path)
            print(f"[+] Loaded apex champion weights from '{model_path}'", flush=True)
        except Exception:
            pass

    agent_factories = {
        "Apex_Grandmaster": lambda p: ApexGrandmasterAgent(name="Apex_Grandmaster", player_id=p, network=net, iterations=45),
        "Hybrid_ISMCTS_RL": lambda p: HybridSearchAgent(name="Hybrid_ISMCTS_RL", player_id=p, network=net, iterations=35),
        "DeepRL_ValueNet": lambda p: DeepRLAgent(name="DeepRL_ValueNet", player_id=p, network=net, epsilon=0.0),
        "Heuristic_RuleBased": lambda p: HeuristicAgent(name="Heuristic_RuleBased", player_id=p),
        "ISMCTS_Search": lambda p: ISMCTSAgent(name="ISMCTS_Search", player_id=p, iterations=20),
        "PIMC_Determinizer": lambda p: PIMCAgent(name="PIMC_Determinizer", player_id=p, num_world_samples=3),
        "Greedy_Deadwood": lambda p: GreedyAgent(name="Greedy_Deadwood", player_id=p),
        "RL_Linear_Model": lambda p: RLAgent(name="RL_Linear_Model", player_id=p),
        "Random_Baseline": lambda p: RandomAgent(name="Random_Baseline", player_id=p),
    }

    runner = TournamentRunner(agent_factories=agent_factories, db=db)
    report = runner.run_tournament(num_matches=args.matches, players_per_match=args.players)
    print("\n" + report.report_text, flush=True)

    exporter = ObsidianExporter(db=db, vault_dir=args.vault)
    counts = exporter.export_vault()
    print(f"\n[+] Obsidian Knowledge Vault updated at '{args.vault}': {counts}", flush=True)


def massive_train_cmd(args: argparse.Namespace) -> None:
    net = NeuralValueNetwork()
    trainer = MassiveScaleTrainer(network=net, model_dir=args.model_dir, learning_rate=args.lr, num_workers=args.workers)
    trainer.train_10000_games(
        total_games=args.games,
        checkpoint_interval=args.checkpoint_interval,
        batch_per_worker=args.batch_size
    )


def ablation_cmd(args: argparse.Namespace) -> None:
    net = NeuralValueNetwork()
    model_path = Path("models/gen_apex.json")
    if model_path.exists():
        try:
            net.load(model_path)
        except Exception:
            pass

    runner = AblationStudyRunner(network=net)
    report = runner.run_component_ablation(matches_per_pair=args.matches)
    print("\n" + report, flush=True)


def sweep_cmd(args: argparse.Namespace) -> None:
    net = NeuralValueNetwork()
    model_path = Path("models/gen_apex.json")
    if model_path.exists():
        try:
            net.load(model_path)
        except Exception:
            pass

    runner = AblationStudyRunner(network=net)
    report = runner.run_budget_sweep(budgets=[5, 10, 20, 40], matches_per_budget=args.matches)
    print("\n" + report, flush=True)


def evolve_cmd(args: argparse.Namespace) -> None:
    evo = EvolutionaryTrainer(model_dir=args.model_dir, learning_rate=args.lr)
    evo.run_evolution(
        generations=args.generations,
        games_per_gen=args.games,
        eval_matches=args.eval_matches,
        promotion_threshold=args.threshold
    )


def train_cmd(args: argparse.Namespace) -> None:
    net = NeuralValueNetwork()
    trainer = SelfPlayTrainer(network=net, learning_rate=args.lr, save_path=args.model)
    trainer.train_curriculum(num_games=args.games, num_players=args.players, eval_interval=args.eval_interval)


def watch_game_cmd(args: argparse.Namespace) -> None:
    print("=================================================================", flush=True)
    print("      JAWAKER HAND (هاند جواكر) - CHAMPIONSHIP MATCH SPECTATOR    ", flush=True)
    print("=================================================================\n", flush=True)

    net = NeuralValueNetwork()
    model_path = Path("models/gen_apex.json")
    if not model_path.exists():
        model_path = Path("models/jawaker_champion_v1.json")

    if model_path.exists():
        try:
            net.load(model_path)
        except Exception:
            pass

    if args.players == 2:
        print("[*] Format: 1v1 Championship Duel", flush=True)
        agents = [
            ApexGrandmasterAgent("Apex_Grandmaster", 0, network=net, iterations=45),
            HeuristicAgent("Heuristic_RuleBased", 1)
        ]
    else:
        print("[*] Format: 4-Player Table", flush=True)
        agents = [
            ApexGrandmasterAgent("Apex_Grandmaster", 0, network=net, iterations=45),
            DeepRLAgent("DeepRL_ValueNet", 1, network=net, epsilon=0.0),
            HeuristicAgent("Heuristic_RuleBased", 2),
            GreedyAgent("Greedy_Deadwood", 3)
        ]

    num_p = len(agents)
    state = GameState.deal_new_round(num_players=num_p, dealer=0)
    delay = args.delay

    print(f"[*] Upcard on fire pile: {state.discard_pile[-1].to_str(show_deck=False)}\n", flush=True)

    while not state.is_round_over:
        curr_p = state.current_player
        agent = agents[curr_p]
        view = state.get_player_view(curr_p)
        legal = state.get_legal_actions()

        if not legal:
            break

        hand_str = " ".join(c.to_str(show_deck=False) for c in view.hand)
        print(f"[Turn {state.turn_number:02d} | Phase: {state.phase.value:<7}] [{agent.name}] (Seat P{curr_p})", flush=True)
        print(f"  Hand ({len(view.hand)} cards): [{hand_str}]", flush=True)

        if state.table.melds:
            table_strs = " | ".join(f"#{tm.meld_id}: {tm.meld.to_str()}" for tm in state.table.melds)
            print(f"  Table Board: {table_strs}", flush=True)

        act, trace = agent.select_action(view, legal)
        print(f"  -> Action: {act.to_str()} (latency: {trace.execution_latency_ms:.1f}ms)", flush=True)
        print("-" * 65, flush=True)

        state.apply_action(act, verify_invariants=True)
        if delay > 0:
            time.sleep(delay)

    print("\n======================= ROUND FINISHED =======================", flush=True)
    res = state.round_result
    if res is not None:
        winner_name = agents[res.winner_id].name if res.winner_id is not None else "Draw"
        win_type = "[HAND -60pts!]" if res.is_hand_finish else "[NORMAL -30pts]"
        print(f"Winner: {winner_name} (P{res.winner_id}) {win_type}", flush=True)
        for p, score in res.round_scores.items():
            print(f"  P{p} [{agents[p].name}]: {score:+d} pts", flush=True)
    print("==============================================================", flush=True)


def export_vault_cmd(args: argparse.Namespace) -> None:
    db = ExperienceDB(args.db)
    exporter = ObsidianExporter(db=db, vault_dir=args.vault)
    counts = exporter.export_vault()
    print(f"[+] Successfully exported Obsidian Knowledge Vault to '{args.vault}'!", flush=True)
    print(f"    - Strategies: {counts['strategies']}", flush=True)
    print(f"    - Mistakes:   {counts['mistakes']}", flush=True)
    print(f"    - Game Logs:  {counts['games']}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Jawaker Hand AI Scientific Laboratory CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Server command for Godot 4
    s_parser = subparsers.add_parser("serve", help="Start WebSocket server for Godot 4 game client")
    s_parser.add_argument("--host", type=str, default="127.0.0.1", help="Server bind host")
    s_parser.add_argument("--port", type=int, default=8765, help="Server bind port")
    s_parser.add_argument("--db", type=str, default="experience.db", help="SQLite database path")
    s_parser.set_defaults(func=serve_cmd)

    # Human vs AI Play command
    p_parser = subparsers.add_parser("play", help="Play interactively against the Apex Grandmaster AI in a 1v1 duel")
    p_parser.add_argument("--rounds", type=int, default=5, help="Number of rounds in match (default: 5)")
    p_parser.add_argument("--db", type=str, default="experience.db", help="SQLite database path")
    p_parser.set_defaults(func=play_cmd)

    # Massive 10,000-game training command
    m_parser = subparsers.add_parser("massive-train", help="Run high-throughput 10,000-game championship self-play training")
    m_parser.add_argument("--games", type=int, default=10000, help="Total number of self-play games (default: 10000)")
    m_parser.add_argument("--workers", type=int, default=4, help="Number of parallel worker batches (default: 4)")
    m_parser.add_argument("--batch-size", type=int, default=25, help="Games per worker batch")
    m_parser.add_argument("--checkpoint-interval", type=int, default=1000, help="Checkpoint interval in games")
    m_parser.add_argument("--lr", type=float, default=0.002, help="Learning rate")
    m_parser.add_argument("--model-dir", type=str, default="models", help="Directory for checkpoint generations")
    m_parser.set_defaults(func=massive_train_cmd)

    # Tournament command
    t_parser = subparsers.add_parser("tournament", help="Run controlled tournament among AI architectures")
    t_parser.add_argument("--matches", type=int, default=10, help="Number of 5-round matches to play")
    t_parser.add_argument("--players", type=int, default=2, help="Number of players per match (2 for 1v1, 4 for 4-player)")
    t_parser.add_argument("--db", type=str, default="experience.db", help="SQLite database path")
    t_parser.add_argument("--vault", type=str, default="obsidian_vault", help="Obsidian vault directory")
    t_parser.set_defaults(func=run_tournament_cmd)

    # Ablation Study command
    ab_parser = subparsers.add_parser("ablation", help="Run component ablation study (ValueNet vs ISMCTS vs Hybrid)")
    ab_parser.add_argument("--matches", type=int, default=15, help="Matches per configuration pair")
    ab_parser.set_defaults(func=ablation_cmd)

    # Search Budget Sweep command
    sw_parser = subparsers.add_parser("sweep", help="Run search budget scaling sweep (K=5, 10, 20, 40)")
    sw_parser.add_argument("--matches", type=int, default=15, help="Matches per budget level")
    sw_parser.set_defaults(func=sweep_cmd)

    # Evolutionary Training command
    ev_parser = subparsers.add_parser("evolve", help="Run AlphaZero-style evolutionary self-play with gated promotion")
    ev_parser.add_argument("--generations", type=int, default=4, help="Number of generations")
    ev_parser.add_argument("--games", type=int, default=100, help="Self-play games per generation")
    ev_parser.add_argument("--eval-matches", type=int, default=10, help="Evaluation matches vs incumbent")
    ev_parser.add_argument("--threshold", type=float, default=0.55, help="Promotion threshold win rate")
    ev_parser.add_argument("--lr", type=float, default=0.002, help="Learning rate")
    ev_parser.add_argument("--model-dir", type=str, default="models", help="Directory to save generational models")
    ev_parser.set_defaults(func=evolve_cmd)

    # Train command
    tr_parser = subparsers.add_parser("train", help="Train DeepRLAgent using self-play curriculum")
    tr_parser.add_argument("--games", type=int, default=300, help="Number of curriculum training games")
    tr_parser.add_argument("--players", type=int, default=2, help="Number of players per game (2 for 1v1, 4 for 4-player)")
    tr_parser.add_argument("--lr", type=float, default=0.002, help="Learning rate")
    tr_parser.add_argument("--eval-interval", type=int, default=50, help="Evaluation interval")
    tr_parser.add_argument("--model", type=str, default="models/jawaker_champion_v1.json", help="Model checkpoint path")
    tr_parser.set_defaults(func=train_cmd)

    # Watch Live command
    w_parser = subparsers.add_parser("watch", help="Watch AI agents play a live round in real time")
    w_parser.add_argument("--players", type=int, default=2, help="Number of players (2 for 1v1, 4 for 4-player)")
    w_parser.add_argument("--delay", type=float, default=0.0, help="Delay in seconds between turns")
    w_parser.set_defaults(func=watch_game_cmd)

    # Export Vault command
    e_parser = subparsers.add_parser("export-vault", help="Export experience database to Obsidian Markdown vault")
    e_parser.add_argument("--db", type=str, default="experience.db", help="SQLite database path")
    e_parser.add_argument("--vault", type=str, default="obsidian_vault", help="Obsidian vault directory")
    e_parser.set_defaults(func=export_vault_cmd)

    # Replay & AI Lab command
    rep_parser = subparsers.add_parser("replay", help="Inspect AI decisions, alternatives, and search traces in terminal")
    rep_parser.add_argument("match_id", type=str, nargs="?", default=None, help="Match ID to inspect (optional)")
    rep_parser.add_argument("--db", type=str, default="experience.db", help="SQLite database path")
    rep_parser.set_defaults(func=replay_cmd)

    # Human vs AI 100-match tracker command
    track_parser = subparsers.add_parser("track", help="View or record Hamza vs AI 100-match challenge")
    track_parser.add_argument("--record", action="store_true", help="Record a new match result")
    track_parser.add_argument("--winner", type=str, default="Hamza", help="Winner name (Hamza / AI)")
    track_parser.add_argument("--human-score", type=int, default=0, help="Hamza final score")
    track_parser.add_argument("--ai-score", type=int, default=0, help="AI final score")
    track_parser.add_argument("--rounds", type=int, default=5, help="Rounds played")
    track_parser.add_argument("--notes", type=str, default="", help="Mistake / weakness observation notes")
    track_parser.add_argument("--db", type=str, default="experience.db", help="SQLite database path")
    track_parser.set_defaults(func=track_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
