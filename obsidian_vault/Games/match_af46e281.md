# Match Record: match_af46e281

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:27
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
Rank 1: Greedy_Deadwood (P1) -> -32 pts [WINNER!]
Rank 2: ISMCTS_Search (P0) -> 240 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 561

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:AH` | 0.3ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DRAW | `DRAW_DISCARD` | 44.6ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `INITIAL_MELD:SET[AD AC AH -> 33pts]+SET[6C 6H 6S -> 18pts]` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:KC` | 38.6ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_DISCARD` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | MELD | `INITIAL_MELD:SET[JC JD JS -> 30pts]+SET[KH KS KC -> 30pts]` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | MELD | `ATTACH:AS->Meld#1` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | MELD | `ATTACH:6D->Meld#2` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:TH` | 0.2ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DRAW | `DRAW_DISCARD` | 30.9ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `ATTACH:JH->Meld#3` | 30.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 26.6ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:JD` | 26.2ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:9H` | 0.2ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 31.6ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `LAY_MELD:SET[TC TD JK1(TH) -> 30pts]` | 44.9ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `ATTACH:TH->Meld#5` | 32.3ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:8C` | 22.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:7S` | 0.2ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 20.9ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:2H` | 21.3ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_DISCARD` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | MELD | `LAY_MELD:RUN[2H 3H 4H -> 9pts]` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:7H` | 0.2ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]