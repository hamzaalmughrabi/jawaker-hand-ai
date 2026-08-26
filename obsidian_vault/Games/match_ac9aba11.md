# Match Record: match_ac9aba11

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:19
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
Rank 1: Hybrid_ISMCTS_RL (P1) -> -31 pts [WINNER!]
Rank 2: PIMC_Determinizer (P0) -> 274 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 511

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:JH` | 18.9ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:TC` | 1.6ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:2S` | 17.8ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:JD` | 1.6ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:8C` | 15.9ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:QD` | 1.7ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 26.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:SET[7C 7H 7S -> 21pts]+RUN[JD QD KD AD -> 41pts]` | 42.8ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:QC` | 33.4ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:TH` | 1.7ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 45.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:9S` | 30.9ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **PIMC_Determinizer** | DISCARD | `DISCARD:KC` | 1.7ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 47.3ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:5S` | 35.4ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | DRAW | `DRAW_DISCARD` | 0.3ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | MELD | `INITIAL_MELD:SET[5C 5D 5S -> 15pts]+RUN[7C 8C 9C -> 24pts]+RUN[6S 7S 8S -> 21pts]` | 0.5ms |
| R1 | T12 | P0 | **PIMC_Determinizer** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]