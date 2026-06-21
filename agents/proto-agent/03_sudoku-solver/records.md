# Records — 03 sudoku-solver (proto-agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 2.035992  | 195            | 36  | new best (first correct) |
| 2   | true    | 0.686924  | 52             | 57  | new best (bitmask+MRV: runtime & memory improved) |
| 3   | true    | 0.597977  | 64             | 54  | new best (no per-level slicing: runtime -13% & loc improved; memory rose to 64) |
| 4   | true    | 0.400056  | 64             | 55  | kept best (popcount table: runtime -33% but loc +1 & memory tie = only 1/3 improved) |
| 5   | true    | 0.414845  | 64             | 53  | new best (popcount + merged inits: runtime -31% & loc improved) |
| 6   | true    | 0.407850  | 64             | 52  | kept best (int.bit_count, no table: loc improved but memory tie & runtime tie = 1/3) |
| 7   | true    | 0.383331  | 61             | 53  | kept best (in-place swap MRV, shrinking scan: memory improved but loc tie & runtime tie = 1/3) |
| 8   | true    | 0.389664  | 61             | 52  | new best (swap MRV + merged FULL/n: memory & loc improved) |
| 9   | true    | 0.357156  | 64             | 43  | kept best (precompute box in 3-tuples + packed lines: loc -9 but memory +3 & runtime tie = 1/3) |
| 10  | true    | 0.517836  | 39             | 42  | new best (flat-int empties + packed lines: memory -22 & loc -10 improved; runtime +33% worse) |

Final best.py = run 10 (runtime 0.517836 s, peak_memory 39 KB, loc 42).
Algorithm constant since run 2 (bitmask + MRV backtracking); runs 3-10 only traded between the three metrics under the 2-of-3 promotion ratchet.
