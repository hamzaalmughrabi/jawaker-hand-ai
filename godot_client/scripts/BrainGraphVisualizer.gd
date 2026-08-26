extends Control
class_name BrainGraphVisualizer

var input_features: Array = []
var hidden1_activations: Array = []
var hidden2_activations: Array = []
var output_val: float = 0.0
var pulse_time: float = 0.0

func _ready() -> void:
	custom_minimum_size = Vector2(480, 160)
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	size_flags_vertical = Control.SIZE_EXPAND_FILL

func _process(delta: float) -> void:
	if visible:
		pulse_time += delta * 2.0
		queue_redraw()

func set_network_state(features: Array, h1: Array, h2: Array, out_val: float) -> void:
	input_features = features
	hidden1_activations = h1
	hidden2_activations = h2
	output_val = out_val
	queue_redraw()

func _draw() -> void:
	var w = size.x
	var h = size.y
	if w < 100 or h < 50:
		return

	# Draw subtle brain silhouette
	_draw_brain_silhouette(w, h)

	var in_count = 16 # Representative active inputs from the 32-dim vector
	var h1_count = 32 # 32 representative neurons from the 64-dim hidden layer
	var h2_count = 16 # 16 representative neurons from the 32-dim hidden layer
	
	var in_nodes: Array[Vector2] = []
	var h1_nodes: Array[Vector2] = []
	var h2_nodes: Array[Vector2] = []
	var out_node = Vector2(w * 0.90, h * 0.5)

	var in_spacing = (h - 35) / float(in_count - 1) if in_count > 1 else 0.0
	for i in range(in_count):
		in_nodes.append(Vector2(w * 0.12, 18 + i * in_spacing))

	var h1_spacing = (h - 25) / float(h1_count - 1) if h1_count > 1 else 0.0
	for i in range(h1_count):
		var arc_offset = sin((float(i) / float(h1_count - 1)) * PI) * (w * 0.035)
		h1_nodes.append(Vector2(w * 0.38 + arc_offset, 12 + i * h1_spacing))

	var h2_spacing = (h - 35) / float(h2_count - 1) if h2_count > 1 else 0.0
	for i in range(h2_count):
		var arc_offset = sin((float(i) / float(h2_count - 1)) * PI) * (w * 0.025)
		h2_nodes.append(Vector2(w * 0.68 - arc_offset, 18 + i * h2_spacing))

	# 1. Draw Real Synapses only where destination neuron is mathematically active!
	for i in range(in_count):
		var p1 = in_nodes[i]
		var in_val = float(input_features[i]) if i < input_features.size() else 0.5
		for j in range(h1_count):
			var p2 = h1_nodes[j]
			var h1_val = float(hidden1_activations[j]) if j < hidden1_activations.size() else 0.0
			if h1_val > 0.0 and in_val > 0.0 and (i + j) % 3 == 0:
				var alpha = clamp(h1_val * 0.25, 0.06, 0.35)
				draw_line(p1, p2, Color(0.0, 0.8, 0.9, alpha), 1.0, true)

	for i in range(h1_count):
		var p1 = h1_nodes[i]
		var h1_val = float(hidden1_activations[i]) if i < hidden1_activations.size() else 0.0
		if h1_val > 0.0:
			for j in range(h2_count):
				var p2 = h2_nodes[j]
				var h2_val = float(hidden2_activations[j]) if j < hidden2_activations.size() else 0.0
				if h2_val > 0.0 and (i + j) % 2 == 0:
					var alpha = clamp(h2_val * 0.3, 0.08, 0.45)
					draw_line(p1, p2, Color(0.2, 0.95, 0.5, alpha), 1.0, true)

	for i in range(h2_count):
		var p1 = h2_nodes[i]
		var h2_val = float(hidden2_activations[i]) if i < hidden2_activations.size() else 0.0
		if h2_val > 0.0:
			var alpha = clamp(h2_val * 0.4, 0.1, 0.5)
			draw_line(p1, out_node, Color(1.0, 0.85, 0.2, alpha), 1.2, true)

	# 2. Draw Real Input Feature Neurons
	for i in range(in_count):
		var pos = in_nodes[i]
		var val = float(input_features[i]) if i < input_features.size() else 0.0
		var is_act = (val > 0.0)
		var col = Color(0.0, 0.85, 1.0) if is_act else Color(0.25, 0.35, 0.4)
		if is_act:
			draw_circle(pos, 5.0, Color(0.0, 0.85, 1.0, 0.25))
		draw_circle(pos, 3.5, col)
		if is_act:
			draw_circle(pos, 1.5, Color(1.0, 1.0, 1.0, 0.9))

	# 3. Draw Real Hidden Layer 1 (64 Neurons)
	for i in range(h1_count):
		var pos = h1_nodes[i]
		var val = float(hidden1_activations[i]) if i < hidden1_activations.size() else 0.0
		var is_act = (val > 0.0)
		var col = Color(0.1, 0.95, 0.4) if is_act else Color(0.2, 0.25, 0.3)
		if is_act:
			var glow_r = clamp(val * 3.0 + 4.0, 4.0, 8.0)
			draw_circle(pos, glow_r, Color(0.1, 0.95, 0.4, 0.25))
		draw_circle(pos, 3.5, col)
		if is_act:
			draw_circle(pos, 1.5, Color(1.0, 1.0, 1.0, 0.95))

	# 4. Draw Real Hidden Layer 2 (32 Neurons)
	for i in range(h2_count):
		var pos = h2_nodes[i]
		var val = float(hidden2_activations[i]) if i < hidden2_activations.size() else 0.0
		var is_act = (val > 0.0)
		var col = Color(0.2, 0.9, 0.7) if is_act else Color(0.2, 0.25, 0.3)
		if is_act:
			var glow_r = clamp(val * 3.5 + 4.5, 4.5, 9.0)
			draw_circle(pos, glow_r, Color(0.2, 0.9, 0.7, 0.3))
		draw_circle(pos, 4.0, col)
		if is_act:
			draw_circle(pos, 1.8, Color(1.0, 1.0, 1.0, 0.95))

	# 5. Master Output Node with real predicted value
	var pulse_glow = 8.0 + sin(pulse_time * 3.0) * 2.0
	draw_circle(out_node, pulse_glow + 4.0, Color(1.0, 0.85, 0.2, 0.2))
	draw_circle(out_node, pulse_glow, Color(1.0, 0.8, 0.1, 0.45))
	draw_circle(out_node, 7.0, Color(1.0, 0.9, 0.2, 1.0))
	draw_circle(out_node, 3.0, Color(1.0, 1.0, 1.0, 1.0))

	# Layer Labels with live active counts
	var active_h1_count = 0
	for v in hidden1_activations:
		if float(v) > 0.0: active_h1_count += 1
	var active_h2_count = 0
	for v in hidden2_activations:
		if float(v) > 0.0: active_h2_count += 1

	_draw_label(Vector2(w * 0.12 - 25, h - 4), "Inputs (32)", Color("#5dade2"))
	_draw_label(Vector2(w * 0.38 - 25, h - 4), "Cortex (%d/64 Active)" % active_h1_count, Color("#2ecc71"))
	_draw_label(Vector2(w * 0.68 - 25, h - 4), "Reasoning (%d/32 Active)" % active_h2_count, Color("#1abc9c"))
	_draw_label(Vector2(w * 0.90 - 25, h - 4), "V(s) = %+.1f" % output_val, Color("#f39c12"))

func _draw_brain_silhouette(w: float, h: float) -> void:
	var points_left: PackedVector2Array = [
		Vector2(w * 0.25, h * 0.06),
		Vector2(w * 0.10, h * 0.18),
		Vector2(w * 0.05, h * 0.45),
		Vector2(w * 0.08, h * 0.78),
		Vector2(w * 0.25, h * 0.94),
		Vector2(w * 0.50, h * 0.90),
		Vector2(w * 0.50, h * 0.10),
		Vector2(w * 0.25, h * 0.06)
	]
	var points_right: PackedVector2Array = [
		Vector2(w * 0.50, h * 0.10),
		Vector2(w * 0.75, h * 0.06),
		Vector2(w * 0.90, h * 0.18),
		Vector2(w * 0.95, h * 0.45),
		Vector2(w * 0.92, h * 0.78),
		Vector2(w * 0.75, h * 0.94),
		Vector2(w * 0.50, h * 0.90)
	]
	draw_polyline(points_left, Color(0.1, 0.4, 0.5, 0.2), 1.5, true)
	draw_polyline(points_right, Color(0.5, 0.3, 0.6, 0.2), 1.5, true)

func _draw_label(pos: Vector2, text: String, color: Color) -> void:
	var font = ThemeDB.fallback_font
	var font_size = 10
	draw_string(font, pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)
