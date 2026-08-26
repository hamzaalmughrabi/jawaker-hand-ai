# Match Record: match_b799df49

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:40:11
**Winner**: **ISMCTS_1** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Hybrid` | **Hybrid_0** |
| P1 | `ISMCTS` | **ISMCTS_1** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Player 1 -> -14 pts [WINNER!]
Rank 2: Player 0 -> 29 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 727

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **ISMCTS_1** | DISCARD | `DISCARD:8D` | 56.4ms |
| R1 | T2 | P0 | **Hybrid_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Hybrid_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **Hybrid_0** | DISCARD | `DISCARD:3H` | 18.9ms |
| R1 | T3 | P1 | **ISMCTS_1** | DRAW | `DRAW_DISCARD` | 56.8ms |
| R1 | T3 | P1 | **ISMCTS_1** | MELD | `INITIAL_MELD:SET[3C 3D 3H -> 9pts]+SET[KH KS JK2(KC) -> 30pts]+RUN[5S 6S 7S -> 18pts]` | 0.1ms |
| R1 | T3 | P1 | **ISMCTS_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **ISMCTS_1** | DISCARD | `DISCARD:AC` | 40.7ms |
| R1 | T4 | P0 | **Hybrid_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **Hybrid_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Hybrid_0** | DISCARD | `DISCARD:6S` | 28.0ms |
| R1 | T5 | P1 | **ISMCTS_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **ISMCTS_1** | MELD | `ATTACH:4S->Meld#3` | 36.0ms |
| R1 | T5 | P1 | **ISMCTS_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **ISMCTS_1** | DISCARD | `DISCARD:8D` | 43.6ms |
| R1 | T6 | P0 | **Hybrid_0** | DRAW | `DRAW_DISCARD` | 34.5ms |
| R1 | T6 | P0 | **Hybrid_0** | MELD | `INITIAL_MELD:RUN[TC JC QC -> 30pts]+RUN[6D 7D 8D -> 21pts]` | 0.1ms |
| R1 | T6 | P0 | **Hybrid_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **Hybrid_0** | DISCARD | `DISCARD:9S` | 35.3ms |
| R1 | T7 | P1 | **ISMCTS_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **ISMCTS_1** | MELD | `ATTACH:9C->Meld#4` | 93.1ms |
| R1 | T7 | P1 | **ISMCTS_1** | MELD | `ATTACH:8S->Meld#3` | 78.8ms |
| R1 | T7 | P1 | **ISMCTS_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **ISMCTS_1** | DISCARD | `DISCARD:2S` | 78.9ms |
| R1 | T8 | P0 | **Hybrid_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **Hybrid_0** | MELD | `ATTACH:8C->Meld#4` | 52.6ms |
| R1 | T8 | P0 | **Hybrid_0** | MELD | `ATTACH:9S->Meld#3` | 46.2ms |
| R1 | T8 | P0 | **Hybrid_0** | MELD | `ATTACH:TS->Meld#3` | 43.1ms |
| R1 | T8 | P0 | **Hybrid_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **Hybrid_0** | DISCARD | `DISCARD:7S` | 22.1ms |
| R1 | T9 | P1 | **ISMCTS_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **ISMCTS_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **ISMCTS_1** | DISCARD | `DISCARD:5C` | 77.7ms |
| R1 | T10 | P0 | **Hybrid_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **Hybrid_0** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]