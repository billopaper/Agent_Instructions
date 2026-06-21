# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.001888 | 26653 | 25 | new best (canonical heapq Dijkstra, adjacency list) |
| 2 | true | 0.827004 | 10106 | 45 | new best (CSR flat arrays; runtime -17%, mem -62%, loc worse but 2/3 win) |
| 3 | true | 1.663791 | 9590 | 50 | reverted (typed array module: mem only -5%, runtime +101% from per-read boxing, 1/3) |
| 4 | true | 0.900300 | 8957 | 50 | reverted (packed-int heap: mem -11% but runtime tie + loc worse, only 1/3) |
| 5 | true | 0.814439 | 8957 | 35 | new best (packed-int heap, concise + divmod; mem -11%, loc -22%, runtime tie, 2/3) |
| 6 | true | 0.840770 | 8958 | 36 | reverted (zip-slice inner loop: slice alloc offset C iteration, 0/3) |
| 7 | true | 2.386814 | 28052 | 45 | reverted (explicit edge dedup via dict: ~3x worse time+mem, Dijkstra already absorbs multi-edges, 0/3) |
| 8 | true | 0.827587 | 8986 | 37 | reverted (settled bytearray vs float stale-check: runtime tie, mem +29KB, loc worse, 0/3) |

Final answer = best.py (run 5). Runs 9-10 left unused: remaining ideas are micro-variations the best-of style explicitly avoids and all tie/regress vs run 5; the promotion rule guarantees they could only revert.
