# 1v1 Championship Duel Strategy

## 1. Core Philosophy in 1v1
In 1v1 duels, game dynamics change significantly from 4-player tables:
1. **Direct Feed**: Any card you discard goes straight to your sole opponent.
2. **Fast Tempo**: Draw rate per player is doubled, making Hand completions much faster.
3. **Unopened Risk (+100)**: If your opponent opens and empties their hand quickly, you risk suffering the +100 unopened penalty.

---

## 2. Decision Matrix: Open vs Hand
* **When to Hold for Hand (-60 pts)**:
  * You hold $\ge 12$ melded cards.
  * Opponent has not opened yet and holds $\ge 10$ cards.
* **When to Open Immediately ($\ge 51$ pts)**:
  * Opponent has already opened on the table.
  * Opponent has $\le 7$ cards remaining.
  * The round has reached Turn 8 or beyond.

---

## 3. Discard Safety Engineering in 1v1
* Track discard pickups: if opponent drew $7\heartsuit$, never discard $6\heartsuit, 8\heartsuit,$ or $7\spadesuit$.
* Dead Cards: Cards whose duplicates (Deck 0 + Deck 1) have both appeared in discards/table are 100% safe.
