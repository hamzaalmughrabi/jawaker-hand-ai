# Match Record: match_298e9e2d

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:39:22
**Winner**: **Heuristic_1** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `PIMC` | **PIMC_0** |
| P1 | `Heuristic` | **Heuristic_1** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Player 1 -> 48 pts [WINNER!]
Rank 2: Player 0 -> 52 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 597

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Heuristic_1** | DISCARD | `DISCARD:8C` | 1.3ms |
| R1 | T2 | P0 | **PIMC_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **PIMC_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **PIMC_0** | DISCARD | `DISCARD:AH` | 1.6ms |
| R1 | T3 | P1 | **Heuristic_1** | DRAW | `DRAW_DISCARD` | 0.1ms |
| R1 | T3 | P1 | **Heuristic_1** | MELD | `INITIAL_MELD:SET[AC AD AH AS -> 44pts]+SET[KD KS JK1(KC) -> 30pts]+RUN[4H 5H 6H -> 15pts]` | 1.5ms |
| R1 | T3 | P1 | **Heuristic_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Heuristic_1** | DISCARD | `DISCARD:AH` | 0.5ms |
| R1 | T4 | P0 | **PIMC_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **PIMC_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **PIMC_0** | DISCARD | `DISCARD:JC` | 1.6ms |
| R1 | T5 | P1 | **Heuristic_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Heuristic_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Heuristic_1** | DISCARD | `DISCARD:9C` | 0.4ms |
| R1 | T6 | P0 | **PIMC_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **PIMC_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **PIMC_0** | DISCARD | `DISCARD:TC` | 1.9ms |
| R1 | T7 | P1 | **Heuristic_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **Heuristic_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Heuristic_1** | DISCARD | `DISCARD:8H` | 0.4ms |
| R1 | T8 | P0 | **PIMC_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **PIMC_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **PIMC_0** | DISCARD | `DISCARD:JH` | 1.9ms |
| R1 | T9 | P1 | **Heuristic_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **Heuristic_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Heuristic_1** | DISCARD | `DISCARD:7D` | 0.4ms |
| R1 | T10 | P0 | **PIMC_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **PIMC_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **PIMC_0** | DISCARD | `DISCARD:TS` | 1.7ms |
| R1 | T11 | P1 | **Heuristic_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T11 | P1 | **Heuristic_1** | MELD | `ATTACH:3H->Meld#3` | 0.1ms |
| R1 | T11 | P1 | **Heuristic_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **Heuristic_1** | DISCARD | `DISCARD:6C` | 0.2ms |
| R1 | T12 | P0 | **PIMC_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **PIMC_0** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]