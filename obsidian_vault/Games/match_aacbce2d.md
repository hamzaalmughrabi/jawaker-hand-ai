# Match Record: match_aacbce2d

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:59:00
**Winner**: **Hybrid_ISMCTS_RL** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Random` | **Random_Baseline** |
| P1 | `Hybrid` | **Hybrid_ISMCTS_RL** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Hybrid_ISMCTS_RL (P1) -> 96 pts [WINNER!]
Rank 2: Random_Baseline (P0) -> 189 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 552

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:2S` | 27.3ms |
| R1 | T2 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T2 | P0 | **Random_Baseline** | DISCARD | `DISCARD:TS` | 0.0ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 48.3ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:SET[TH TS JK1(TC) -> 30pts]+RUN[4C 5C 6C 7C 8C -> 30pts]` | 50.8ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T3 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KS` | 30.4ms |
| R1 | T4 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T4 | P0 | **Random_Baseline** | DISCARD | `DISCARD:5D` | 0.0ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T5 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:6S` | 33.2ms |
| R1 | T6 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T6 | P0 | **Random_Baseline** | DISCARD | `DISCARD:TH` | 0.0ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T7 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:9S` | 31.9ms |
| R1 | T8 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T8 | P0 | **Random_Baseline** | DISCARD | `DISCARD:9H` | 0.0ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `ATTACH:9C->Meld#2` | 45.9ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T9 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:6S` | 28.4ms |
| R1 | T10 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T10 | P0 | **Random_Baseline** | DISCARD | `DISCARD:JS` | 0.0ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T11 | P1 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:AH` | 30.5ms |
| R1 | T12 | P0 | **Random_Baseline** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T12 | P0 | **Random_Baseline** | MELD | `PASS_MELD` | 0.0ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]