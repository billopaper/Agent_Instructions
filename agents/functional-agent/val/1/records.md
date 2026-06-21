# Records — weighted-shortest-path (functional agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.95932   | 26651          | 24  | new best (Dijkstra, list-of-lists adjacency, binary heap) |
| 2   | true    | 0.747559  | 10103          | 37  | new best (CSR flat-list adjacency; mem −62%, runtime −22%, loc +13 → 2/3 improved) |
| 3   | true    | 1.059839  | 8188           | 41  | reverted (CSR with array module; mem −19% but runtime +42% from int boxing, loc +4 → only 1/3) |
| 4   | true    | 0.702358  | 10103          | 39  | reverted (localized push/pop + zip-slice inner loop; runtime −6% = within tie band, loc +2 → 0/3) |
| 5   | true    | 0.938426  | 10289          | 35  | kept best (compact array CSR but off/pos as lists → mem +2%, only loc improved = 1/3) |
| 6   | true    | 1.41914   | 8188           | 35  | new best (all-array CSR incl. off/pos; mem −19% & loc −2 = 2/3; runtime regresses but memory has higher rank) |
| 7   | true    | 1.524104  | 7954           | 34  | new best (count degrees directly into off, prefix-sum in place; drops deg list → mem −3% & loc −1 = 2/3) |
| 8   | true    | 1.765021  | 6709           | 33  | new best (wgt as 'i', dist as array('d'), fold degree-count to 1 line → mem −16% & loc −1 = 2/3; weights fit int32) |
| 9   | true    | 1.628474  | 6592           | 32  | new best (dist as array('i') with 2^31-1 sentinel, fold fill to 1 line → mem −2% & loc −1 = 2/3; runtime tie) |
| 10  | true    | 1.646352  | 6592           | 32  | kept best (final confirmation grade of best.py; identical solution, matches metrics) |

**Final answer:** `best.py` = run 9 (all-array CSR Dijkstra). Metrics: runtime ~1.63s, peak_memory 6592 KB, loc 32. Correct 13/13.
