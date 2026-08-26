# Mistake Analysis: Unopened Penalty (+100 / +200 Points)

## Summary
The single most costly mistake in competitive Jawaker Hand is failing to open before an opponent finishes.

---

### 1. Penalty Mechanics
* **Normal Finish Loser Penalty**: $+100$ points.
* **Hand Finish Loser Penalty**: $+200$ points (doubled!).

---

### 2. Preventive AI Heuristics
1. **Turn 8 Threshold**: If turn count reaches $\ge 8$ and any opponent has $\le 6$ cards remaining, immediately execute any valid opening $\ge 51$ points.
2. **Draw Discard Utilization**: Take from the discard pile whenever it enables a $\ge 51$-point opening.
