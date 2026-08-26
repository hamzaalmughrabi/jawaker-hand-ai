# Match Record: match_f51441e6

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:39:55
**Winner**: **Greedy_0** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Greedy` | **Greedy_0** |
| P1 | `DeepRL` | **DeepRL_1** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Player 0 -> -83 pts [WINNER!]
Rank 2: Player 1 -> 176 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 554

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **DeepRL_1** | DISCARD | `DISCARD:2S` | 1.5ms |
| R1 | T2 | P0 | **Greedy_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T2 | P0 | **Greedy_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Greedy_0** | DISCARD | `DISCARD:AH` | 0.4ms |
| R1 | T3 | P1 | **DeepRL_1** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T3 | P1 | **DeepRL_1** | MELD | `PASS_MELD` | 0.4ms |
| R1 | T3 | P1 | **DeepRL_1** | DISCARD | `DISCARD:3H` | 1.6ms |
| R1 | T4 | P0 | **Greedy_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Greedy_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Greedy_0** | DISCARD | `DISCARD:QC` | 0.3ms |
| R1 | T5 | P1 | **DeepRL_1** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T5 | P1 | **DeepRL_1** | MELD | `PASS_MELD` | 0.5ms |
| R1 | T5 | P1 | **DeepRL_1** | DISCARD | `DISCARD:4D` | 1.5ms |
| R1 | T6 | P0 | **Greedy_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Greedy_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Greedy_0** | DISCARD | `DISCARD:JD` | 0.4ms |
| R1 | T7 | P1 | **DeepRL_1** | DRAW | `DRAW_DISCARD` | 0.5ms |
| R1 | T7 | P1 | **DeepRL_1** | MELD | `INITIAL_MELD:RUN[TD JD QD -> 30pts]+RUN[JS QS KS -> 30pts]` | 0.5ms |
| R1 | T7 | P1 | **DeepRL_1** | MELD | `PASS_MELD` | 0.7ms |
| R1 | T7 | P1 | **DeepRL_1** | DISCARD | `DISCARD:4C` | 5.4ms |
| R1 | T8 | P0 | **Greedy_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Greedy_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Greedy_0** | DISCARD | `DISCARD:TS` | 0.4ms |
| R1 | T9 | P1 | **DeepRL_1** | DRAW | `DRAW_DISCARD` | 1.3ms |
| R1 | T9 | P1 | **DeepRL_1** | MELD | `PASS_MELD` | 1.5ms |
| R1 | T9 | P1 | **DeepRL_1** | DISCARD | `DISCARD:5D` | 6.4ms |
| R1 | T10 | P0 | **Greedy_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Greedy_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Greedy_0** | DISCARD | `DISCARD:AD` | 0.4ms |
| R1 | T11 | P1 | **DeepRL_1** | DRAW | `DRAW_STOCK` | 0.8ms |
| R1 | T11 | P1 | **DeepRL_1** | MELD | `PASS_MELD` | 1.3ms |
| R1 | T11 | P1 | **DeepRL_1** | DISCARD | `DISCARD:2H` | 5.4ms |
| R1 | T12 | P0 | **Greedy_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T12 | P0 | **Greedy_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T12 | P0 | **Greedy_0** | DISCARD | `DISCARD:QS` | 0.4ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]