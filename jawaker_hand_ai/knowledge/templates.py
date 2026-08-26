"""Obsidian Markdown templates for Jawaker Hand strategies, mistakes, game logs, and dossiers."""

DISCARD_STRATEGY_TEMPLATE = r"""# Discard Strategy in Jawaker Hand

## 1. Core Principles
In Jawaker Hand, every discard carries strategic weight because opened players can attach cards directly to table melds.

### The Table Attachment Rule
* **High Danger**: Discarding a card of the same suit and adjacent rank to an open table Run (e.g., discarding $8\heartsuit$ when $5\heartsuit-6\heartsuit-7\heartsuit$ is on the table).
* **Set Danger**: Discarding a card matching the rank of an open 3-card table Set (e.g., discarding $9\spadesuit$ when $9\heartsuit-9\diamondsuit-9\clubsuit$ is on the table).

---

## 2. Priority Order for Discarding
1. **Dead Unmelded High Cards**: Discard high cards ($K, Q, J$) that cannot form melds and cannot attach to table melds to minimize potential penalty points.
2. **Duplicated / Dead Suit Runs**: Discard cards where both copies of connector ranks have already been discarded or melded.
3. **Safe Low Cards**: Low cards ($2, 3, 4$) have low point risk ($2..4$ pts) if caught at round end.

---

## 3. Discard Telemetry Insights
* Empirical blunders occur most frequently between Turns 6–10 when opponents have opened and players discard connectors into opponent runs.
"""

OPENING_51_STRATEGY_TEMPLATE = r"""# Opening Strategy: The 51-Point Rule

## Official Jawaker Hand Rule
A player cannot place any cards on the table until they can lay down valid melds totaling **$\ge 51$ points**.

---

### 1. Point Values in Melds
* **Ace ($A$)**: $11$ points (EXCEPT when used in low run $A-2-3$, where $A = 1$).
* **Face Cards & 10 ($10, J, Q, K$)**: $10$ points each.
* **$2$ to $9$**: Face value.
* **Joker**: Takes the point value of the substituted card.

---

### 2. Key Synergies to Reach 51 Points
1. **Triple Aces ($A\spadesuit, A\heartsuit, A\diamondsuit$)**: Instantly yields $33$ points! Requires only an $18$-point second meld (e.g. $6-7-8$) to open.
2. **High Runs ($10-J-Q-K-A$)**: Yields $51$ points in a single 5-card run.
3. **Double Face Sets ($K-K-K$ + $Q-Q-Q$)**: Yields $30 + 30 = 60$ points.

---

### 3. Strategic Trade-Off: Open Early vs Hold for Hand
* **Open Early**: Protects against the devastating **$+100$ Unopened Penalty**.
* **Hold for Hand**: Attempt only if having $\ge 12$ melded cards with no opponents currently opened.
"""

MISTAKE_UNOPENED_TEMPLATE = r"""# Mistake Analysis: Unopened Penalty (+100 / +200 Points)

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
"""

STRATEGY_1V1_TEMPLATE = r"""# 1v1 Championship Duel Strategy

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
"""

JOKER_MASTERY_TEMPLATE = r"""# Joker Mastery & Substitution Patterns

## 1. Joker Value & Utility
* **In Hand at Round End**: **15 penalty points**.
* **In Initial Meld ($\ge 51$)**: Takes the value of the replaced card (e.g. Ace = 11 pts, King = 10 pts).
* **As Wild Card**: Universal connector to bridge missing ranks or suits.

---

## 2. The Tactical Joker Liberation Pattern
When a Joker is on the table in a sequence such as:
$$8\diamondsuit - \text{JK} - 10\diamondsuit$$
1. The AI retains the natural $9\diamondsuit$ in hand.
2. At turn start, it substitutes $9\diamondsuit$ for the Joker (`SWAP_JOKER`).
3. The liberated Joker is returned to hand.
4. The Joker is immediately used to lay down a new meld or attach to other table melds to empty the hand!

---

## 3. Avoiding Accidental Joker Discards
* Post-game oracle analysis proves that discarding a Joker costs an average of 30 to 60 expected points per game.
"""
