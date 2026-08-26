# Match Record: match_01d537c3

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:39:51
**Winner**: **Heuristic_0** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Heuristic` | **Heuristic_0** |
| P1 | `PIMC` | **PIMC_1** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Player 0 -> -68 pts [WINNER!]
Rank 2: Player 1 -> 148 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 376

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **PIMC_1** | DISCARD | `DISCARD:AD` | 1.6ms |
| R1 | T2 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Heuristic_0** | DISCARD | `DISCARD:QD` | 0.7ms |
| R1 | T3 | P1 | **PIMC_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **PIMC_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **PIMC_1** | DISCARD | `DISCARD:AH` | 1.6ms |
| R1 | T4 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_0** | MELD | `INITIAL_MELD:SET[9C 9S 9H -> 27pts]+RUN[JK1(JS) QS KS AS -> 41pts]` | 0.7ms |
| R1 | T4 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Heuristic_0** | DISCARD | `DISCARD:TC` | 0.5ms |
| R1 | T5 | P1 | **PIMC_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **PIMC_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **PIMC_1** | DISCARD | `DISCARD:TH` | 1.7ms |
| R1 | T6 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Heuristic_0** | DISCARD | `DISCARD:AC` | 0.5ms |
| R1 | T7 | P1 | **PIMC_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **PIMC_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **PIMC_1** | DISCARD | `DISCARD:KC` | 1.6ms |
| R1 | T8 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_0** | DISCARD | `DISCARD:KD` | 0.6ms |
| R1 | T9 | P1 | **PIMC_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **PIMC_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **PIMC_1** | DISCARD | `DISCARD:TS` | 1.7ms |
| R1 | T10 | P0 | **Heuristic_0** | DRAW | `DRAW_DISCARD` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_0** | MELD | `ATTACH:TS->Meld#2` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Heuristic_0** | DISCARD | `DISCARD:8S` | 0.6ms |
| R1 | T11 | P1 | **PIMC_1** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **PIMC_1** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **PIMC_1** | DISCARD | `DISCARD:QC` | 1.8ms |
| R1 | T12 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T12 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]