"""WebSocket Game Server bridging the Python Hand Engine with Godot 4 Client."""

from __future__ import annotations
import asyncio
import json
import websockets
from websockets.exceptions import ConnectionClosed
import time
from typing import Optional

from ..engine.card import Card
from ..engine.state import TurnPhase, GameState, Action, ActionType
from ..engine.rules import GameRules, MatchState
from ..agents.heuristic_agent import HeuristicAgent
from ..agents.ismcts_agent import ISMCTSAgent
from ..agents.apex_grandmaster_agent import ApexGrandmasterAgent
from ..persistence.db import ExperienceDB
from ..persistence.trace import DecisionTrace
from .bridge import player_view_to_dict, action_to_dict, round_result_to_dict


class GameSession:
    """Manages active match state and agent sessions for one Godot client."""

    def __init__(self, db: Optional[ExperienceDB] = None, num_players: int = 2, total_rounds: int = 5):
        self.db = db if db is not None else ExperienceDB(":memory:")
        self.num_players = num_players
        self.total_rounds = total_rounds
        self.current_match_id = f"match_{int(time.time())}"
        self.match_traces: list[DecisionTrace] = []
        self.match_state: Optional[MatchState] = None
        self.state: Optional[GameState] = None
        self.ai_agents = {}
        self.player_names = {0: "You"}

        # Initialize Apex Grandmaster AI
        apex_ai = ApexGrandmasterAgent(player_id=1, name="AI Grandmaster")
        self.ai_agents[1] = apex_ai
        self.player_names[1] = apex_ai.name

        for p in range(2, num_players):
            h_ai = HeuristicAgent(player_id=p, name=f"AI Tactician {p}")
            self.ai_agents[p] = h_ai
            self.player_names[p] = h_ai.name

    def start_new_match(self) -> None:
        self.current_match_id = f"match_{int(time.time())}"
        self.match_traces = []
        self.match_state = MatchState(
            num_players=self.num_players,
            rules=GameRules(total_rounds=self.total_rounds),
            player_names=self.player_names
        )
        self.state = GameState.deal_new_round(num_players=self.num_players, dealer=self.match_state.current_dealer)

    def start_next_round(self) -> None:
        if self.match_state and not self.match_state.is_match_over:
            self.state = GameState.deal_new_round(num_players=self.num_players, dealer=self.match_state.current_dealer)


class GameServer:
    """WebSocket server listening for Godot 4 client connections."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765, db_path: str = "experience.db"):
        self.host = host
        self.port = port
        self.db = ExperienceDB(db_path)
        self.session = GameSession(db=self.db)

    async def start(self) -> None:
        print(f"[*] Starting Jawaker Hand WebSocket Server on ws://{self.host}:{self.port}...", flush=True)
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"[+] Server listening! Ready for Godot 4 client connection.", flush=True)
            await asyncio.Future()

    async def handle_client(self, websocket: websockets.WebSocketServerProtocol) -> None:
        print(f"[+] Client connected from {websocket.remote_address}!", flush=True)
        try:
            async for raw_message in websocket:
                try:
                    data = json.loads(raw_message)
                    event_type = data.get("event")

                    if event_type == "START_MATCH":
                        num_p = data.get("num_players", 2)
                        self.session = GameSession(db=self.db, num_players=num_p)
                        self.session.start_new_match()
                        await self.send_state(websocket)
                        await self.process_ai_turns_if_needed(websocket)

                    elif event_type == "NEXT_ROUND":
                        if self.session.match_state and not self.session.match_state.is_match_over:
                            self.session.start_next_round()
                            await self.send_state(websocket)
                            await self.process_ai_turns_if_needed(websocket)

                    elif event_type == "PLAYER_ACTION":
                        action_index = data.get("action_index")
                        await self.handle_human_action(websocket, action_index)

                    elif event_type == "DRAW_STOCK":
                        await self.handle_draw_stock(websocket)

                    elif event_type == "DRAW_DISCARD":
                        await self.handle_draw_discard(websocket)

                    elif event_type == "DISCARD_CARD_ID":
                        card_id = data.get("card_id")
                        await self.handle_human_discard_card_id(websocket, card_id)

                    elif event_type == "GET_CURRENT_TRACES":
                        traces_data = [t.to_dict() for t in self.session.match_traces]
                        try:
                            await websocket.send(json.dumps({
                                "event": "MATCH_TRACES",
                                "match_id": self.session.current_match_id,
                                "traces": traces_data
                            }))
                        except ConnectionClosed:
                            pass

                    elif event_type == "GET_MATCH_HISTORY":
                        matches_list = self.db.get_all_matches()
                        try:
                            await websocket.send(json.dumps({
                                "event": "MATCH_HISTORY",
                                "matches": matches_list
                            }))
                        except ConnectionClosed:
                            pass

                    elif event_type == "GET_MATCH_TRACES":
                        match_id = data.get("match_id", "")
                        if match_id and match_id != self.session.current_match_id:
                            db_traces = self.db.get_traces_for_match(match_id)
                            traces_data = [t.to_dict() for t in db_traces]
                        else:
                            traces_data = [t.to_dict() for t in self.session.match_traces]
                        try:
                            await websocket.send(json.dumps({
                                "event": "MATCH_TRACES",
                                "match_id": match_id or self.session.current_match_id,
                                "traces": traces_data
                            }))
                        except ConnectionClosed:
                            pass

                except Exception as ex:
                    print(f"[-] Error processing message: {ex}", flush=True)
                    try:
                        await websocket.send(json.dumps({"event": "ERROR", "message": str(ex)}))
                    except Exception:
                        break

        except ConnectionClosed:
            print(f"[*] Client disconnected from {websocket.remote_address}", flush=True)
        except Exception as ex:
            print(f"[*] Client connection terminated: {ex}", flush=True)

    async def send_state(self, websocket: websockets.WebSocketServerProtocol) -> None:
        if self.session.state is None:
            return

        legal = self.session.state.get_legal_actions() if not self.session.state.is_round_over else []
        view = self.session.state.get_player_view(0)
        view_dict = player_view_to_dict(view, legal)

        response = {
            "event": "STATE_UPDATE",
            "state": view_dict,
            "match": {
                "round_number": self.session.match_state.rounds_played + 1 if self.session.match_state else 1,
                "total_rounds": self.session.total_rounds,
                "scores": self.session.match_state.cumulative_scores if self.session.match_state else {0: 0, 1: 0},
                "dealer_id": self.session.match_state.current_dealer if self.session.match_state else 0
            }
        }
        try:
            await websocket.send(json.dumps(response))
        except ConnectionClosed:
            pass

    async def handle_human_action(self, websocket: websockets.WebSocketServerProtocol, action_index: Optional[int]) -> None:
        if self.session.state is None or self.session.state.is_round_over:
            return
        if self.session.state.current_player != 0:
            return

        legal = self.session.state.get_legal_actions()
        if action_index is None or not (0 <= action_index < len(legal)):
            return

        chosen_action = legal[action_index]
        self.session.state.apply_action(chosen_action)

        try:
            await websocket.send(json.dumps({
                "event": "ACTION_NOTIFICATION",
                "player_id": 0,
                "agent_name": "You",
                "action": action_to_dict(chosen_action, action_index),
                "latency_ms": 0.0
            }))
        except ConnectionClosed:
            return

        await self.send_state(websocket)

        if self.session.state.is_round_over:
            await self.handle_round_over(websocket)
        else:
            await self.process_ai_turns_if_needed(websocket)

    async def handle_draw_stock(self, websocket: websockets.WebSocketServerProtocol) -> None:
        if self.session.state is None or self.session.state.is_round_over:
            return
        if self.session.state.current_player != 0 or self.session.state.phase != TurnPhase.DRAW:
            return
        if not self.session.state.stock:
            return

        act = Action.draw_stock()
        self.session.state.apply_action(act)

        try:
            await websocket.send(json.dumps({
                "event": "ACTION_NOTIFICATION",
                "player_id": 0,
                "agent_name": "You",
                "action": action_to_dict(act, 0),
                "latency_ms": 0.0
            }))
        except ConnectionClosed:
            return

        await self.send_state(websocket)

    async def handle_draw_discard(self, websocket: websockets.WebSocketServerProtocol) -> None:
        if self.session.state is None or self.session.state.is_round_over:
            return
        if self.session.state.current_player != 0 or self.session.state.phase != TurnPhase.DRAW:
            return
        if not self.session.state.discard_pile:
            return

        act = Action.draw_discard()
        self.session.state.apply_action(act)

        try:
            await websocket.send(json.dumps({
                "event": "ACTION_NOTIFICATION",
                "player_id": 0,
                "agent_name": "You",
                "action": action_to_dict(act, 0),
                "latency_ms": 0.0
            }))
        except ConnectionClosed:
            return

        await self.send_state(websocket)

    async def handle_human_discard_card_id(self, websocket: websockets.WebSocketServerProtocol, card_id: Optional[int]) -> None:
        if self.session.state is None or self.session.state.is_round_over:
            return
        if self.session.state.current_player != 0:
            return
        if card_id is None:
            return

        # If in DRAW phase, auto-draw first from stock!
        if self.session.state.phase == TurnPhase.DRAW:
            legal = self.session.state.get_legal_actions()
            draw_act = next((a for a in legal if a.action_type == ActionType.DRAW_STOCK), None)
            if draw_act is not None:
                self.session.state.apply_action(draw_act)

        # If in MELD phase, pass meld phase to advance to DISCARD
        if self.session.state.phase == TurnPhase.MELD:
            self.session.state.drawn_from_discard_this_turn = None
            self.session.state.phase = TurnPhase.DISCARD

        if self.session.state.phase != TurnPhase.DISCARD:
            return

        hand = self.session.state.hands[0]
        matched_card = next((c for c in hand if c.id == card_id), None)
        if matched_card is not None:
            act = Action.discard(matched_card)
        else:
            legal = self.session.state.get_legal_actions()
            act = next((a for a in legal if a.action_type == ActionType.DISCARD), None)

        if act is not None:
            self.session.state.apply_action(act)

            try:
                await websocket.send(json.dumps({
                    "event": "ACTION_NOTIFICATION",
                    "player_id": 0,
                    "agent_name": "You",
                    "action": action_to_dict(act, 0),
                    "latency_ms": 0.0
                }))
            except ConnectionClosed:
                return

            await self.send_state(websocket)

            if self.session.state.is_round_over:
                await self.handle_round_over(websocket)
            else:
                await self.process_ai_turns_if_needed(websocket)

    async def process_ai_turns_if_needed(self, websocket: websockets.WebSocketServerProtocol) -> None:
        loop_guard = 0
        while (
            self.session.state is not None and
            not self.session.state.is_round_over and
            self.session.state.current_player != 0 and
            loop_guard < 12
        ):
            loop_guard += 1
            curr_p = self.session.state.current_player
            agent = self.session.ai_agents.get(curr_p)
            view = self.session.state.get_player_view(curr_p)
            legal = self.session.state.get_legal_actions()

            if not legal:
                break

            await asyncio.sleep(0.2)

            try:
                if agent is not None:
                    act, trace = agent.select_action(view, legal)
                else:
                    act = legal[0]
                    trace = None
            except Exception as ex:
                print(f"[!] AI action error: {ex}. Using safe move fallback.", flush=True)
                if view.phase == TurnPhase.DRAW:
                    act = next((a for a in legal if a.action_type == ActionType.DRAW_STOCK), legal[0])
                elif view.phase == TurnPhase.MELD:
                    act = next((a for a in legal if a.action_type == ActionType.PASS_MELD), legal[0])
                else:
                    act = legal[0]
                trace = None

            self.session.state.apply_action(act)

            if trace is not None:
                trace.match_id = self.session.current_match_id
                trace.round_number = self.session.match_state.rounds_played + 1 if self.session.match_state else 1
                self.session.match_traces.append(trace)
                try:
                    self.db.save_decision_trace(trace)
                except Exception:
                    pass

            latency = trace.execution_latency_ms if trace else 0.1
            agent_name = agent.name if agent else "AI"
            try:
                await websocket.send(json.dumps({
                    "event": "ACTION_NOTIFICATION",
                    "player_id": curr_p,
                    "agent_name": agent_name,
                    "action": action_to_dict(act, 0),
                    "latency_ms": latency
                }))
                await self.send_state(websocket)
            except ConnectionClosed:
                break

            if self.session.state.is_round_over:
                await self.handle_round_over(websocket)
                break

        # If loop_guard hit limit, force AI discard to guarantee human gets the turn!
        if (
            self.session.state is not None and
            not self.session.state.is_round_over and
            self.session.state.current_player != 0
        ):
            curr_p = self.session.state.current_player
            hand = self.session.state.hands.get(curr_p, [])
            if hand:
                self.session.state.phase = TurnPhase.DISCARD
                forced_act = Action.discard(hand[0])
                self.session.state.apply_action(forced_act)
                try:
                    await websocket.send(json.dumps({
                        "event": "ACTION_NOTIFICATION",
                        "player_id": curr_p,
                        "agent_name": "AI Grandmaster",
                        "action": action_to_dict(forced_act, 0),
                        "latency_ms": 0.1
                    }))
                    await self.send_state(websocket)
                except ConnectionClosed:
                    pass

    async def handle_round_over(self, websocket: websockets.WebSocketServerProtocol) -> None:
        res = self.session.state.round_result
        if res is not None and self.session.match_state is not None:
            self.session.match_state.record_round_result(res)
            res_dict = round_result_to_dict(res, self.session.player_names)

            is_match_over = self.session.match_state.is_match_over
            match_summary = self.session.match_state.get_final_summary() if is_match_over else None

            response = {
                "event": "ROUND_OVER",
                "round_result": res_dict,
                "cumulative_scores": self.session.match_state.cumulative_scores,
                "is_match_over": is_match_over,
                "match_summary": match_summary.summary_text if match_summary else None
            }
            try:
                await websocket.send(json.dumps(response))
            except ConnectionClosed:
                pass


def run_server(host: str = "127.0.0.1", port: int = 8765, db_path: str = "experience.db") -> None:
    server = GameServer(host=host, port=port, db_path=db_path)
    asyncio.run(server.start())


if __name__ == "__main__":
    run_server()
