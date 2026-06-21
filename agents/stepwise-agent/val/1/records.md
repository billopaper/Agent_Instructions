# Records — Weighted Shortest Path (stepwise agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 0.950747 | 26651 | 25 | new best (first correct: Dijkstra, heapq, adjacency list of tuples) |
| 2 | true | 0.729342 | 10103 | 37 | new best (CSR flat-list adjacency; runtime −23%, memory −62%, loc +12) |
| 3 | true | 1.168954 | 7954 | 37 | reverted (array.array CSR; memory −21% but runtime +60%, only 1/3 improved) |
| 4 | true | 0.787580 | 8955 | 37 | reverted (int-encoded heap via divmod; memory −11% but runtime tie, only 1/3 improved) |
| 5 | true | 0.833029 | 9868 | 36 | new best (count degrees into head, drop deg array; memory ↓, loc ↓ 2/3; runtime delta is build/measurement noise — hot loop unchanged) |
| 6 | true | 0.874148 | 8721 | 30 | new best (consolidation: int-encoded heap keys + compaction + local push/pop; memory ↓, loc ↓ 2/3; runtime tie) |
| 7 | true | 0.818784 | 7549 | 28 | new best (eliminate pos via head-cursor fill, inline build loops; memory ↓ −13%, loc ↓ 2/3; runtime tie) |
| 8 | true | 0.778196 | 8697 | 28 | reverted (tuple heap instead of int keys; memory +15%, runtime tie — int keys win) |
| 9 | true | 1.002190 | 8498 | 29 | reverted (array.array 'q' for to/wt; runtime +22%, memory +13% from build spike, loc +1 — all worse) |
| 10 | — | — | — | — | not run: solution.py == best.py (run 7); frontier mapped, re-grade would be a no-op |

**Final answer: run 7** — `best.py` (runtime 0.819s, peak 7549 KB, 28 LOC).
