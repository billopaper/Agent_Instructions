# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.043099 | 26653 | 24 | new best (heap Dijkstra, list-of-lists adj) |
| 2 | true | 0.829124 | 9871 | 37 | new best (CSR flat-array Dijkstra; mem -63%, rt -20%, loc +13) |
| 3 | true | 1.436633 | 9458 | 40 | reverted (array('q') CSR; mem -4% but rt +73% from int boxing, only 1/3 improved) |
| 4 | true | 0.715420 | 7747 | 54 | new best (bidirectional Dijkstra on CSR; rt -14%, mem -22%, loc +17) |
| 5 | true | 0.754480 | 7688 | 40 | new best (compact table-driven bidir, lazy-delete drops settled bytearrays; loc 54->40, mem -1%, rt tie) |
| 6 | true | 0.720975 | 7688 | 48 | reverted (explicit bidir, local-bound push/pop; rt -4% tie, mem tie, loc +8 worse) |
| 7 | true | 1.520468 | 7688 | 40 | reverted (interleaved single-array CSR; rt +101% from 2*p arithmetic, mem identical, no gain) |
| 8 | true | 0.725519 | 7652 | 40 | kept best (added `nd < mu` prune; mem -36kb but rt tie & loc tie -> only 1/3, blocked by rule) |
| 9 | true | 0.744407 | 7652 | 38 | new best (run 8 prune + collapsed 2 lines; mem -36kb & loc -2, rt tie -> 2/3) |
| 10 | true | 0.774680 | 7592 | 37 | new best FINAL (int-encoded heap keys dist*n+node, no tuples; mem -60kb & loc -1, rt tie -> 2/3) |
