# Records — weighted-shortest-path (best-of agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.13589 | 26653 | 26 | new best — canonical Dijkstra, list-of-lists adjacency |
| 2 | true | 1.331603 | 7957 | 38 | kept best — CSR arrays: 3× less memory but slower + longer (1/3 improved) |
| 3 | true | 1.480155 | 7958 | 39 | kept best — CSR + zip-over-slices inner loop, slower still (slice alloc) |
| 4 | true | 1.286908 | 7957 | 30 | kept best — compact CSR (30 loc); memory-only win, loc still > 26 (1/3) |
| 5 | true | 0.953339 | 26653 | 16 | new best — compact list-of-lists + localized push/pop: runtime −16% & loc 16 (2/3) |
| 6 | true | 1.379075 | 41142 | 21 | kept best — multi-edge dedup: dict costs MORE memory + slower (0/3) |
| 7 | true | 0.974983 | 25504 | 16 | kept best — int-packed heap (d*n+u): memory −1149kb but runtime tie, loc tie (1/3) |
| 8 | true | 0.99173  | 25504 | 15 | new best — int-packed heap + merged setup line: memory + loc both lower, runtime tie (2/3) |
