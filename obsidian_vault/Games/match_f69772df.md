# Match Record: match_f69772df

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:44
**Winner**: **Heuristic_RuleBased** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Random` | **Random_Baseline** |
| P1 | `Heuristic` | **Heuristic_RuleBased** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Heuristic_RuleBased (P1) -> -13 pts [WINNER!]
Rank 2: Random_Baseline (P0) -> 290 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 498

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:KC` | 0.4ms |
| R1 | T2 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | MELD | `INITIAL_MELD:SET[6D 6S 6C -> 18pts]+RUN[JH QH JK2(KH) AH -> 41pts]` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | DISCARD | `DISCARD:6C` | 0.0ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QC` | 0.8ms |
| R1 | T4 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | DISCARD | `DISCARD:9S` | 0.0ms |
| R1 | T5 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:9S` | 1.0ms |
| R1 | T6 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | DISCARD | `DISCARD:5H` | 0.0ms |
| R1 | T7 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:8C` | 1.1ms |
| R1 | T8 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | MELD | `LAY_MELD:RUN[AC 2C 3C -> 6pts]` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | DISCARD | `DISCARD:9H` | 0.0ms |
| R1 | T9 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T9 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:KS` | 1.1ms |
| R1 | T10 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | MELD | `ATTACH:4C->Meld#3` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | DISCARD | `DISCARD:6S` | 0.0ms |
| R1 | T11 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T11 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:5D` | 1.2ms |
| R1 | T12 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]