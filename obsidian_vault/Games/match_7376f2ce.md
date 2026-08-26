# Match Record: match_7376f2ce

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:58:32
**Winner**: **Heuristic_RuleBased** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Heuristic` | **Heuristic_RuleBased** |
| P1 | `Hybrid` | **Hybrid_ISMCTS_RL** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Heuristic_RuleBased (P0) -> -117 pts [WINNER!]
Rank 2: Hybrid_ISMCTS_RL (P1) -> 2 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 542

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:3H` | 29.4ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | MELD | `INITIAL_MELD:SET[9D 9H JK2(9C) -> 27pts]+RUN[5H 6H 7H 8H -> 26pts]` | 1.0ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | MELD | `ATTACH:9H->Meld#2` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:AH` | 0.6ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:SET[QD QH QS -> 30pts]+RUN[9S TS JS -> 29pts]` | 48.0ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KS` | 32.7ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:9D` | 0.9ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `ATTACH:4H->Meld#2` | 51.2ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KS` | 29.9ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | MELD | `SWAP_JOKER:9C->Meld#1[JK2]` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | MELD | `ATTACH:JK2->Meld#1` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:6S` | 0.8ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `LAY_MELD:RUN[2D 3D 4D -> 9pts]` | 45.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KH` | 28.4ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:5H` | 0.8ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:AH` | 27.4ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:TD` | 0.7ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]