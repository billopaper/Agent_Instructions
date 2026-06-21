# FizzBuzz — run log (smart-pattern agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.001848  | 38             | 3   | new best (cyclic period-15 lookup table) |
| 2   | true    | 0.001645  | 38             | 1   | new best (table folded into default-arg, single line; runtime+loc both lower) |
| 3   | true    | 0.00162   | 38             | 1   | kept best (classic 3-modulo one-liner; only runtime lower = 1/3, within noise) |
| 4   | true    | 0.00147   | 37             | 7   | new best (template `base * k` + patch number slots; runtime+memory both lower = 2/3, per promotion rule) |
| 5   | true    | 0.002097  | 46             | 1   | kept best (one-line comprehension over repeated tuple; intermediate + output both alive -> slower & more mem, only loc lower = 1/3) |
| 6   | true    | 0.001619  | 37             | 8   | kept best (divmod exact-build `base*q+base[:r]`; mem still 37 floor, runtime not lower = 0/3) |
| 7   | true    | 0.002076  | 38             | 3   | kept best (itertools.cycle+zip, modulo-free; iterator overhead -> slower, only loc lower = 1/3) |
| 8   | true    | 0.001514  | 37             | 5   | kept best (run-4 algo, base hoisted to default-arg, inlined if; loc 5 but runtime not strictly lower = 1/3) |
| 9   | true    | 0.001544  | 37             | 5   | kept best (re-sample of run-8 form; runtime reproducibly ~0.0015 > 0.00147, only loc lower = 1/3) |
| 10  | true    | 0.001536  | 37             | 7   | final (restored best.py = run-4 code into solution.py; solution.py == best.py, runs exhausted) |

**Final answer: `best.py` = run 4** — `template * k` repetition + in-place patch of number slots.
Metrics of record: runtime 0.00147 s, peak memory 37 KB, loc 7. It is the only solution that
achieved both the runtime minimum (0.00147) and the memory floor (37 KB); no later run beat 2 of 3.
