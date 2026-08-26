# Jawaker Hand Godot 4 Game Client

A modern, responsive 2D card game interface for **Jawaker Hand (هاند جواكر)** built in **Godot 4.3 (GDScript)** and connected to the high-performance **Python Engine & Apex RL AI**.

---

## 🎮 How to Run the Game

### Step 1: Start the Python Backend Server
In your terminal, run:
```powershell
cd C:\Users\hamza\.gemini\antigravity\scratch\jawaker-hand-ai
python -u -m jawaker_hand_ai.cli.main serve --port 8765
```

### Step 2: Open & Run in Godot 4
1. Open the **Godot 4** editor.
2. Click **Import** and choose the `godot_client/project.godot` file located at:
   `C:\Users\hamza\.gemini\antigravity\scratch\jawaker-hand-ai\godot_client\project.godot`
3. Press **F5** (or click the **Play** button at top right) to run the game!

---

## 🃏 Features & Visual Presentation

* **Casino Green Felt Table**: Realistic poker table with wooden bezel and dedicated melds area.
* **Interactive Player Hand**:
  * Hover lift animation (`-12px` elevation).
  * Selected card elevation (`-28px`).
  * Instant discard clicking in `DISCARD` phase.
  * **Sort Suit** & **Sort Rank** buttons.
* **Table Melds Area**: Displays active Sets & Runs with point counters and Joker representations (e.g. `JK (7S)`).
* **Stock & Fire Piles**: Visual stock deck with remaining card badge and fire pile upcard.
* **Real-Time Turn Status**: Dynamic banners with live AI thinking indicators and match score accounting.
