# Match Record: match_8cda6703

**Match Type**: 1v1 Championship Duel
**Date**: 2026-08-25 20:57:30
**Winner**: **Greedy_Deadwood** (P1)
**Total Rounds**: 5

## Participating Agents
| Player Seat | Agent Architecture | Name |
|---|---|---|
| P0 | `Hybrid` | **Hybrid_ISMCTS_RL** |
| P1 | `Greedy` | **Greedy_Deadwood** |

## Final Score Accounting
```
--- JAWAKER HAND 5-ROUND MATCH RESULTS ---
Rank 1: Greedy_Deadwood (P1) -> -42 pts [WINNER!]
Rank 2: Hybrid_ISMCTS_RL (P0) -> -24 pts
```

## AI Decision Traces Sample
Total AI Decisions Recorded: 456

| Round | Turn | Player | Agent Name | Phase | Action Selected | Latency (ms) |
|---|---|---|---|---|---|---|
| R1 | T1 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:AD` | 0.5ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T2 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:8H` | 21.1ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T3 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:AD` | 0.4ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_DISCARD` | 23.9ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | MELD | `INITIAL_MELD:SET[TC TD TH TS -> 40pts]+SET[AS AC AD -> 33pts]` | 24.3ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T4 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:KH` | 15.4ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_DISCARD` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | MELD | `INITIAL_MELD:SET[KD KS KH -> 30pts]+RUN[9D TD JD -> 29pts]` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T5 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:JC` | 0.2ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | MELD | `LAY_MELD:RUN[6H 7H 8H -> 21pts]` | 27.6ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | MELD | `ATTACH:KC->Meld#3` | 23.4ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T6 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:8S` | 19.7ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | MELD | `ATTACH:AH->Meld#2` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | MELD | `ATTACH:5H->Meld#5` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | MELD | `ATTACH:4H->Meld#5` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T7 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:9C` | 0.2ms |
| R1 | T8 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T8 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T8 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:JH` | 15.9ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | DRAW | `DRAW_STOCK` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | MELD | `PASS_MELD` | 0.0ms |
| R1 | T9 | P1 | **Greedy_Deadwood** | DISCARD | `DISCARD:9S` | 0.2ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | DRAW | `DRAW_STOCK` | 0.1ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | MELD | `PASS_MELD` | 0.1ms |
| R1 | T10 | P0 | **Hybrid_ISMCTS_RL** | DISCARD | `DISCARD:4S` | 16.3ms |

## Strategy & Analysis Links
- [[1v1 Championship Duel Strategy]]
- [[Opening 51 Points Strategy]]
- [[Discard Strategy]]
- [[Joker Mastery]]
- [[Unopened Hand Penalty]]