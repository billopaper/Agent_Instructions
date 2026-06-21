# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 0.973187 | 26651 | 25 | new best (first correct: Dijkstra + binary heap, dist=None sentinel) |
| 2 | true | 1.308474 | 18633 | 42 | reverted (CSR flat arrays: memory -30% but runtime +34%, loc +17 — only 1/3 improved) |
| 3 | true | 0.952749 | 26651 | 25 | kept best (localized heap + INF sentinel: runtime tie within 10%, mem/loc tie — 0/3) |
| 4 | true | 0.958628 | 25503 | 28 | kept best (int-packed heap nd*n+v: mem -1MB but loc +3, runtime tie — 1/3) |
| 5 | true | 1.331718 | 6710 | 36 | kept best (CSR two-pass, no edge list: memory -75%! but runtime +37%, loc +11 — 1/3) |
| 6 | true | 1.278609 | 6710 | 22 | NEW BEST (compressed CSR: memory 6710<26651 AND loc 22<25 — 2/3, runtime regress accepted) |
| 7 | true | 1.274445 | 6710 | 20 | kept best (CSR + .tolist hot loop, loc 20: only loc improved, mem/runtime tie — 1/3) |
| 8 | true | 1.330181 | 4424 | 20 | NEW BEST (CSR + packed-int heap nd*n+v: memory 4424<6710 AND loc 20<22 — 2/3) |
| 9 | true | 1.467152 | 4439 | 19 | kept best (import-combine loc 19 + array('q') dist: only loc improved; b'\xff'*8n temp spike raised mem to 4439, qualified heapq calls slowed runtime — 1/3) |
| 10 | true | 1.353017 | 4424 | 20 | final confirm of best (solution.py == best.py, 13/13) |

**Final best = run 8.** correct 13/13 · runtime 1.353s · peak_memory 4424 kb · loc 20.
