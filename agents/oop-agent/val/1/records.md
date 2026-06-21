# Records — Weighted Shortest Path (oop-agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.931094  | 26651          | 44  | new best (first correct) |
| 2   | true    | 0.762341  | 7837           | 56  | new best (CSR: runtime −18%, mem −71%; loc worse → 2/3) |
| 3   | true    | 0.909451  | 6592           | 46  | new best (32-bit wt + prefix-sum build: mem −16%, loc −10; runtime worse → 2/3) |
| 4   | true    | 0.899115  | 6592           | 47  | reverted (None sentinel ≈ tie runtime, loc worse — build, not sentinel, drove speed) |
| 5   | true    | 0.738413  | 6592           | 46  | kept best (fast list-deg build restored runtime −19%, but mem/loc tie → only 1/3) |
| 6   | true    | 0.731935  | 6592           | 44  | new best (run 5 build + dropped docstrings: runtime −19%, loc −2 → 2/3) |
| 7   | true    | 0.777769  | 6592           | 44  | reverted (dist as array('q') -1 sentinel: peak mem unchanged → dist isn't the peak driver) |
| 8   | true    | 0.795220  | 6593           | 44  | reverted (zip over array slices: slice alloc per node negates C-iteration gain) |
| 9   | true    | 0.769749  | 6621           | 48  | reverted (done bytearray skip: sparse graphs → no heap shrink, mem +29, loc worse) |

Final answer: best.py = run 6 (runtime 0.732 / mem 6592 / loc 44).
Run 10 deliberately unused — design space converged; memory floor (6592) and runtime floor
(~0.73) both confirmed across 4+ variants, and re-grading identical code only chases noise.
