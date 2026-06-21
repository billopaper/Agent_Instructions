# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.985385 | 26653 | 22 | new best (heapq Dijkstra, list-of-tuples adj) |
| 2 | true | 1.969384 | 9047 | 41 | kept best (CSR flat-array adj: mem -3x, runtime tie, loc +19 → only 1/3 improved) |
| 3 | true | 2.459879 | 18408 | 24 | kept best (packed-int adj: mem mid, runtime +24% WORSE from bit-op unpack, loc +2 → dominated) |
| 4 | true | 1.835823 | 5976 | 55 | kept best (bidirectional Dijkstra on CSR: mem best 5976, runtime -7.5% (TIE, <10%), loc +33 → only 1/3 improved) |
| 5 | true | 1.772161 | 5976 | 59 | NEW BEST (run4 + localized heappush/heappop: runtime -10.7% (>10%) + mem -4.5x vs run1 → 2/3 improved, loc worse) |
| 6 | true | 1.710719 | 5976 | 27 | kept best (compressed + direction-unified bidirectional: loc 59→27, mem/runtime tie → only loc improved, 1/3) |
| 7 | true | 1.701804 | 5196 | 28 | NEW BEST (run6 + `del pos` frees CSR cursor: mem 5976→5196 + loc 59→28 vs run5 → 2/3 improved) |
