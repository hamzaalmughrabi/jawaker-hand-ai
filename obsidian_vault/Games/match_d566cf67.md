# Match Record: match_d566cf67

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:48:22
**Winner**: **Heuristic_RuleBased** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `PIMC` | **PIMC_Determinizer** |
| P1 | `Heuristic` | **Heuristic_RuleBased** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Heuristic_RuleBased (P1) -> -28 pts [WINNER!]
Rank 2: PIMC_Determinizer (P0) -> 307 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 495

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:AD` | 0.4ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JK1` | 1.6ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_DISCARD` | 0.1ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | MELD | `INITIAL_MELD:SET[QC QD QH QS -> 40pts]+RUN[6H JK1(7H) 8H -> 21pts]` | 0.9ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QC` | 0.3ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:AH` | 1.7ms |
| R1 | T5 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QD` | 0.3ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:TD` | 1.7ms |
| R1 | T7 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T7 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:KD` | 0.3ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:QS` | 1.8ms |
| R1 | T9 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T9 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:TC` | 0.3ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:KS` | 1.8ms |
| R1 | T11 | P1 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **Heuristic_RuleBased** | DISCARD | `DISCARD:AC` | 0.3ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:9H` | 1.9ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]