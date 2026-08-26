# Match Record: match_4a950e2c

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:39:52
**Winner**: **Heuristic_0** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Heuristic` | **Heuristic_0** |
| P1 | `Greedy` | **Greedy_1** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Player 0 -> -77 pts [WINNER!]
Rank 2: Player 1 -> 48 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 476

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Greedy_1** | DISCARD | `DISCARD:QH` | 0.7ms |
| R1 | T2 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_0** | MELD | `INITIAL_MELD:SET[AS AD JK2(AC) JK1(AH) -> 44pts]+RUN[2H 3H 4H -> 9pts]` | 1.3ms |
| R1 | T2 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Heuristic_0** | DISCARD | `DISCARD:AS` | 0.4ms |
| R1 | T3 | P1 | **Greedy_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T3 | P1 | **Greedy_1** | MELD | `INITIAL_MELD:SET[7C 7D 7S -> 21pts]+SET[9H 9D 9S -> 27pts]+RUN[6H 7H 8H -> 21pts]` | 0.1ms |
| R1 | T3 | P1 | **Greedy_1** | MELD | `ATTACH:7H->Meld#3` | 0.0ms |
| R1 | T3 | P1 | **Greedy_1** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T3 | P1 | **Greedy_1** | DISCARD | `DISCARD:QS` | 0.2ms |
| R1 | T4 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Heuristic_0** | MELD | `ATTACH:9C->Meld#4` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_0** | DISCARD | `DISCARD:JC` | 0.5ms |
| R1 | T5 | P1 | **Greedy_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T5 | P1 | **Greedy_1** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Greedy_1** | DISCARD | `DISCARD:QS` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_0** | MELD | `LAY_MELD:SET[3H 3C 3D -> 9pts]` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Heuristic_0** | DISCARD | `DISCARD:KC` | 0.2ms |
| R1 | T7 | P1 | **Greedy_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Greedy_1** | MELD | `ATTACH:5H->Meld#2` | 0.0ms |
| R1 | T7 | P1 | **Greedy_1** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T7 | P1 | **Greedy_1** | DISCARD | `DISCARD:8C` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_0** | DISCARD | `DISCARD:JC` | 0.2ms |
| R1 | T9 | P1 | **Greedy_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T9 | P1 | **Greedy_1** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Greedy_1** | DISCARD | `DISCARD:TH` | 0.2ms |
| R1 | T10 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Heuristic_0** | DISCARD | `DISCARD:QC` | 0.5ms |
| R1 | T11 | P1 | **Greedy_1** | DRAW | `DRAW_STOCK` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]