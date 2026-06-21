# Run Log — train/01_fizzbuzz (OOP agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.003104  | 42             | 21  | new best (rule-based class model) |
| 2   | true    | 0.001583  | 38             | 14  | new best (single class, direct modulo — all 3 improved) |
| 3   | true    | 0.001453  | 38             | 9   | new best (15-cycle dict pattern, inlined — runtime+loc improved) |
| 4   | true    | 0.001526  | 38             | 6   | kept best (cycle tuple, loc 6 but runtime regressed — only 1/3 improved) |
| 5   | true    | 0.001502  | 38             | 7   | kept best (cycle tuple + local bind — runtime still noise-bound, only 1/3) |
| 6   | false   | 0.002407  | 70             | 10  | error (slice-stamping: off-by-one in strided count; worse metrics) — reverted |
| 7   | true    | 0.001465  | 38             | 8   | kept best (itertools.cycle + zip — runtime tied, only loc improved 1/3) |
| 8   | true    | 0.001425  | 38             | 7   | new best (lean dict.get, single-line dict, local bind — runtime+loc improved 2/3) |
| 9   | true    | 0.001416  | 38             | 6   | new best (drop local bind — loc 6, runtime improved; bind cost is noise) — runtime+loc 2/3 |
| 10  | true    | 0.001445  | 38             | 5   | kept best (callable-object idiom, loc 5 but runtime regressed — only 1/3) — restored best (run 9) |

**Final answer = best.py = run 9** (runtime 0.001416s, peak_memory 38 KB, loc 6). solution.py restored to match.
