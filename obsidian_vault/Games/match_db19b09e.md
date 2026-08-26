# Match Record: match_db19b09e

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:48:20
**Winner**: **PIMC_Determinizer** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `PIMC` | **PIMC_Determinizer** |
| P1 | `DeepRL` | **DeepRL_ValueNet** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: PIMC_Determinizer (P0) -> 109 pts [WINNER!]
Rank 2: DeepRL_ValueNet (P1) -> 116 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 437

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:5D` | 2.4ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JD` | 1.6ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_DISCARD` | 0.6ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `INITIAL_MELD:RUN[8C 9C TC -> 27pts]+RUN[JD QD KD -> 30pts]` | 0.5ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.0ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:6C` | 8.9ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JC` | 1.7ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.7ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.1ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:6H` | 9.6ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:QH` | 1.7ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.1ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.0ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:7D` | 8.6ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:KH` | 1.7ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 2.4ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.1ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:4C` | 8.3ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:QS` | 1.8ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.9ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.0ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:5S` | 7.5ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JH` | 1.7ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]