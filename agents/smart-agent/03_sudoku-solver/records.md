# Records — 03 sudoku-solver (smart-agent)

| run | correct | runtime_s | peak_mem_kb | loc | action |
|-----|---------|-----------|-------------|-----|--------|
| 1   | true    | 1.750247  | 40          | 56  | new best (bitmask + MRV backtracking) |
| 2   | true    | 0.952281  | 39          | 45  | new best (popcount table + semicolon packing; all 3 improved) |
| 3   | true    | 0.664294  | 39          | 46  | kept best (runtime -30% but loc 46>45 & mem tie -> only 1/3) |
| 4   | true    | 0.634308  | 39          | 41  | new best (O(1) swap-pop removal + tighter packing; runtime+loc improved) |
| 5   | true    | 0.599586  | 38          | 40  | new best (default-arg local binding of hot names; mem+loc improved, runtime tie) |
| 6   | true    | 0.669091  | 34          | 41  | kept best (flat-int empties: mem -4 but runtime +12% & loc +1 -> only 1/3) |
| 7   | true    | 0.635431  | 34          | 39  | new best (flat-int empties + module _BOX table fixes runtime; mem+loc improved) |
| 8   | true    | 1.140809  | 16          | 45  | kept best (iterative explicit-stack DFS: mem -53% but runtime +80% & loc +6 -> 1/3) |
| 9   | true    | 1.024352  | 39          | 44  | kept best (recursion + forced-cell propagation: all 3 worse; placed-lists cost memory) |
| 10  | -        | -         | -           | -   | not used; restored best.py (run 7) into solution.py as final answer |

**Final answer = run 7**: runtime 0.635s, peak_memory 34 kb, loc 39.
