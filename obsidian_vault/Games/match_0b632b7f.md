# Match Record: match_0b632b7f

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:47:10
**Winner**: **Hybrid_ISMCTS_RL** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `PIMC` | **PIMC_Determinizer** |
| P1 | `Hybrid` | **Hybrid_ISMCTS_RL** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Hybrid_ISMCTS_RL (P1) -> -66 pts [WINNER!]
Rank 2: PIMC_Determinizer (P0) -> 284 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 446

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:6C` | 54.6ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:AD` | 1.5ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 119.4ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:RUN[9D TD JK1(JD) QD KD AD -> 60pts]+RUN[6S 7S 8S -> 21pts]` | 121.0ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:QC` | 64.6ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:AH` | 1.6ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 67.3ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `LAY_MELD:RUN[AH 2H 3H -> 6pts]` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KC` | 76.5ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JH` | 1.6ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:7H` | 77.4ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JK2` | 1.7ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 92.6ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `ATTACH:JK2->Meld#1` | 97.3ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:5D` | 69.8ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:AD` | 1.6ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:AC` | 69.1ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]