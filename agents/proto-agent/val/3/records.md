# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 0.94723 | 26653 | 25 | new best (classic heap Dijkstra) |
| 2 | yes | 0.981718 | 25504 | 28 | kept best (int-packed heap: mem better, runtime tie, loc worse) |
| 3 | yes | 1.034854 | 25504 | 23 | new best (compact int-pack: divmod + semicolon; mem & loc better, runtime tie) |
| 4 | yes | 1.153226 | 16129 | 24 | kept best (packed adjacency w*n+v: mem big drop, but runtime worse & loc +1) |
| 5 | yes | 1.150901 | 16129 | 19 | new best (packed adjacency + single-line if/semicolons; mem & loc better) |
| 6 | yes | 1.031876 | 9016 | 24 | new best (CSR via array('q'): mem big drop & runtime >10% better; loc worse) |
| 7 | yes | 1.057727 | 9030 | 21 | kept best (CSR + array dist: mem slightly worse (init bytes temp), only loc improved) |
| 8 | yes | 1.600889 | 6525 | 21 | new best (single packed CSR array w*n+v: mem & loc better; runtime worse from per-edge divmod) |
| 9 | yes | 1.030997 | 6526 | 21 | kept best (two int32 CSR arrays, no divmod: 35% faster, but mem +1KB tie & loc tie -> only 1 improved) |
| 10 | yes | 1.475455 | 6526 | 20 | kept best (int32 CSR, dropped early-exit for loc 20: runtime only 7.8% better=tie, mem tie -> only loc improved) |
