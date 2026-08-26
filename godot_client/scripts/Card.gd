extends Control

signal card_clicked(card_node: Control)
signal card_double_clicked(card_node: Control)
signal card_drag_started(card_node: Control)
signal card_dragged(card_node: Control, global_pos: Vector2)
signal card_drag_ended(card_node: Control, global_pos: Vector2)

@export var card_id: int = -1
@export var rank_str: String = "A"
@export var suit_name: String = "SPADES"
@export var is_joker: bool = false
@export var is_face_up: bool = true
@export var is_selected: bool = false

var base_y: float = 0.0
var hover_offset: float = -14.0
var selected_offset: float = -28.0

var is_dragging: bool = false
var drag_start_mouse_pos: Vector2 = Vector2.ZERO
var drag_threshold: float = 8.0

@onready var bg_panel: Panel = $Background
@onready var top_left_rank: Label = $TopLeft/Rank
@onready var top_left_suit: Label = $TopLeft/Suit
@onready var center_icon: Label = $CenterArea/CenterIcon
@onready var court_label: Label = $CenterArea/CourtLabel
@onready var bot_right_rank: Label = $BottomRight/Rank
@onready var bot_right_suit: Label = $BottomRight/Suit
@onready var back_panel: Panel = $BackPanel
@onready var combo_border: Panel = $ComboBorder

var suit_symbols: Dictionary = {
	"SPADES": "♠",
	"HEARTS": "♥",
	"DIAMONDS": "♦",
	"CLUBS": "♣",
	"JOKER": "★"
}

# Standard Jawaker 4-Color Luxury Palette
var suit_colors: Dictionary = {
	"SPADES": Color("#1e272e"),    # Carbon Velvet Black
	"HEARTS": Color("#e74c3c"),    # Ruby Red
	"DIAMONDS": Color("#0984e3"),  # Royal Sapphire Blue
	"CLUBS": Color("#009432"),     # Emerald Casino Green
	"JOKER": Color("#8e44ad")      # Royal Amethyst Purple
}

func _ready() -> void:
	gui_input.connect(_on_gui_input)
	mouse_entered.connect(_on_mouse_entered)
	mouse_exited.connect(_on_mouse_exited)
	update_visuals()

func setup_card(data: Dictionary, face_up: bool = true) -> void:
	card_id = data.get("id", -1)
	var raw_rank = data.get("rank_str", "")
	rank_str = "10" if (raw_rank == "T" or raw_rank == "10" or data.get("rank", 0) == 10) else raw_rank
	suit_name = data.get("suit", "SPADES")
	is_joker = data.get("is_joker", false)
	is_face_up = face_up
	update_visuals()

func update_visuals() -> void:
	if not is_inside_tree():
		return
		
	if not is_face_up:
		back_panel.visible = true
		$TopLeft.visible = false
		$CenterArea.visible = false
		$BottomRight.visible = false
		combo_border.visible = false
		return
		
	back_panel.visible = false
	$TopLeft.visible = true
	$CenterArea.visible = true
	$BottomRight.visible = true
	
	var sym = suit_symbols.get(suit_name, "♠")
	var col = suit_colors.get(suit_name, Color.BLACK)
	
	top_left_rank.add_theme_color_override("font_color", col)
	top_left_suit.add_theme_color_override("font_color", col)
	center_icon.add_theme_color_override("font_color", col)
	bot_right_rank.add_theme_color_override("font_color", col)
	bot_right_suit.add_theme_color_override("font_color", col)
	
	if is_joker:
		top_left_rank.text = "JK"
		top_left_suit.text = "★"
		center_icon.text = "★"
		center_icon.add_theme_font_size_override("font_size", 36)
		court_label.visible = true
		court_label.text = "JOKER"
		court_label.add_theme_color_override("font_color", Color("#f1c40f"))
		bot_right_rank.text = "JK"
		bot_right_suit.text = "★"
	else:
		top_left_rank.text = rank_str
		top_left_suit.text = sym
		bot_right_rank.text = rank_str
		bot_right_suit.text = sym
		
		var r_upper = rank_str.to_upper()
		if r_upper == "K":
			center_icon.text = "♚"
			center_icon.add_theme_font_size_override("font_size", 34)
			court_label.visible = true
			court_label.text = "KING"
			court_label.add_theme_color_override("font_color", col)
		elif r_upper == "Q":
			center_icon.text = "♛"
			center_icon.add_theme_font_size_override("font_size", 34)
			court_label.visible = true
			court_label.text = "QUEEN"
			court_label.add_theme_color_override("font_color", col)
		elif r_upper == "J":
			center_icon.text = "♝"
			center_icon.add_theme_font_size_override("font_size", 34)
			court_label.visible = true
			court_label.text = "JACK"
			court_label.add_theme_color_override("font_color", col)
		elif r_upper == "A":
			center_icon.text = sym
			center_icon.add_theme_font_size_override("font_size", 38)
			court_label.visible = false
		else:
			center_icon.text = sym
			center_icon.add_theme_font_size_override("font_size", 34)
			court_label.visible = false

func set_combo_highlight(col: Color, visible_highlight: bool = true) -> void:
	if not is_inside_tree() or combo_border == null:
		return
		
	if not visible_highlight or col == Color.TRANSPARENT:
		combo_border.visible = false
		return
		
	combo_border.visible = true
	var style: StyleBoxFlat = StyleBoxFlat.new()
	style.draw_center = false
	style.bg_color = Color(0, 0, 0, 0)
	style.border_color = col
	style.border_width_top = 4
	style.border_width_left = 4
	style.border_width_right = 4
	style.border_width_bottom = 4
	style.corner_radius_top_left = 8
	style.corner_radius_top_right = 8
	style.corner_radius_bottom_right = 8
	style.corner_radius_bottom_left = 8
	style.shadow_size = 0
	combo_border.add_theme_stylebox_override("panel", style)

func set_selected(selected: bool) -> void:
	is_selected = selected
	z_index = 15 if selected else 0
	_animate_position()

func _on_mouse_entered() -> void:
	if not is_selected and not is_dragging:
		z_index = 10
		var tween = create_tween()
		tween.tween_property(self, "position:y", base_y + hover_offset, 0.1)

func _on_mouse_exited() -> void:
	if not is_selected and not is_dragging:
		z_index = 0
	_animate_position()

func _animate_position() -> void:
	if is_dragging:
		return
	var target_y = base_y
	if is_selected:
		target_y += selected_offset
	var tween = create_tween()
	tween.tween_property(self, "position:y", target_y, 0.12).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)

func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
			is_dragging = false
			card_double_clicked.emit(self)
			return
			
		elif event.button_index == MOUSE_BUTTON_LEFT:
			if event.double_click:
				is_dragging = false
				card_double_clicked.emit(self)
				return
				
			if event.pressed:
				drag_start_mouse_pos = event.global_position
				is_dragging = false
			else:
				if is_dragging:
					is_dragging = false
					z_index = 0
					card_drag_ended.emit(self, event.global_position)
				else:
					card_clicked.emit(self)
				
	elif event is InputEventMouseMotion:
		if (event.button_mask & MOUSE_BUTTON_MASK_LEFT) != 0:
			if not is_dragging and event.global_position.distance_to(drag_start_mouse_pos) > drag_threshold:
				is_dragging = true
				z_index = 30
				card_drag_started.emit(self)
			if is_dragging:
				card_dragged.emit(self, event.global_position)
