# Match Record: match_02b01a10

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:47:01
**Winner**: **DeepRL_ValueNet** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Random` | **Random_Baseline** |
| P1 | `DeepRL` | **DeepRL_ValueNet** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: DeepRL_ValueNet (P1) -> -49 pts [WINNER!]
Rank 2: Random_Baseline (P0) -> 319 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 499

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:2C` | 3.3ms |
| R1 | T2 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | DISCARD | `DISCARD:9D` | 0.0ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_DISCARD` | 2.3ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `INITIAL_MELD:SET[9S 9H 9D -> 27pts]+RUN[7C JK1(8C) JK2(9C) TC JC -> 44pts]` | 5.5ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.5ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:4H` | 2.4ms |
| R1 | T4 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | DISCARD | `DISCARD:TS` | 0.0ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.5ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.6ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:3C` | 3.3ms |
| R1 | T6 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | DISCARD | `DISCARD:6C` | 0.0ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.7ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.6ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:2C` | 2.9ms |
| R1 | T8 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | DISCARD | `DISCARD:8D` | 0.0ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.5ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.5ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:6D` | 2.1ms |
| R1 | T10 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | DISCARD | `DISCARD:9D` | 0.0ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.8ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.7ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:6D` | 2.1ms |
| R1 | T12 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T12 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T12 | P0 | **Random_Baseline** | DISCARD | `DISCARD:4S` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]