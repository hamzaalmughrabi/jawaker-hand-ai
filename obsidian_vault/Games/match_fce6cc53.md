# Match Record: match_fce6cc53

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:47:48
**Winner**: **DeepRL_ValueNet** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `ISMCTS` | **ISMCTS_Search** |
| P1 | `DeepRL` | **DeepRL_ValueNet** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: DeepRL_ValueNet (P1) -> 39 pts [WINNER!]
Rank 2: ISMCTS_Search (P0) -> 121 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 572

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:2D` | 1.6ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:KD` | 43.4ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `INITIAL_MELD:SET[7C 7D 7S -> 21pts]+SET[JC JD JS -> 30pts]` | 0.5ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.4ms |
| R1 | T3 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:2C` | 1.6ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:8H` | 31.1ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.4ms |
| R1 | T5 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:AD` | 1.6ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:QC` | 29.3ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.4ms |
| R1 | T7 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:3S` | 1.6ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:2S` | 45.3ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.4ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | MELD | `ATTACH:JH->Meld#2` | 0.6ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.3ms |
| R1 | T9 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:4H` | 1.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:AH` | 27.4ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DRAW | `DRAW_STOCK` | 0.3ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | MELD | `PASS_MELD` | 0.3ms |
| R1 | T11 | P1 | **DeepRL_ValueNet** | DISCARD | `DISCARD:4S` | 1.3ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]