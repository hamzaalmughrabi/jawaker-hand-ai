# Match Record: match_4f2e3aa7

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:48:10
**Winner**: **Greedy_Deadwood** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `ISMCTS` | **ISMCTS_Search** |
| P1 | `Greedy` | **Greedy_Deadwood** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Greedy_Deadwood (P1) -> -86 pts [WINNER!]
Rank 2: ISMCTS_Search (P0) -> 49 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 470

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:AD` | 0.4ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:KD` | 39.5ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:JC` | 0.4ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:TS` | 54.5ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:KC` | 0.4ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:QS` | 58.2ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:QD` | 0.5ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:5H` | 59.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_DISCARD` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | MELD | `INITIAL_MELD:SET[5C 5D 5H -> 15pts]+RUN[5S 6S 7S -> 18pts]+RUN[9S TS JS -> 29pts]` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:JC` | 0.2ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:TD` | 60.4ms |
| R1 | T11 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T11 | P1 | **Greedy_Deadwood** | MELD | `ATTACH:5S->Meld#1` | 0.0ms |
| R1 | T11 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T11 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:9H` | 0.2ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DRAW | `DRAW_DISCARD` | 85.5ms |
| R1 | T12 | P0 | **ISMCTS_Search** | MELD | `INITIAL_MELD:SET[3D 3H 3C -> 9pts]+RUN[8H 9H TH -> 27pts]+RUN[6S JK2(7S) 8S -> 21pts]` | 93.4ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]