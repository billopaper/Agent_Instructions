# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 0.950591 | 26653 | 25 | new best (first correct: Dijkstra + heapq, list adjacency) |
| 2 | yes | 0.963637 | 26653 | 26 | reverted (localized heap fns + INF const; runtime tie, loc +1, no gain) |
| 3 | yes | 1.1903 | 7964 | 47 | kept best (CSR/array adjacency: memory -70%, but runtime +25% & loc +22; only 1/3 improved) |
| 4 | yes | 1.29531 | 7965 | 48 | kept best (CSR + zip-slice iteration; slower than indexing, slice alloc overhead) |
| 5 | yes | 0.867669 | 24469 | 43 | kept best (bidirectional Dijkstra: memory -8%, runtime -8.7% TIE, loc +18; only 1/3 — runtime just under 10% threshold) |
| 6 | yes | 0.875371 | 24433 | 45 | kept best (bidirectional + nd<best pruning; neutral - stop-condition already cuts late work; still 1/3) |
| 7 | yes | 1.004374 | 5411 | 68 | kept best (bidirectional + CSR: memory -80% = champion, dominates run3; but runtime +6% & loc +43; still 1/3) |
| 8 | yes | 0.95054 | 26653 | 22 | kept best (compact forward Dijkstra; identical runtime/memory, loc -3; weakly dominates run1 but only 1/3 improved -> rule blocks) |
