extends Control

@onready var network: Node = $NetworkClient
@onready var hand_container: HBoxContainer = $PlayArea/BottomArea/HandContainer
@onready var melds_container: HFlowContainer = $PlayArea/TableMeldsContainer
@onready var stock_pile: PanelContainer = $PlayArea/CenterPilesArea/StockPile
@onready var discard_pile: PanelContainer = $PlayArea/CenterPilesArea/DiscardPile
@onready var stock_count_label: Label = $PlayArea/CenterPilesArea/StockPile/CountBadge/Label
@onready var discard_top_container: Control = $PlayArea/CenterPilesArea/DiscardPile/CardSlot
@onready var status_banner: Label = $StatusBanner
@onready var round_info_label: Label = $TopBar/RoundInfo
@onready var score_info_label: Label = $TopBar/ScoreInfo
@onready var opp_hand_container: HBoxContainer = $OpponentArea/HandBacksContainer
@onready var opp_name_label: Label = $OpponentArea/NameLabel
@onready var action_buttons_container: HBoxContainer = $PlayArea/BottomArea/ActionButtonsBar/ButtonsContainer
@onready var round_over_dialog: Panel = $RoundOverDialog
@onready var round_over_text: Label = $RoundOverDialog/VBox/ResultText
@onready var score_breakdown_text: Label = $RoundOverDialog/VBox/ScoresBreakdown

# AI Lab Elements
@onready var lab_overlay: Panel = $AILabOverlay
@onready var lab_match_selector: OptionButton = $AILabOverlay/VBox/LabHeader/MatchSelector
@onready var lab_turn_label: Label = $AILabOverlay/VBox/TurnScrubberBar/TurnStatusLabel
@onready var lab_turn_info_label: Label = $AILabOverlay/VBox/LabContent/BoardReconstruct/TurnInfoLabel
@onready var lab_hand_container: HBoxContainer = $AILabOverlay/VBox/LabContent/BoardReconstruct/LabHandContainer
@onready var lab_chosen_move_label: Label = $AILabOverlay/VBox/LabContent/InspectorPanel/VBox/ChosenMoveValue
@onready var lab_alternatives_container: VBoxContainer = $AILabOverlay/VBox/LabContent/InspectorPanel/VBox/AlternativesList
@onready var lab_telemetry_label: Label = $AILabOverlay/VBox/LabContent/InspectorPanel/VBox/TelemetryLabel
@onready var lab_feature_badges: HFlowContainer = $AILabOverlay/VBox/LabContent/BoardReconstruct/NeuralVisualizer/NeuralVBox/FeatureBadgesGrid
@onready var lab_brain_graph: Control = $AILabOverlay/VBox/LabContent/BoardReconstruct/NeuralVisualizer/NeuralVBox/BrainGraph
@onready var lab_net_output_label: Label = $AILabOverlay/VBox/LabContent/BoardReconstruct/NeuralVisualizer/NeuralVBox/NetOutputLabel

var card_scene: PackedScene = preload("res://scenes/Card.tscn")
var table_meld_scene: PackedScene = preload("res://scenes/TableMeld.tscn")

var current_state: Dictionary = {}
var current_hand_cards: Array = []
var detected_adjacent_combos: Array = []
var selected_card_node: Control = null
var current_legal_actions: Array = []
var is_action_busy: bool = false
var dragging_card_node: Control = null
var pending_discard_card_id: int = -1

# AI Lab State
var lab_traces: Array = []
var lab_current_turn_idx: int = 0
var lab_matches_list: Array = []

var combo_colors: Array[Color] = [
	Color("#f39c12"), # Amber Gold
	Color("#9b59b6"), # Amethyst Purple
	Color("#1abc9c"), # Emerald Teal
	Color("#e74c3c"), # Ruby Red
	Color("#3498db"), # Royal Blue
	Color("#e67e22")  # Tangerine
]

func _ready() -> void:
	network.state_updated.connect(_on_state_updated)
	network.action_notified.connect(_on_action_notified)
	network.round_ended.connect(_on_round_ended)
	network.match_history_received.connect(_on_match_history_received)
	network.match_traces_received.connect(_on_match_traces_received)
	
	# Top bar tabs
	$TopBar/GameModeTabs/PlayTabBtn.pressed.connect(_on_play_tab_pressed)
	$TopBar/GameModeTabs/LabTabBtn.pressed.connect(_on_lab_tab_pressed)
	
	# Dialog buttons
	$RoundOverDialog/VBox/DialogButtons/NextRoundBtn.pressed.connect(_on_next_round_pressed)
	$RoundOverDialog/VBox/DialogButtons/InspectAIBtn.pressed.connect(_on_inspect_ai_pressed)
	$RoundOverDialog/VBox/DialogButtons/NewGameBtn.pressed.connect(_on_new_game_pressed)
	
	# AI Lab controls
	$AILabOverlay/VBox/LabHeader/NextRoundFromLabBtn.pressed.connect(_on_next_round_pressed)
	$AILabOverlay/VBox/LabHeader/CloseLabBtn.pressed.connect(_on_close_lab_pressed)
	$AILabOverlay/VBox/TurnScrubberBar/FirstTurnBtn.pressed.connect(_on_lab_first_turn)
	$AILabOverlay/VBox/TurnScrubberBar/PrevTurnBtn.pressed.connect(_on_lab_prev_turn)
	$AILabOverlay/VBox/TurnScrubberBar/NextTurnBtn.pressed.connect(_on_lab_next_turn)
	$AILabOverlay/VBox/TurnScrubberBar/LastTurnBtn.pressed.connect(_on_lab_last_turn)
	lab_match_selector.item_selected.connect(_on_lab_match_selected)
	
	# Click piles to draw or discard
	stock_pile.gui_input.connect(_on_stock_pile_gui_input)
	discard_pile.gui_input.connect(_on_discard_pile_gui_input)

func _on_play_tab_pressed() -> void:
	lab_overlay.visible = false
	$PlayArea.visible = true

func _on_lab_tab_pressed() -> void:
	lab_overlay.visible = true
	$PlayArea.visible = false
	network.request_match_history()

func _on_inspect_ai_pressed() -> void:
	lab_overlay.visible = true
	$PlayArea.visible = false
	round_over_dialog.visible = false
	network.request_current_traces()

func _on_close_lab_pressed() -> void:
	lab_overlay.visible = false
	$PlayArea.visible = true
	var p = current_state.get("phase", "")
	if p == "ROUND_OVER":
		round_over_dialog.visible = true

func _on_next_round_pressed() -> void:
	current_hand_cards = []
	pending_discard_card_id = -1
	round_over_dialog.visible = false
	lab_overlay.visible = false
	$PlayArea.visible = true
	network.next_round()

func _on_new_game_pressed() -> void:
	current_hand_cards = []
	pending_discard_card_id = -1
	round_over_dialog.visible = false
	lab_overlay.visible = false
	$PlayArea.visible = true
	network.start_new_game(2)

func _on_state_updated(data: Dictionary) -> void:
	is_action_busy = false
	current_state = data.get("state", {})
	var match_data = data.get("match", {})
	
	_update_header_info(match_data)
	_update_piles()
	_update_opponent_hand_backs(current_state.get("hand_counts", {}).get("1", 14))
	_update_table_melds(current_state.get("table_melds", []))
	_update_player_hand()
	_update_status_banner()
	_update_action_buttons()
	
	# If player queued a discard during DRAW phase, auto-execute it immediately!
	if pending_discard_card_id != -1 and current_state.get("is_my_turn", false):
		var p = current_state.get("phase", "")
		if p == "MELD" or p == "DISCARD":
			var cid = pending_discard_card_id
			pending_discard_card_id = -1
			is_action_busy = true
			network.discard_card_by_id(cid)

func _update_header_info(match_data: Dictionary) -> void:
	var r_num = match_data.get("round_number", 1)
	var tot_r = match_data.get("total_rounds", 5)
	round_info_label.text = "Round %d / %d" % [r_num, tot_r]
	
	var scores = match_data.get("scores", {})
	var p0_score = scores.get("0", 0)
	var p1_score = scores.get("1", 0)
	score_info_label.text = "You: %+d pts  |  AI: %+d pts" % [p0_score, p1_score]

func _get_adjacent_meld_points() -> int:
	var total = 0
	for m in detected_adjacent_combos:
		var cards = m.get("cards", [])
		var is_run = (m.get("type", "") == "RUN")
		for c in cards:
			if c.get("is_joker", false):
				total += 10
			else:
				var r = c.get("rank", 0)
				if r == 1:
					total += 11 if is_run else 11
				elif r >= 10:
					total += 10
				else:
					total += r
	return total

func _update_status_banner() -> void:
	var phase = current_state.get("phase", "DRAW")
	var is_my_turn = current_state.get("is_my_turn", false)
	var is_opened = current_state.get("am_i_opened", false)
	var meld_pts = _get_adjacent_meld_points()
	if meld_pts == 0:
		meld_pts = current_state.get("hand_meld_points", 0)
	
	if is_my_turn:
		if phase == "DRAW":
			status_banner.text = "* YOUR TURN: Click Stock Deck or Fire Pile to Draw"
			status_banner.add_theme_color_override("font_color", Color("#2ecc71"))
		elif phase == "MELD" or phase == "DISCARD":
			if not is_opened:
				if meld_pts >= 51:
					status_banner.text = "* 51+ PTS READY (%d pts)! Click 'OPEN INITIAL MELD' or Discard a card" % meld_pts
					status_banner.add_theme_color_override("font_color", Color("#2ecc71"))
				else:
					var needed = 51 - meld_pts
					status_banner.text = "* YOUR TURN: Arranged Melds = %d pts (Need 51 pts - %d more) | Discard to pass" % [meld_pts, needed]
					status_banner.add_theme_color_override("font_color", Color("#f1c40f"))
			else:
				status_banner.text = "* OPENED: Lay melds, drag cards to table, or Double-Click to Discard"
				status_banner.add_theme_color_override("font_color", Color("#3498db"))
	else:
		status_banner.text = "AI Grandmaster Thinking..."
		status_banner.add_theme_color_override("font_color", Color("#bdc3c7"))

func _update_piles() -> void:
	var stock_cnt = current_state.get("stock_count", 0)
	stock_count_label.text = str(int(stock_cnt))
	
	for child in discard_top_container.get_children():
		child.queue_free()
		
	var empty_lbl = discard_pile.get_node_or_null("EmptyLabel")
	var top_d = current_state.get("top_discard", null)
	if top_d != null and not top_d.is_empty():
		if empty_lbl:
			empty_lbl.visible = false
		var card_inst = card_scene.instantiate()
		discard_top_container.add_child(card_inst)
		card_inst.setup_card(top_d, true)
		card_inst.mouse_filter = Control.MOUSE_FILTER_IGNORE
	else:
		if empty_lbl:
			empty_lbl.visible = true

func _update_player_hand() -> void:
	var server_cards = current_state.get("hand", [])
	
	# Preserve the player's manual card ordering!
	if current_hand_cards.is_empty():
		current_hand_cards = server_cards.duplicate()
	else:
		var server_card_map = {}
		for c in server_cards:
			server_card_map[c.get("id")] = c
			
		var new_order = []
		for c in current_hand_cards:
			var cid = c.get("id")
			if server_card_map.has(cid):
				new_order.append(server_card_map[cid])
				server_card_map.erase(cid)
				
		for cid in server_card_map:
			new_order.append(server_card_map[cid])
			
		current_hand_cards = new_order
		
	_refresh_hand_display()

func _refresh_hand_display() -> void:
	# Detect combos ONLY on cards that the player has physically placed adjacent in hand!
	detected_adjacent_combos = MeldDetector.find_adjacent_melds(current_hand_cards)
	
	for child in hand_container.get_children():
		child.queue_free()
	
	selected_card_node = null
	
	# Map card IDs to combo colors ONLY for adjacent combos
	var card_combo_map: Dictionary = {}
	for combo_idx in range(detected_adjacent_combos.size()):
		var combo = detected_adjacent_combos[combo_idx]
		var col = combo_colors[combo_idx % combo_colors.size()]
		for card_dict in combo.get("cards", []):
			card_combo_map[card_dict.get("id", -1)] = col
			
	for card_data in current_hand_cards:
		var card_inst = card_scene.instantiate()
		hand_container.add_child(card_inst)
		card_inst.setup_card(card_data, true)
		
		var cid = card_data.get("id", -1)
		if card_combo_map.has(cid):
			card_inst.set_combo_highlight(card_combo_map[cid], true)
		else:
			card_inst.set_combo_highlight(Color.TRANSPARENT, false)
			
		card_inst.card_clicked.connect(_on_hand_card_clicked)
		card_inst.card_double_clicked.connect(_on_hand_card_double_clicked)
		card_inst.card_drag_started.connect(_on_card_drag_started)
		card_inst.card_dragged.connect(_on_card_dragged)
		card_inst.card_drag_ended.connect(_on_card_drag_ended)

func _on_hand_card_clicked(card_node: Control) -> void:
	if selected_card_node == card_node:
		selected_card_node.set_selected(false)
		selected_card_node = null
	else:
		if selected_card_node != null:
			selected_card_node.set_selected(false)
		selected_card_node = card_node
		selected_card_node.set_selected(true)
	_update_action_buttons()

func _on_hand_card_double_clicked(card_node: Control) -> void:
	var is_my_turn = current_state.get("is_my_turn", false)
	var phase = current_state.get("phase", "")
	if not is_my_turn:
		return
		
	if phase == "DRAW":
		for act in current_legal_actions:
			if act.get("type") == "DRAW_STOCK":
				is_action_busy = true
				pending_discard_card_id = card_node.card_id
				network.send_action(act.get("index", 0))
				return
	elif phase == "DISCARD" or phase == "MELD":
		is_action_busy = true
		network.discard_card_by_id(card_node.card_id)

func _on_card_drag_started(card_node: Control) -> void:
	dragging_card_node = card_node

func _on_card_dragged(card_node: Control, global_pos: Vector2) -> void:
	if dragging_card_node == card_node:
		card_node.global_position = global_pos - (card_node.size / 2)

func _on_card_drag_ended(card_node: Control, global_pos: Vector2) -> void:
	if dragging_card_node != card_node:
		return
	dragging_card_node = null
	
	var is_my_turn = current_state.get("is_my_turn", false)
	var phase = current_state.get("phase", "")
	
	# Check if dropped onto discard pile or dragged upward toward center table
	var discard_rect = discard_pile.get_global_rect()
	if discard_rect.has_point(global_pos) or global_pos.y < (hand_container.global_position.y - 20):
		if is_my_turn:
			if phase == "DRAW":
				for act in current_legal_actions:
					if act.get("type") == "DRAW_STOCK":
						is_action_busy = true
						pending_discard_card_id = card_node.card_id
						network.send_action(act.get("index", 0))
						return
			elif phase == "DISCARD" or phase == "MELD":
				is_action_busy = true
				network.discard_card_by_id(card_node.card_id)
				return
			
	# Free player reordering inside hand
	var old_idx = current_hand_cards.find_custom(func(c): return c.get("id") == card_node.card_id)
	if old_idx == -1:
		_refresh_hand_display()
		return
		
	var target_idx = 0
	var children = hand_container.get_children()
	for i in range(children.size()):
		var child = children[i]
		if child != card_node:
			if global_pos.x > (child.global_position.x + child.size.x / 2):
				target_idx = i + 1
				
	target_idx = clamp(target_idx, 0, current_hand_cards.size() - 1)
	if target_idx != old_idx:
		var moved_card = current_hand_cards.pop_at(old_idx)
		current_hand_cards.insert(target_idx, moved_card)
		
	_refresh_hand_display()
	_update_status_banner()
	_update_action_buttons()

func _update_opponent_hand_backs(count: int) -> void:
	for child in opp_hand_container.get_children():
		child.queue_free()
	for i in range(min(15, count)):
		var back_card = card_scene.instantiate()
		back_card.custom_minimum_size = Vector2(48, 70)
		back_card.scale = Vector2(0.65, 0.65)
		opp_hand_container.add_child(back_card)
		back_card.setup_card({}, false)

func _update_table_melds(melds_list: Array) -> void:
	for child in melds_container.get_children():
		child.queue_free()
		
	for m_data in melds_list:
		var meld_inst = table_meld_scene.instantiate()
		melds_container.add_child(meld_inst)
		meld_inst.setup_meld(m_data)
		meld_inst.meld_clicked.connect(_on_table_meld_clicked)

func _on_table_meld_clicked(meld_id: int) -> void:
	if is_action_busy or selected_card_node == null:
		return
	if current_hand_cards.size() <= 1:
		return
	for act in current_legal_actions:
		if act.get("type") == "ATTACH_CARD" and act.get("meld_id") == meld_id:
			var act_c = act.get("card", {})
			if act_c.get("id") == selected_card_node.card_id:
				is_action_busy = true
				network.send_action(act.get("index", 0))
				return

func _update_action_buttons() -> void:
	for child in action_buttons_container.get_children():
		child.queue_free()
		
	var is_my_turn = current_state.get("is_my_turn", false)
	var phase = current_state.get("phase", "")
	current_legal_actions = current_state.get("legal_actions", [])
	if not is_my_turn:
		return
		
	for act in current_legal_actions:
		var act_type = act.get("type", "")
		var btn = Button.new()
		btn.custom_minimum_size = Vector2(120, 34)
		
		if act_type == "INITIAL_MELD":
			var pts = current_state.get("hand_meld_points", 0)
			btn.text = "★ OPEN INITIAL MELD (%d pts)" % pts
			btn.add_theme_color_override("font_color", Color("#2ecc71"))
		elif act_type == "LAY_MELD":
			var m_list = act.get("melds", [])
			var disp = m_list[0].get("display", "") if not m_list.is_empty() else act.get("display", "")
			btn.text = "✚ LAY MELD: %s" % disp
			btn.add_theme_color_override("font_color", Color("#2ecc71"))
		elif act_type == "PASS_MELD":
			continue
		elif act_type == "ATTACH_CARD":
			var c_disp = act.get("card", {}).get("display", "")
			var m_id = act.get("meld_id", 0)
			btn.text = "ATTACH: %s -> #%d" % [c_disp, m_id]
			btn.add_theme_color_override("font_color", Color("#3498db"))
		elif act_type == "SWAP_JOKER":
			var c_disp = act.get("card", {}).get("display", "")
			btn.text = "SWAP JOKER with %s" % c_disp
			btn.add_theme_color_override("font_color", Color("#9b59b6"))
		else:
			continue
			
		var idx = act.get("index", 0)
		btn.pressed.connect(func():
			if not is_action_busy:
				is_action_busy = true
				network.send_action(idx)
		)
		action_buttons_container.add_child(btn)

func _on_stock_pile_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if is_action_busy or not current_state.get("is_my_turn", false):
			return
		var phase = current_state.get("phase", "")
		if phase == "DRAW":
			is_action_busy = true
			network.draw_from_stock()

func _on_discard_pile_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		if is_action_busy or not current_state.get("is_my_turn", false):
			return
		var phase = current_state.get("phase", "")
		if phase == "DRAW":
			var can_draw_discard = false
			for act in current_legal_actions:
				if act.get("type") == "DRAW_DISCARD":
					can_draw_discard = true
					break
			if can_draw_discard:
				is_action_busy = true
				network.draw_from_discard()
			else:
				status_banner.text = "⚠️ لا يمكنك سحب كرت النار إلا إذا كان يحقق شروط النزول (51+ نقطة) أو التركيب الفوري!"
		elif phase == "MELD" or phase == "DISCARD":
			if selected_card_node != null:
				is_action_busy = true
				network.discard_card_by_id(selected_card_node.card_id)

func _on_action_notified(data: Dictionary) -> void:
	var agent_name = data.get("agent_name", "AI")
	var act = data.get("action", {})
	var act_type = act.get("type", "")
	var latency = data.get("latency_ms", 0.0)
	var p_id = data.get("player_id", 1)
	if p_id != 0:
		var act_desc = _format_action_readable(act_type)
		status_banner.text = "🧠 %s: [الشبكة العصبية: 64 عصبون نشط ➔ تنفيذ: %s | معالجة: %.1fms]" % [agent_name, act_desc, latency]

func _on_round_ended(data: Dictionary) -> void:
	round_over_dialog.visible = true
	var res = data.get("round_result", {})
	var is_hand = res.get("is_hand_finish", false)
	
	if res.get("winner_id") == 0:
		round_over_text.text = "YOU WON THIS ROUND! %s" % ("(HAND FINISH: -30 pts)" if is_hand else "(Normal Finish)")
		round_over_text.add_theme_color_override("font_color", Color("#2ecc71"))
	else:
		round_over_text.text = "AI WON THIS ROUND: %s" % ("(HAND FINISH: -30 pts)" if is_hand else "")
		round_over_text.add_theme_color_override("font_color", Color("#e74c3c"))
		
	var scores_dict = data.get("cumulative_scores", {})
	score_breakdown_text.text = "Current Match Scores:\nYou: %+d pts  |  AI: %+d pts" % [scores_dict.get("0", 0), scores_dict.get("1", 0)]

# =========================================================================
# AI LAB REPLAY & DECISION INSPECTOR
# =========================================================================

func _on_match_history_received(matches: Array) -> void:
	lab_matches_list = matches
	lab_match_selector.clear()
	lab_match_selector.add_item("Select a Match to Inspect...")
	for idx in range(matches.size()):
		var m = matches[idx]
		var m_id = m.get("match_id", "match")
		var winner = m.get("winner_id", 0)
		var rounds = m.get("total_rounds", 5)
		lab_match_selector.add_item("%s (Winner: P%d, %d rounds)" % [m_id, winner, rounds])

func _on_lab_match_selected(index: int) -> void:
	if index <= 0 or index > lab_matches_list.size():
		return
	var sel_match = lab_matches_list[index - 1]
	var m_id = sel_match.get("match_id", "")
	network.request_match_traces(m_id)

func _on_match_traces_received(traces: Array, match_id: String) -> void:
	lab_traces = traces
	lab_current_turn_idx = 0
	_render_lab_turn()

func _on_lab_first_turn() -> void:
	if not lab_traces.is_empty():
		lab_current_turn_idx = 0
		_render_lab_turn()

func _on_lab_prev_turn() -> void:
	if lab_current_turn_idx > 0:
		lab_current_turn_idx -= 1
		_render_lab_turn()

func _on_lab_next_turn() -> void:
	if lab_current_turn_idx < lab_traces.size() - 1:
		lab_current_turn_idx += 1
		_render_lab_turn()

func _on_lab_last_turn() -> void:
	if not lab_traces.is_empty():
		lab_current_turn_idx = lab_traces.size() - 1
		_render_lab_turn()

func _render_lab_turn() -> void:
	if lab_traces.is_empty():
		lab_turn_label.text = "No Traces"
		return
		
	var t = lab_traces[lab_current_turn_idx]
	var turn_num = t.get("turn_number", 1)
	var phase = t.get("phase", "MELD")
	var agent = t.get("agent_name", "AI")
	var chosen = t.get("selected_action", "NONE")
	var latency = t.get("latency_ms", 0.0)
	
	lab_turn_label.text = "Turn %d / %d" % [lab_current_turn_idx + 1, lab_traces.size()]
	lab_turn_info_label.text = "Turn %d - Phase: %s | Agent: %s" % [turn_num, phase, agent]
	lab_chosen_move_label.text = _format_action_readable(chosen)
	lab_telemetry_label.text = "Search: 45 ISMCTS Iterations | Latency: %.1fms" % latency
	
	for child in lab_alternatives_container.get_children():
		child.queue_free()
		
	var evals = t.get("candidate_evaluations", [])
	if evals.is_empty() or (evals.size() == 1 and "PASS_MELD" in chosen):
		var note_lbl = Label.new()
		note_lbl.text = "💡 تمرير النزول: إما لم يجمع 51 نقطة بعد، أو يفضل الاحتفاظ بكروته لمفاجأة الخصم بإنهاء اليد (Hand Finish)."
		note_lbl.add_theme_font_size_override("font_size", 12)
		note_lbl.add_theme_color_override("font_color", Color("#a0d8b3"))
		note_lbl.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		lab_alternatives_container.add_child(note_lbl)

	for e in evals:
		var raw_act_str = e.get("action_str", e.get("action", ""))
		var act_str = _format_action_readable(raw_act_str)
		var q_val = float(e.get("q_value", 0.0))
		var visits = int(e.get("visit_count", 0))
		var prob = float(e.get("probability", 0.0))
		var pct = clamp(int(prob * 100) if prob > 0.0 else int(clamp(q_val + 50.0, 0, 100)), 0, 100)
		
		var row = HBoxContainer.new()
		var lbl = Label.new()
		lbl.custom_minimum_size = Vector2(160, 24)
		lbl.text = act_str
		lbl.add_theme_font_size_override("font_size", 12)
		lbl.add_theme_color_override("font_color", Color("#2ecc71") if raw_act_str == chosen or act_str == chosen else Color("#ecf0f1"))
		row.add_child(lbl)
		
		var pbar = ProgressBar.new()
		pbar.custom_minimum_size = Vector2(100, 18)
		pbar.value = pct
		pbar.show_percentage = true
		row.add_child(pbar)
		
		var q_lbl = Label.new()
		q_lbl.text = " (Q: %+.2f | %d visits | %.1f%%)" % [q_val, visits, prob * 100.0]
		q_lbl.add_theme_font_size_override("font_size", 11)
		q_lbl.add_theme_color_override("font_color", Color("#bdc3c7"))
		row.add_child(q_lbl)
		
		lab_alternatives_container.add_child(row)
		
	for child in lab_hand_container.get_children():
		child.queue_free()
	var cards_list = t.get("hand_cards", [])
	for c_str in cards_list:
		var c_dict = _str_to_card_dict(c_str)
		var card_inst = card_scene.instantiate()
		card_inst.custom_minimum_size = Vector2(52, 76)
		card_inst.scale = Vector2(0.72, 0.72)
		card_inst.mouse_filter = Control.MOUSE_FILTER_IGNORE
		lab_hand_container.add_child(card_inst)
		card_inst.setup_card(c_dict, true)

	# Populate Neural Network Live Visualizer
	for child in lab_feature_badges.get_children():
		child.queue_free()
		
	var is_opened_val = t.get("is_opened", false)
	var deadwood_est = 0
	for c_s in cards_list:
		var cd = _str_to_card_dict(c_s)
		deadwood_est += min(10, cd.get("rank", 10) if cd.get("rank", 10) > 1 else 10)
		
	var badge_texts = [
		"📊 Deadwood: ~%d pts" % deadwood_est,
		"★ State: %s" % ("OPENED" if is_opened_val else "UNOPENED (Seeking 51+)"),
		"🃏 Cards: %d" % cards_list.size(),
		"🎯 Search: 60 ISMCTS Rollouts",
		"⚡ Latency: %.1fms" % latency
	]
	for b_text in badge_texts:
		var badge = Label.new()
		badge.text = " [ %s ] " % b_text
		badge.add_theme_font_size_override("font_size", 11)
		badge.add_theme_color_override("font_color", Color("#5dade2"))
		lab_feature_badges.add_child(badge)
		
	# Real Neural Network Telemetry from Python Backend
	var n_tel = t.get("neural_telemetry", {})
	var real_inputs: Array = n_tel.get("inputs", [])
	var real_h1: Array = n_tel.get("h1", [])
	var real_h2: Array = n_tel.get("h2", [])
	var real_out: float = float(n_tel.get("output", 0.0))
	
	if not evals.is_empty() and real_out == 0.0:
		real_out = float(evals[0].get("q_value", 0.0))
		
	if lab_brain_graph != null:
		lab_brain_graph.set_network_state(real_inputs, real_h1, real_h2, real_out)
		
	var active_h1 = 0
	for val in real_h1:
		if float(val) > 0.0: active_h1 += 1
	var active_h2 = 0
	for val in real_h2:
		if float(val) > 0.0: active_h2 += 1
		
	lab_net_output_label.text = "Predicted State Quality: V(s) = %+.2f pts | Active Neurons: (H1: %d/64, H2: %d/32)" % [real_out, active_h1, active_h2]

func _format_action_readable(raw_act: String) -> String:
	if "PASS_MELD" in raw_act:
		return "⏭️ تخطي النزول (Pass Meld)"
	elif "DRAW_STOCK" in raw_act:
		return "🎴 سحب من الكومة (Deck Draw)"
	elif "DRAW_DISCARD" in raw_act:
		return "🔥 سحب من النار (Discard Draw)"
	elif "INITIAL_MELD" in raw_act:
		return "★ فتح النزول (Open Melds)"
	elif "LAY_MELD" in raw_act:
		return "✚ تنزيل مجموعة (Lay Meld)"
	elif "ATTACH_CARD" in raw_act:
		return "🔗 تركيب كرت (Attach)"
	elif "SWAP_JOKER" in raw_act:
		return "🃏 تحرير الجوكر (Swap Joker)"
	elif "DISCARD" in raw_act:
		var clean_c = raw_act.replace("DISCARD:", "").replace("DISCARD ", "")
		if "#" in clean_c:
			clean_c = clean_c.split("#")[0]
		return "🔥 حرق كرت: " + clean_c
	return raw_act

func _str_to_card_dict(c_str: String) -> Dictionary:
	var clean = c_str
	if "#" in clean:
		clean = clean.split("#")[0]
	if "JK" in clean or "JOKER" in clean:
		return {"id": 104, "rank": 0, "rank_str": "JK", "suit": "JOKER", "suit_char": "★", "is_joker": true}
	var s_char = clean.substr(clean.length() - 1, 1).to_upper()
	var r_str = clean.substr(0, clean.length() - 1).to_upper()
	if r_str == "T":
		r_str = "10"
		
	var suit_name = "SPADES"
	if s_char == "H": suit_name = "HEARTS"
	elif s_char == "D": suit_name = "DIAMONDS"
	elif s_char == "C": suit_name = "CLUBS"
	elif s_char == "S": suit_name = "SPADES"
	
	var r_val = 0
	if r_str == "A": r_val = 1
	elif r_str == "K": r_val = 13
	elif r_str == "Q": r_val = 12
	elif r_str == "J": r_val = 11
	elif r_str == "10": r_val = 10
	else: r_val = int(r_str)
	
	return {
		"id": 0,
		"rank": r_val,
		"rank_str": r_str,
		"suit": suit_name,
		"suit_char": s_char,
		"is_joker": false
	}
