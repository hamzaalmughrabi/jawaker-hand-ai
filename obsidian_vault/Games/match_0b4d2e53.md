# Match Record: match_0b4d2e53

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:56:56
**Winner**: **Greedy_Deadwood** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Greedy` | **Greedy_Deadwood** |
| P1 | `Hybrid` | **Hybrid_ISMCTS_RL** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Greedy_Deadwood (P0) -> -45 pts [WINNER!]
Rank 2: Hybrid_ISMCTS_RL (P1) -> 61 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 482

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:QS` | 19.3ms |
| R1 | T2 | P0 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T2 | P0 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Greedy_Deadwood** | DISCARD | `DISCARD:KD` | 0.4ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:SET[4C 4H 4S -> 12pts]+SET[AD AS AC -> 33pts]+SET[5C 5H 5S -> 15pts]` | 27.8ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:QH` | 18.7ms |
| R1 | T4 | P0 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Greedy_Deadwood** | DISCARD | `DISCARD:QH` | 0.5ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:QC` | 20.3ms |
| R1 | T6 | P0 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Greedy_Deadwood** | DISCARD | `DISCARD:KC` | 0.4ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:6S` | 23.1ms |
| R1 | T8 | P0 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Greedy_Deadwood** | DISCARD | `DISCARD:9H` | 0.4ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:9H` | 22.3ms |
| R1 | T10 | P0 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Greedy_Deadwood** | DISCARD | `DISCARD:KS` | 0.4ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | MELD | `ATTACH:4D->Meld#1` | 21.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:6H` | 18.4ms |
| R1 | T12 | P0 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T12 | P0 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]