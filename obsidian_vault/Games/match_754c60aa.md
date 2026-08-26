# Match Record: match_754c60aa

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:54
**Winner**: **ISMCTS_Search** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `ISMCTS` | **ISMCTS_Search** |
| P1 | `Hybrid` | **Hybrid_ISMCTS_RL** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: ISMCTS_Search (P0) -> -2 pts [WINNER!]
Rank 2: Hybrid_ISMCTS_RL (P1) -> 26 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 538

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:TC` | 17.5ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:5H` | 44.5ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 30.6ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KC` | 22.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DRAW | `DRAW_DISCARD` | 56.6ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `INITIAL_MELD:SET[2C 2D 2H -> 6pts]+SET[KH KS KC -> 30pts]+RUN[7H 8H 9H -> 24pts]` | 54.2ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:QD` | 37.2ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:RUN[TH JH QH KH AH -> 51pts]` | 40.8ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:TS` | 25.5ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:QC` | 61.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:JH` | 29.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:8C` | 61.8ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:JD` | 24.0ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:AC` | 62.2ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:TC` | 24.8ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]