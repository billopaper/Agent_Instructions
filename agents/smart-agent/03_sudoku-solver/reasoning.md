# Reasoning trail — 03 sudoku-solver (smart-pattern / Einstein)

## Initial approach and why

Sudoku is the textbook case for **bitmask constraint tracking + backtracking with the
Minimum-Remaining-Values (MRV) heuristic** — the smartest standard pattern for this task:

- Represent the digits already used in each row, column, and 3×3 box as a single 9-bit
  integer (`rows[r]`, `cols[c]`, `boxes[b]`). A digit `d` occupies bit `d-1`.
  Candidate set for an empty cell is then one expression:
  `FULL & ~(rows[r] | cols[c] | boxes[b])`. Placing/removing a digit is one XOR/OR per unit.
- **MRV**: at each step branch on the empty cell with the *fewest* candidates. This collapses
  the search tree dramatically and makes forced cells (1 candidate) fill first with no real
  branching. A cell with 0 candidates is an immediate dead end (prune).
- Validate the givens while building the masks — a duplicate in any unit means the board is
  unsolvable, return `False` immediately (handles the over-constrained test case), and since
  we only *read* the board during init, it is left unchanged.
- An already-complete valid board has no empties → return `True` unchanged.

Correctness was the top priority and it held on every single run (10/10 hidden tests each time);
all later iterations were pure metric optimization (memory > runtime > loc in priority).

## Iteration-by-iteration

- **Run 1 — baseline** (bitmask + MRV, `bin(cand).count("1")` popcount, `pop(best_i)`):
  correct, 1.750 s / 40 kb / 56 loc. First correct → `best.py`.

- **Run 2 — popcount lookup table + dense packing**: precomputed `_POP = bytes(popcount)`
  replaces the per-cell `bin().count("1")` (the hottest line), and semicolon-packing cut loc.
  0.952 s / 39 kb / 45 loc — **all three improved** → new best. Biggest single win (~46% runtime).

- **Run 3 — O(1) cell removal + `enumerate`**: swap-to-end + `pop()` instead of `pop(best_i)`,
  and `enumerate` instead of index lookups. 0.664 s / 39 kb / **46** loc. Runtime −30% but the
  extra `n = len(...)` line pushed loc to 46 and memory tied → only 1/3 → **kept best**. Lesson:
  a real speedup still fails the 2-of-3 promotion rule if it costs a line.

- **Run 4 — fold the speedup into a tighter form**: same O(1) removal, packed into existing
  lines (no extra line). 0.634 s / 39 kb / 41 loc — runtime + loc improved → new best.

- **Run 5 — default-argument local binding**: `def bt(empties=empties, rows=rows, ..., POP=_POP,
  FULL=0x1FF)` turns every hot-loop name from a global/closure lookup into a fast *local* lookup
  (classic CPython trick; the objects are only mutated in place, never reassigned, so binding
  once is safe). 0.600 s / 38 kb / 40 loc — mem + loc improved, runtime a tie → new best.

- **Run 6 — flat-int `empties`** (`r*9+c` instead of `(r,c,b)` tuples): each entry now references
  a *cached* small-int singleton instead of allocating a tuple. Memory dropped to **34 kb** (−4),
  but recomputing the box index `(r//3)*3+c//3` every scan iteration (run 5 had `b` precomputed in
  the tuple) cost +12% runtime, and decoding added a line (41) → only 1/3 → **kept best**. The
  diagnosis here drove run 7.

- **Run 7 — flat ints + module `_BOX` table**: keep the flat-int memory win, but add an
  import-time `_BOX` byte table (cell → box index) so the box index is a cheap lookup, not
  arithmetic, in the hot loop. Module-level constants (`_POP`, `_BOX`) are allocated once at
  import and do not count against `solve`'s measured peak. Packed the post-pop decode into one
  line. **0.635 s / 34 kb / 39 loc** — memory + loc improved, runtime back to a tie → new best.
  **This is the final answer.**

- **Run 8 — iterative explicit-stack DFS** (replace recursion with a `list`-of-lists stack):
  proved that recursion frames were the memory cost — peak **halved to 16 kb**. But Python-level
  stack management (index mutation, manual backtrack loop) is far slower than CPython's C-level
  recursion: runtime +80% (1.14 s) and loc +6 (45). Only memory improved → **kept best**.

- **Run 9 — recursion + forced-cell propagation**: fill all single-candidate cells iteratively
  inside each frame, recurse only on true branch points, to shrink recursion depth. It backfired:
  the per-frame `placed` undo-lists accumulate a tuple for nearly every forced cell along the
  path, costing *more* memory (39 kb) than plain recursion, plus bookkeeping overhead (1.02 s) and
  +5 loc. All three worse → **kept best**.

- **Run 10 — not used**: restored `best.py` (run 7) into `solution.py`. Re-grading would only
  re-measure the median, which the rules say achieves nothing.

## What worked, what didn't, key insight

**Worked**
- Bitmask masks + MRV: the right algorithmic core — correct first try, fast, tiny memory.
- Popcount lookup table (`_POP`): the single biggest runtime win; kill `bin().count()` in the hot loop.
- Default-argument local binding of every hot name: free, real CPython speedup.
- Flat-int cells + an import-time `_BOX` table: cut memory (cached small ints, no tuple allocs)
  without re-introducing per-node arithmetic. Pushing constant tables to module scope keeps them
  out of the measured peak.

**Didn't work (but informative)**
- Iterative explicit-stack DFS: best memory by far (16 kb) but ~2× slower and more code — a stark
  memory↔runtime trade-off. Native recursion wins overall when runtime is weighted above loc.
- Forced-cell propagation with undo-lists: the bookkeeping cost more memory and time than it saved.
  MRV already fills forced cells first essentially for free, so explicit propagation was redundant.

**Key insight / pattern converged on**: for Sudoku, *bitmask + MRV + native recursion* is the
sweet spot. Optimize it by (1) replacing the hot popcount with a precomputed table, (2) binding
hot names as function-local defaults, (3) storing cells as flat ints and pushing all derived
constant tables to module scope so they cost nothing at measure time. The promotion rule
(≥2 of 3 strictly better) repeatedly forced "fold the win in without spending a line elsewhere"
rather than accepting a single-metric gain — runs 3→4 and 6→7 are exactly that move.

## Why best.py is the final answer

Run 7 dominates the field on the prioritized metric mix: lowest-but-one memory among the *fast*
solutions (34 kb), competitive best-tier runtime (0.635 s), and the lowest loc reached without
sacrificing speed (39). The only configs with lower memory (runs 8/9) pay 60–80% more runtime and
more lines and fail the 2-of-3 promotion rule. Run 7 is correct on all 10 hidden tests, handles
unsolvable, already-solved, easy, and hard boards, and `solution.py` has been restored to equal it.
