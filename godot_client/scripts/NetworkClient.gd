extends Node

signal connected_to_server()
signal connection_failed()
signal disconnected_from_server()
signal state_updated(state_dict: Dictionary)
signal action_notified(action_dict: Dictionary)
signal round_ended(result_dict: Dictionary)
signal match_history_received(matches: Array)
signal match_traces_received(traces: Array, match_id: String)

var ws: WebSocketPeer = WebSocketPeer.new()
var is_connected_to_server: bool = false
var server_url: String = "ws://127.0.0.1:8765"
var server_pid: int = -1
var retry_timer: float = 0.0
var max_retries: int = 5
var retry_count: int = 0
var has_attempted_server_spawn: bool = false

func _ready() -> void:
	_connect_or_spawn_server()

func _connect_or_spawn_server() -> void:
	var err = ws.connect_to_url(server_url)
	if err != OK:
		_spawn_local_server()

func _spawn_local_server() -> void:
	# Auto-spawn the Python background server process with explicit root sys.path
	var root_dir = ProjectSettings.globalize_path("res://..").replace("\\", "/")
	var py_code = "import sys; sys.path.insert(0, r'%s'); from jawaker_hand_ai.cli.main import main; sys.argv=['main','serve','--port','8765']; main()" % root_dir
	var args = ["-u", "-c", py_code]
	server_pid = OS.create_process("python", args, false)
	if server_pid == -1:
		server_pid = OS.create_process("python3", args, false)

func _process(delta: float) -> void:
	ws.poll()
	var state = ws.get_ready_state()
	
	if state == WebSocketPeer.STATE_OPEN:
		if not is_connected_to_server:
			is_connected_to_server = true
			retry_count = 0
			connected_to_server.emit()
			start_match(2)
		
		while ws.get_available_packet_count() > 0:
			var packet = ws.get_packet()
			var msg_str = packet.get_string_from_utf8()
			_handle_server_message(msg_str)
			
	elif state == WebSocketPeer.STATE_CLOSED or state == WebSocketPeer.STATE_CLOSING:
		if is_connected_to_server:
			is_connected_to_server = false
			disconnected_from_server.emit()
		
		# Persistent auto-reconnect logic: keep retrying every 1.0 second
		retry_timer += delta
		if retry_timer > 1.0:
			retry_timer = 0.0
			retry_count += 1
			if retry_count % 3 == 0:
				_spawn_local_server()
			ws.connect_to_url(server_url)

func _handle_server_message(raw_json: String) -> void:
	var json = JSON.new()
	var err = json.parse(raw_json)
	if err != OK:
		return
	
	var data: Dictionary = json.data
	var event_type = data.get("event", "")
	
	if event_type == "STATE_UPDATE":
		state_updated.emit(data)
	elif event_type == "ACTION_NOTIFICATION":
		action_notified.emit(data)
	elif event_type == "ROUND_OVER":
		round_ended.emit(data)
	elif event_type == "MATCH_HISTORY" or event_type == "MATCH_HISTORY_RESPONSE":
		match_history_received.emit(data.get("matches", []))
	elif event_type == "MATCH_TRACES" or event_type == "MATCH_TRACES_RESPONSE":
		match_traces_received.emit(data.get("traces", []), data.get("match_id", ""))

func start_match(num_players: int = 2) -> void:
	send_json({
		"event": "START_MATCH",
		"num_players": num_players
	})

func start_new_game(num_players: int = 2) -> void:
	send_json({
		"event": "START_NEW_GAME",
		"num_players": num_players
	})

func next_round() -> void:
	send_json({
		"event": "NEXT_ROUND"
	})

func send_action(action_index: int) -> void:
	send_json({
		"event": "PLAYER_ACTION",
		"action_index": action_index
	})

func draw_from_stock() -> void:
	send_json({
		"event": "DRAW_STOCK"
	})

func draw_from_discard() -> void:
	send_json({
		"event": "DRAW_DISCARD"
	})

func discard_card_by_id(card_id: int) -> void:
	send_json({
		"event": "DISCARD_CARD_ID",
		"card_id": card_id
	})

func request_match_history() -> void:
	send_json({
		"event": "GET_MATCH_HISTORY"
	})

func request_match_traces(match_id: String) -> void:
	send_json({
		"event": "GET_MATCH_TRACES",
		"match_id": match_id
	})

func request_current_traces() -> void:
	send_json({
		"event": "GET_CURRENT_TRACES"
	})

func send_json(data: Dictionary) -> void:
	if ws.get_ready_state() == WebSocketPeer.STATE_OPEN:
		var json_str = JSON.stringify(data)
		ws.send_text(json_str)

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST or what == NOTIFICATION_PREDELETE:
		if server_pid > 0:
			OS.kill(server_pid)
