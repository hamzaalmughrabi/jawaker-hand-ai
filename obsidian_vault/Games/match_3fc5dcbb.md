# Match Record: match_3fc5dcbb

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-26 09:47:28
**Winner**: **Heuristic_RuleBased** (P0)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Heuristic` | **Heuristic_RuleBased** |
| P1 | `RL` | **RL_Linear_Model** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Heuristic_RuleBased (P0) -> -12 pts [WINNER!]
Rank 2: RL_Linear_Model (P1) -> 194 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 501

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:7C` | 0.8ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:AD` | 0.8ms |
| R1 | T3 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 0.3ms |
| R1 | T3 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 0.3ms |
| R1 | T3 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:9C` | 0.7ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:AC` | 0.9ms |
| R1 | T5 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 0.3ms |
| R1 | T5 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 0.3ms |
| R1 | T5 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:JC` | 1.2ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_DISCARD` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | MELD | `INITIAL_MELD:SET[JD JH JC -> 30pts]+RUN[8D 9D TD -> 27pts]` | 0.8ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QS` | 1.1ms |
| R1 | T7 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T7 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.3ms |
| R1 | T7 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:4D` | 9.7ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:QD` | 0.7ms |
| R1 | T9 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.1ms |
| R1 | T9 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.1ms |
| R1 | T9 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:AH` | 7.7ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **Heuristic_RuleBased** | DISCARD | `DISCARD:KS` | 0.9ms |
| R1 | T11 | P1 | **RL_Linear_Model** | DRAW | `DRAW_STOCK` | 1.2ms |
| R1 | T11 | P1 | **RL_Linear_Model** | MELD | `PASS_MELD` | 1.4ms |
| R1 | T11 | P1 | **RL_Linear_Model** | DISCARD | `DISCARD:6H` | 7.5ms |
| R1 | T12 | P0 | **Heuristic_RuleBased** | DRAW | `DRAW_DISCARD` | 0.1ms |
| R1 | T12 | P0 | **Heuristic_RuleBased** | MELD | `LAY_MELD:SET[6C 6D 6H -> 18pts]` | 0.1ms |
| R1 | T12 | P0 | **Heuristic_RuleBased** | MELD | `PASS_MELD` | 0.1ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]