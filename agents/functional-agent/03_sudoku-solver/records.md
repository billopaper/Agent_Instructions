# Records — 03 sudoku-solver (functional agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 1.040462  | 83             | 64  | new best (first correct) |
| 2   | true    | 0.864166  | 83             | 58  | new best (runtime -17%, loc -6) |
| 3   | true    | 0.591748  | 57             | 58  | new best (runtime -31%, mem -26) |
| 4   | true    | 1.318381  | 39             | 58  | reverted (packed-int masks: mem -18 but runtime +123%; int reads alloc per access) |
| 5   | true    | 0.594602  | 57             | 57  | kept best (drop popcount table, use int.bit_count(): loc -1 only; runtime/mem tie → rule needs 2 of 3) |
| 6   | true    | 0.540902  | 43             | 73  | reverted (naked-single propagation: mem -14, runtime tie; loc +15 too costly) |
| 7   | true    | 0.558021  | 43             | 58  | reverted (propagation + min()/key MRV, compacted: mem -14 but loc tie at 58) |
| 8   | true    | 0.559201  | 43             | 56  | new best (propagation, docstring/stmt trim: mem -14 AND loc -2; runtime tie) |
| 9   | true    | 2.087941  | 38             | 54  | reverted (drop MRV, branch first cell: mem/loc improved but runtime +273% — would game 2-of-3, refused) |
| 10  | true    | 0.560307  | 43             | 56  | final confirmation of best (solution.py == best.py) |

**Final answer = best.py (run 8):** correct 10/10, runtime ~0.56s, peak memory 43 KB, loc 56.
