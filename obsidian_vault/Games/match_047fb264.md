# Match Record: match_047fb264

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:48:24
**Winner**: **Heuristic_RuleBased** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Heuristic` | **Heuristic_RuleBased** |
| P1 | `Random` | **Random_Baseline** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Heuristic_RuleBased (P0) -> 12 pts [WINNER!]
Rank 2: Random_Baseline (P1) -> 217 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 459

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Random_Baseline** | DISCARD | `DISCARD:9H` | 0.0ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:AD` | 0.4ms |
| R1 | T3 | P1 | **Random_Baseline** | DRAW | `DRAW_DISCARD` | 0.0ms |
| R1 | T3 | P1 | **Random_Baseline** | MELD | `INITIAL_MELD:SET[AD AC AH -> 33pts]+RUN[TC JC QC -> 30pts]` | 0.0ms |
| R1 | T3 | P1 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T3 | P1 | **Random_Baseline** | DISCARD | `DISCARD:3C` | 0.0ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | MELD | `INITIAL_MELD:SET[6D 6H 6S -> 18pts]+SET[TH TS TC -> 30pts]+SET[7S 7H 7C -> 21pts]` | 0.4ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:KD` | 0.6ms |
| R1 | T5 | P1 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T5 | P1 | **Random_Baseline** | MELD | `ATTACH:7D->Meld#5` | 0.0ms |
| R1 | T5 | P1 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Random_Baseline** | DISCARD | `DISCARD:3C` | 0.0ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QH` | 0.5ms |
| R1 | T7 | P1 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Random_Baseline** | MELD | `ATTACH:6C->Meld#3` | 0.0ms |
| R1 | T7 | P1 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T7 | P1 | **Random_Baseline** | DISCARD | `DISCARD:8D` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | MELD | `ATTACH:9C->Meld#2` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QC` | 0.7ms |
| R1 | T9 | P1 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T9 | P1 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Random_Baseline** | DISCARD | `DISCARD:5D` | 0.0ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_DISCARD` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | MELD | `LAY_MELD:SET[5H 5C 5D -> 15pts]` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:KS` | 0.2ms |
| R1 | T11 | P1 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]