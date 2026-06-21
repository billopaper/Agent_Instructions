# Records — 03 Sudoku Solver (oop-agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.725984  | 16             | 96  | new best (first correct) |
| 2   | true    | 0.493893  | 16             | 72  | new best (runtime -32%, loc -24; mem tie) |
| 3   | true    | 0.482891  | 16             | 71  | reverted (precompute box idx; runtime -2% = tie, only loc improved) |
| 4   | true    | 0.517170  | 40             | 91  | reverted (naked-single propagation + list slicing; worse on all 3 — slicing/placed lists cost mem+time) |
| 5   | true    | 0.601682  | 12             | 66  | new best (int-encoded cells: mem 16->12, loc 72->66; runtime +22% but 2/3 improved & memory is top metric) |
| 6   | true    | 0.579983  | 12             | 65  | reverted (divmod -> //,%; runtime -3.6% = tie, only loc improved) |
| 7   | true    | 0.518453  | 12             | 65  | new best (module-level (r,c,box) table: runtime -14%, loc 66->65; mem 12 tie -> module consts not counted in peak) |
| 8   | true    | 0.477176  | 12             | 64  | reverted (full self-access in _fill; runtime -7.9% = tie, loc -1 only; mem still 12 -> not frame-dominated). NOTE: weakly nicer than run7 but only 1/3 strict, rule keeps run7 |
| 9   | true    | 1.437406  | 84             | 56  | reverted (CONTRAST: set objects per unit instead of bitmasks; ~2.8x slower, 7x memory, loc 56. Confirms bitmask int representation is the source of the mem/runtime wins) |

Final answer: best.py = run 7 (bitmask masks + module-level (r,c,box) table + MRV + in-place pop/swap). Metrics 0.518 s / 12 kB / 65 LOC. Run 10 left unused — converged; solution.py == best.py.
