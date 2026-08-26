# Match Record: match_a58ea9cd

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:39
**Winner**: **PIMC_Determinizer** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `ISMCTS` | **ISMCTS_Search** |
| P1 | `PIMC` | **PIMC_Determinizer** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: PIMC_Determinizer (P1) -> 142 pts [WINNER!]
Rank 2: ISMCTS_Search (P0) -> 143 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 507

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **PIMC_Determinizer** | DISCARD | `DISCARD:AS` | 1.5ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `INITIAL_MELD:SET[KC KD KH -> 30pts]+SET[8D 8S 8C -> 24pts]` | 40.0ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:QS` | 34.7ms |
| R1 | T3 | P1 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **PIMC_Determinizer** | DISCARD | `DISCARD:AH` | 1.7ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:TS` | 58.1ms |
| R1 | T5 | P1 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T5 | P1 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **PIMC_Determinizer** | DISCARD | `DISCARD:TD` | 1.7ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:TC` | 63.0ms |
| R1 | T7 | P1 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **PIMC_Determinizer** | DISCARD | `DISCARD:KH` | 1.7ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:JH` | 47.6ms |
| R1 | T9 | P1 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **PIMC_Determinizer** | DISCARD | `DISCARD:QH` | 1.7ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:7H` | 49.0ms |
| R1 | T11 | P1 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **PIMC_Determinizer** | DISCARD | `DISCARD:JS` | 1.7ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:AS` | 36.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]