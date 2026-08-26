# Match Record: match_27cfce99

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:42
**Winner**: **Random_Baseline** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Random` | **Random_Baseline** |
| P1 | `DeepRL` | **DeepRL_ValueNet** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Random_Baseline (P0) -> 139 pts [WINNER!]
Rank 2: DeepRL_ValueNet (P1) -> 154 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 524

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:2D` | 1.5ms |
| R1 | T2 | P0 | **Random_Baseline** | DRAW | `DRAW_DISCARD` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | MELD | `INITIAL_MELD:RUN[3C 4C 5C -> 12pts]+RUN[2D JK2(3D) 4D -> 9pts]+RUN[JH QH KH -> 30pts]` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | DISCARD | `DISCARD:6H` | 0.0ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 2.0ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:3S` | 15.6ms |
| R1 | T4 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | DISCARD | `DISCARD:3S` | 0.0ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.3ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.3ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:4C` | 15.4ms |
| R1 | T6 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | MELD | `ATTACH:6C->Meld#1` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | DISCARD | `DISCARD:JS` | 0.0ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.1ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.2ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:3H` | 15.5ms |
| R1 | T8 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | DISCARD | `DISCARD:7S` | 0.0ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.3ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:2D` | 15.3ms |
| R1 | T10 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | MELD | `ATTACH:3D->Meld#2` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | DISCARD | `DISCARD:9D` | 0.0ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 1.3ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:4S` | 17.2ms |
| R1 | T12 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]