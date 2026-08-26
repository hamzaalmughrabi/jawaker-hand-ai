# Joker Mastery & Substitution Patterns

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
