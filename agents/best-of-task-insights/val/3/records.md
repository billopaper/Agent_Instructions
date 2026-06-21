# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.201207 | 30012 | 22 | new best (heapq Dijkstra, adj list of tuples) |
| 2 | true | 0.951506 | 26653 | 25 | new best (tentative-dist relaxation: push only on improvement → fewer heap entries) |
| 3 | true | 1.302715 | 7957 | 37 | kept best (CSR on array: memory −70% but runtime +37%, loc worse → only 1/3) |
| 4 | true | 0.968225 | 25504 | 27 | kept best (int-encoded heap: memory −1149kb only, runtime tie, loc worse → 1/3; heap is small vs adj) |
| 5 | true | 0.836512 | 9871 | 36 | new best (CSR on lists: runtime −12% AND memory −63% → 2/3; list access avoids array boxing, flat layout beats tuples) |
| 6 | true | 1.301493 | 7957 | 25 | new best (CSR on array, minified: memory floor 7957 AND loc 25 → 2/3; runtime +56% is the trade) |
| 7 | true | 1.356985 | 7957 | 24 | kept best (array dist: memory unchanged 7957, loc 24 → only 1/3; peak is the edge arrays, not dist) |
| 8 | true | 1.367718 | 6712 | 24 | new best (wt as 32-bit 'I': memory 6712 AND loc 24 → 2/3; weights fit 32-bit, sums stay in 64-bit dist) |
| 9 | true | 1.356625 | 4425 | 23 | new best (int-encoded heap key nd*n+v + merged init line: memory −34% AND loc 23 → 2/3; heap was a big part of peak) |
| 10 | true | 0.850857 | 8723 | 23 | kept best (list-CSR + int-heap: runtime 0.851 fast corner but memory 8723 ≈2x run9 → 1/3; documents runtime/memory frontier) |
