# Match Record: match_e8b859c2

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 21:28:57
**Winner**: **ISMCTS_Search** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `ISMCTS` | **ISMCTS_Search** |
| P1 | `RL` | **RL_Linear_Model** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: ISMCTS_Search (P0) -> 74 pts [WINNER!]
Rank 2: RL_Linear_Model (P1) -> 291 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 521

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:2C` | 0.7ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DRAW | `DRAW_DISCARD` | 55.2ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `INITIAL_MELD:SET[AD AS AH -> 33pts]+RUN[2C 3C 4C 5C 6C -> 20pts]` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:KC` | 53.3ms |
| R1 | T3 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.5ms |
| R1 | T3 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.5ms |
| R1 | T3 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:6C` | 10.9ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:QC` | 43.9ms |
| R1 | T5 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T5 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.5ms |
| R1 | T5 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:KC` | 10.9ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:6H` | 37.8ms |
| R1 | T7 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T7 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.3ms |
| R1 | T7 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:3D` | 8.2ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:8S` | 45.3ms |
| R1 | T9 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T9 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.2ms |
| R1 | T9 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:6D` | 8.5ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:7D` | 50.9ms |
| R1 | T11 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.7ms |
| R1 | T11 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.5ms |
| R1 | T11 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:TD` | 8.0ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T12 | P0 | **ISMCTS_Search** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T12 | P0 | **ISMCTS_Search** | DISCARD | `DISCARD:9S` | 70.6ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]