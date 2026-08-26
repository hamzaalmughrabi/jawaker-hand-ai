extends PanelContainer

signal meld_clicked(meld_id: int)

@export var meld_id: int = -1
@export var meld_type: String = "SET"
@export var points: int = 0

@onready var title_label: Label = $VBox/Header/Title
@onready var points_label: Label = $VBox/Header/Points
@onready var cards_container: HBoxContainer = $VBox/CardsContainer

var card_scene: PackedScene = preload("res://scenes/Card.tscn")

func _ready() -> void:
	gui_input.connect(_on_gui_input)

func setup_meld(data: Dictionary) -> void:
	meld_id = data.get("meld_id", -1)
	var meld_data = data.get("meld", {})
	meld_type = meld_data.get("type", "SET")
	points = meld_data.get("points", 0)
	
	title_label.text = "#%d %s" % [meld_id, meld_type]
	points_label.text = "%d pts" % points
	
	for child in cards_container.get_children():
		child.queue_free()
		
	var cards_list = meld_data.get("cards", [])
	
	for idx in range(cards_list.size()):
		var c_data = cards_list[idx]
		var card_inst = card_scene.instantiate()
		cards_container.add_child(card_inst)
		card_inst.setup_card(c_data, true)
		card_inst.custom_minimum_size = Vector2(58, 86)
		card_inst.scale = Vector2(0.72, 0.72)
		card_inst.mouse_filter = Control.MOUSE_FILTER_PASS

func _on_gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		meld_clicked.emit(meld_id)
