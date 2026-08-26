# Match Record: match_d3db8c19

**Match Type**: 4-Player Table
**Date**: 2026-08-25 20:26:19
**Winner**: **Heuristic_0** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Heuristic` | **Heuristic_0** |
| P1 | `Random` | **Random_1** |
| P2 | `RL` | **RL_2** |
| P3 | `ISMCTS` | **ISMCTS_3** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Player 0 -> 63 pts [WINNER!]
Rank 2: Player 2 -> 213 pts
Rank 3: Player 1 -> 349 pts
Rank 4: Player 3 -> 419 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 709

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Random_1** | DISCARD | `DISCARD:3H` | 0.0ms |
| R1 | T2 | P2 | **RL_2** | DRAW | `DRAW_STOCK` | 73.5ms |
| R1 | T2 | P2 | **RL_2** | MELD | `PASS_MELD` | 109.8ms |
| R1 | T2 | P2 | **RL_2** | DISCARD | `DISCARD:JD` | 871.0ms |
| R1 | T3 | P3 | **ISMCTS_3** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P3 | **ISMCTS_3** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P3 | **ISMCTS_3** | DISCARD | `DISCARD:AS` | 8324.8ms |
| R1 | T4 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_0** | DISCARD | `DISCARD:AC` | 874.6ms |
| R1 | T5 | P1 | **Random_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T5 | P1 | **Random_1** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Random_1** | DISCARD | `DISCARD:5H` | 0.0ms |
| R1 | T6 | P2 | **RL_2** | DRAW | `DRAW_STOCK` | 69.2ms |
| R1 | T6 | P2 | **RL_2** | MELD | `PASS_MELD` | 107.3ms |
| R1 | T6 | P2 | **RL_2** | DISCARD | `DISCARD:2H` | 951.5ms |
| R1 | T7 | P3 | **ISMCTS_3** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P3 | **ISMCTS_3** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P3 | **ISMCTS_3** | DISCARD | `DISCARD:AC` | 8275.6ms |
| R1 | T8 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_0** | DISCARD | `DISCARD:JH` | 846.6ms |
| R1 | T9 | P1 | **Random_1** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T9 | P1 | **Random_1** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Random_1** | DISCARD | `DISCARD:KH` | 0.0ms |
| R1 | T10 | P2 | **RL_2** | DRAW | `DRAW_STOCK` | 71.1ms |
| R1 | T10 | P2 | **RL_2** | MELD | `PASS_MELD` | 112.6ms |
| R1 | T10 | P2 | **RL_2** | DISCARD | `DISCARD:9H` | 889.0ms |
| R1 | T11 | P3 | **ISMCTS_3** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P3 | **ISMCTS_3** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P3 | **ISMCTS_3** | DISCARD | `DISCARD:KC` | 8508.9ms |
| R1 | T12 | P0 | **Heuristic_0** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **Heuristic_0** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T12 | P0 | **Heuristic_0** | DISCARD | `DISCARD:JS` | 857.9ms |
| R1 | T13 | P1 | **Random_1** | DRAW | `DRAW_STOCK` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]