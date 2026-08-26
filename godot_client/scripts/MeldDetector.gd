class_name MeldDetector
extends RefCounted

## Utility for real-time detection of adjacent runs and sets in the player's ordered hand.

static func find_adjacent_melds(hand: Array) -> Array:
	var n = hand.size()
	if n < 3:
		return []

	var found_melds = []
	var used_indices = {}
	
	# Greedily search for longest valid runs and sets of adjacent cards (length >= 3)
	var i = 0
	while i < n:
		if used_indices.has(i):
			i += 1
			continue
			
		var best_meld = null
		# Try lengths from longest (e.g. 7) down to 3
		for length in range(min(7, n - i), 2, -1):
			var sub_slice = hand.slice(i, i + length)
			var is_run = is_valid_run(sub_slice)
			var is_set = is_valid_set(sub_slice)
			if is_run or is_set:
				var idx_list = []
				for k in range(i, i + length):
					idx_list.append(k)
				best_meld = {
					"start": i,
					"length": length,
					"indices": idx_list,
					"type": "RUN" if is_run else "SET",
					"cards": sub_slice
				}
				break
				
		if best_meld != null:
			found_melds.append(best_meld)
			for idx in best_meld["indices"]:
				used_indices[idx] = true
			i += best_meld["length"]
		else:
			i += 1
			
	return found_melds


static func is_valid_set(cards: Array) -> bool:
	if cards.size() < 3 or cards.size() > 4:
		return false
		
	var target_rank = -1
	var seen_suits: Dictionary = {}
	var joker_count = 0
	
	for c in cards:
		if c.get("is_joker", false):
			joker_count += 1
		else:
			var r = c.get("rank", -1)
			var s = c.get("suit", "")
			if target_rank == -1:
				target_rank = r
			elif target_rank != r:
				return false
				
			if seen_suits.has(s):
				return false
			seen_suits[s] = true
			
	return target_rank != -1 or joker_count >= 3


static func is_valid_run(cards: Array) -> bool:
	if cards.size() < 3 or cards.size() > 14:
		return false
		
	var target_suit = ""
	for c in cards:
		if not c.get("is_joker", false):
			var s = c.get("suit", "")
			if target_suit == "":
				target_suit = s
			elif target_suit != s:
				return false
				
	# Case 1: Normal ascending (e.g. 2, 3, 4 ... or 10, J, Q, K)
	if _check_consecutive_run(cards, false):
		return true
	# Case 2: High Ace run (e.g. Q, K, A -> Ace = 14)
	if _check_consecutive_run(cards, true):
		return true
		
	return false


static func _check_consecutive_run(cards: Array, high_ace: bool) -> bool:
	var ranks = []
	for c in cards:
		if c.get("is_joker", false):
			ranks.append(-1)
		else:
			var r = c.get("rank", 0)
			if r == 1 and high_ace:
				r = 14
			ranks.append(r)
			
	var anchor_idx = -1
	for idx in range(ranks.size()):
		if ranks[idx] != -1:
			anchor_idx = idx
			break
			
	if anchor_idx == -1:
		return true
		
	var anchor_val = ranks[anchor_idx]
	var expected_start = anchor_val - anchor_idx
	if expected_start < 1 or (expected_start + ranks.size() - 1) > 14:
		return false
		
	for idx in range(ranks.size()):
		var expected = expected_start + idx
		if ranks[idx] != -1 and ranks[idx] != expected:
			return false
			
	return true
