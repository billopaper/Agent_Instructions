# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 0.992352 | 26653 | 25 | new best (Dijkstra heapq, adj list) |
| 2 | yes | 0.826707 | 10106 | 41 | new best (CSR flat-array adjacency: mem 26653->10106, rt -17%) |
| 3 | yes | 0.834553 | 10106 | 43 | reverted (local-bind push/pop: runtime tie, loc worse; heap calls not bottleneck) |
| 4 | yes | 1.148176 | 24598 | 46 | reverted (edge-dedup dict: all worse; dict overhead > parallel-edge savings, tests not multi-edge-heavy) |
| 5 | yes | 0.995622 | 10292 | 42 | reverted (array module to/wt: rt slower from boxing, mem unchanged; adjacency is not the mem bottleneck) |
| 6 | yes | 1.450343 | 8957 | 42 | reverted (int-encoded heap nd*n+v: mem 10106->8957 good, but divmod/bigint-mul made rt 1.45; pq IS a mem contributor) |
| 7 | yes | 0.864099 | 8957 | 45 | not promoted (1/3: mem improved 8957, rt tie, loc worse); kept in solution.py to refine LOC next |
| 8 | yes | 0.908761 | 8957 | 37 | NEW BEST (compacted shift-heap: mem 10106->8957, loc 41->37, rt tie within 10%) -> 2/3 |
| 9 | yes | 0.828596 | 8957 | 38 | not promoted vs run8 (rt recovered to 0.829 tie, mem tie, loc +1 worse); local-bind push/pop |
| 10 | yes | 0.821875 | 7552 | 37 | NEW BEST (del deg,pos frees n-arrays before search: mem 8957->7552, rt tie, loc tie) Pareto-dominates run8 |
