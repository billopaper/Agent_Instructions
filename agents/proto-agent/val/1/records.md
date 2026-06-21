# Records — Weighted Shortest Path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | yes     | 1.18045   | 30011          | 23  | new best (Dijkstra, list-of-lists adj, heap) |
| 2   | yes     | 0.769288  | 10103          | 44  | new best (CSR flat-list adj; runtime -35%, mem -66%, loc worse but 2/3 improved) |
| 3   | yes     | 1.004943  | 11534          | 45  | reverted (array('q') CSR; runtime AND mem both worse — boxing on access + byte-buffer spike) |
| 4   | yes     | 0.641783  | 7917           | 67  | new best (bidirectional Dijkstra on CSR; runtime -17%, mem -22% from smaller heaps; loc worse but 2/3 improved) |
| 5   | yes     | 0.641293  | 7918           | 71  | reverted (balanced-frontier bidirectional; runtime tie, mem tie, loc worse — alternation already balanced) |
| 6   | yes     | 0.634734  | 7858           | 46  | new best (compact bidirectional: lazy d<=dist skip drops seen arrays; mem lower, loc 67->46, runtime tie; 2/3 improved) |
| 7   | yes     | 1.168682  | 7858           | 45  | reverted (interleaved single adj array; runtime ~2x worse from *2 arith + step-2 range; mem tie) |
| 8   | yes     | 0.613947  | 7624           | 38  | new best (reuse deg as fill pointer -> one fewer n-list; mem 7858->7624, loc 46->38, runtime tie; 2/3 improved) |
| 9   | yes     | 0.751949  | 9868           | 29  | reverted (unidirectional compact, same CSR; runtime +22%, mem +29% vs best; loc lowest but only 1/3 -> isolates bidirectional as the runtime+memory driver) |
