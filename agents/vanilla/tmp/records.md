# Records

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 0.989229 | 26651 | 25 | new best (Dijkstra heapq, adj list of tuples) |
| 2 | yes | 1.16268 | 7954 | 37 | kept best (CSR+array: mem 3.3x better but runtime & loc worse, only 1/3) |
| 3 | yes | 1.186102 | 7954 | 24 | NEW BEST (compact CSR: mem 7954 & loc 24 both beat baseline) |
| 4 | yes | 1.223309 | 6709 | 21 | NEW BEST (32-bit wgt + array dist, mem 6709 & loc 21) |
| 5 | yes | 1.350422 | 6710 | 22 | kept best (zip-slice slower: per-pop slice alloc overhead) |
| 6 | yes | 1.365365 | 4423 | 21 | kept best (int-heap: mem 4423 great, but runtime worse & loc tie = 1/3) |
| 7 | yes | 1.805161 | 4424 | 20 | NEW BEST (int-heap + no early-exit: mem 4424 & loc 20; runtime sacrificed) |
| 8 | yes | 1.819297 | 4307 | 19 | NEW BEST (drop redundant src==dst guard + del pos: mem 4307, loc 19) |
| 9 | yes | 1.450601 | 4306 | 19 | NEW BEST (early-exit back, staleness-skip dropped: runtime 1.45 & mem 4306, loc 19) |
| 10 | yes | 1.408063 | 4306 | 19 | kept best (divmod: runtime within tolerance, all ties = 0 strict improvements) |
