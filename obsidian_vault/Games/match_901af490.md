# Match Record: match_901af490

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:47:24
**Winner**: **ISMCTS_Search** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Hybrid` | **Hybrid_ISMCTS_RL** |
| P1 | `ISMCTS` | **ISMCTS_Search** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: ISMCTS_Search (P1) -> -9 pts [WINNER!]
Rank 2: Hybrid_ISMCTS_RL (P0) -> 27 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 553

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **ISMCTS_Search** | DISCARD | `DISCARD:JH` | 36.9ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 34.4ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:SET[JC JD JH -> 30pts]+SET[7H 7C 7D -> 21pts]` | 0.1ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:AC` | 31.4ms |
| R1 | T3 | P1 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **ISMCTS_Search** | DISCARD | `DISCARD:QC` | 31.7ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:8S` | 30.7ms |
| R1 | T5 | P1 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **ISMCTS_Search** | DISCARD | `DISCARD:8C` | 31.8ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | MELD | `LAY_MELD:RUN[8H 9H TH -> 27pts]` | 56.6ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:TS` | 47.0ms |
| R1 | T7 | P1 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **ISMCTS_Search** | DISCARD | `DISCARD:AC` | 42.1ms |
| R1 | T8 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:9D` | 47.1ms |
| R1 | T9 | P1 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **ISMCTS_Search** | DISCARD | `DISCARD:5H` | 35.0ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | MELD | `ATTACH:7S->Meld#2` | 49.6ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:6D` | 38.7ms |
| R1 | T11 | P1 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **ISMCTS_Search** | DISCARD | `DISCARD:AS` | 32.3ms |
| R1 | T12 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]