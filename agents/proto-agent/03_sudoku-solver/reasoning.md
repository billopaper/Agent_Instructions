# Reasoning trail — 03 sudoku-solver (proto-agent / prototype-driven)

## Initial approach and why

Prototype-driven style: grab a known-good idiom, get it correct first, then iterate on
metrics. For Sudoku the canonical idiom is **recursive backtracking with row/column/box
constraint sets**. The one non-obvious requirement from the spec is the "over-constrained
board returns False" case (e.g. two 5s already in a row): plain backtracking only checks
*empty* cells, so a board whose **given clues** already conflict would slip through. So the
seed version validates the pre-filled cells while building the constraint structures, and
returns False immediately on a duplicate clue. An already-complete valid board has no
empty cells, so backtracking returns True instantly and leaves it unchanged — both edge
cases fall out of the same structure.

## Iteration log

- **Run 1 — sets + sequential fill (correct, 2.036 s / 195 KB / 36 loc).** First correct
  solution, became best. Three lists of `set()` for rows/cols/boxes, an `empties` list,
  fill them in declaration order. Slow (2 s) because it fills empties in scan order with no
  search ordering — hard puzzles cause deep backtracking.

- **Run 2 — bitmask + MRV (0.687 / 52 / 57). PROMOTED (runtime, memory).** Two idiom swaps
  at once: (a) represent each unit's used digits as an **integer bitmask** instead of a set
  (`bit = 1<<v`, availability = `0x3FE & ~(rows|cols|boxes)`), and (b) **MRV heuristic** —
  at each step pick the empty cell with the *fewest* candidates (popcount of the mask),
  short-circuiting on a forced single. MRV is the big win on hard boards: it collapses the
  search tree. Runtime fell 2.04→0.69 s, memory 195→52 KB. LOC rose to 57 (more machinery).

- **Run 3 — drop per-level list slicing (0.598 / 64 / 54). PROMOTED (runtime, loc).** Run 2
  rebuilt the candidate list every recursion (`remaining[:best]+remaining[best+1:]`).
  Replaced that with a fixed `empties` list and skip already-filled cells (`if board[r][c]`).
  Runtime −13%, loc −3. Surprise: peak memory *rose* 52→64 KB. So the slicing version was
  actually lighter on peak memory — the skip version keeps the full-length list live and
  iterates it at every depth.

- **Run 4 — precomputed popcount table (0.400 / 64 / 55). KEPT best (only runtime).**
  Replaced `bin(av).count("1")` with a module-level `POP = bytes(...)` lookup. Runtime
  −33% (0.598→0.400) — counting set bits was a real hot-path cost. But loc went +1 (the
  table line) and memory tied at 64, so only **1 of 3** improved → not promoted.

- **Run 5 — popcount table + merged inits (0.415 / 64 / 53). PROMOTED (runtime, loc).**
  Same speed as run 4, but reclaimed the table's line by merging the three accumulator
  inits into `rows, cols, boxes = ([0]*9 for _ in range(3))`. Now runtime −31% **and** loc
  −1 vs the run-3 best → 2 of 3.

- **Run 6 — int.bit_count(), drop the table (0.408 / 64 / 52). KEPT best (only loc).**
  Confirmed Python ≥3.10 (no error). `av.bit_count()` is as fast as the table and removes
  the table line (loc 52). But memory stayed 64 — **proving the POP table was never the
  memory cost**; the 52→64 jump came purely from the run-3 structural change. Only loc
  improved → kept.

- **Run 7 — in-place swap MRV, shrinking scan (0.383 / 61 / 53). KEPT best (only memory).**
  Tested the memory hypothesis: keep a single `empties` list, but scan only `empties[k:n]`
  and swap the chosen cell to position `k` (swap back on backtrack). No per-level allocation
  *and* a shrinking scan like the slicing version. Memory dropped 64→61, runtime −7.7%
  (a tie, just under the 10% bar), loc tied at 53 → only 1 of 3.

- **Run 8 — swap MRV + merged FULL/n (0.390 / 61 / 52). PROMOTED (memory, loc).** Same as
  run 7 but `FULL, n = 0x3FE, len(empties)` on one line → loc 52. Now memory −3 **and** loc
  −1 vs run-5 best → 2 of 3. This is the balanced sweet spot: fast, lean, compact.

- **Run 9 — precompute box index in 3-tuples + packed lines (0.357 / 64 / 43). KEPT best.**
  Stored `(r, c, b)` so the box index isn't recomputed in the hot scan, and packed the
  triple bitmask updates onto single lines. LOC crashed to 43 (−9) and runtime −8.5%, but
  the fatter 3-tuples pushed memory 61→64. Runtime tie, memory worse → only loc improved.

- **Run 10 — flat-int empties + packed lines (0.518 / 39 / 42). PROMOTED (memory, loc).**
  Stored each empty as a single int `r*9+c` instead of a tuple. CPython caches ints 0–80 as
  singletons, so `empties` is ~50 shared references rather than ~50 distinct tuple objects —
  peak memory plunged 61→39 KB. Combined with the line-packing, loc hit 42. The cost:
  `divmod()` per scanned cell made runtime regress 0.390→0.518 s (+33%). Under the 2-of-3
  ratchet, memory and loc both strictly improved → promoted. This is the final answer.

## What worked, what didn't, key insight

- **Worked:** the bitmask + MRV idiom (run 2) is the single decision that mattered — one
  swap took runtime from 2.0 s to 0.69 s. Everything after was metric-trading, not
  algorithmic. `int.bit_count()` and the popcount table both killed the set-counting cost.
  The flat-int-as-cell trick is the memory unlock (distinct tuples → cached-int refs).
- **Didn't / surprised me:** my intuition that *avoiding* list allocation would lower peak
  memory was backwards (run 3) — keeping the full list live at every depth costs more than
  short-lived slices. And precomputing the box index (run 9) helped runtime but the extra
  tuple width cost more memory than it saved.
- **Key insight:** with a fixed algorithm, the three metrics are in tension and the 2-of-3
  ratchet walks `best.py` along a Pareto frontier. Memory and LOC move together and are
  *deterministic* to improve (data representation + line packing), while runtime is noisy
  and capped by the algorithm — so the ratchet naturally pulled the final answer toward the
  low-memory / low-LOC corner, trading runtime for it.

## Why best.py is the final answer

`best.py` is the run-10 version (39 KB / 42 loc / 0.518 s). It is correct on all 10 hidden
tests and is the global optimum on **two of three** metrics (memory and LOC) across every
attempt — the promotion ratchet only ever moved here on strict 2-of-3 improvements, so no
earlier version dominates it. The honest tradeoff: run 8 (0.390 / 61 / 52) is ~25% faster.
If runtime were weighted highest, run 8 would be preferable; under the experiment's equal
2-of-3 promotion rule, run 10 is the correct final selection.
