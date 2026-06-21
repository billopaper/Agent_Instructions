# Reasoning — Weighted Shortest Path (OOP agent)

## Problem framing

Single-pair minimum-weight path in a **weighted undirected graph**, non-negative
integer weights, possibly large (thousands of nodes/edges). Multi-edges → smallest
weight wins; self-loops → ignorable; `src == dst → 0`; unreachable → `-1`.

Non-negative weights ⇒ **Dijkstra with a binary heap** is the right tool (no need for
Bellman-Ford). Multi-edges need no pre-dedup: Dijkstra's relaxation naturally keeps the
minimum arriving cost, so I never have to collapse parallel edges explicitly. Self-loops
are dropped at build time (`u == v`), since they can never improve a path.

## Initial OOP approach (run 1)

Per my style, I modelled two responsibilities as two classes:
- `Graph` — owns the adjacency list and edge normalization (drop self-loops, store both
  directions).
- `DijkstraSolver` — owns the search (lazy-deletion heap Dijkstra).

Correct on the **first run**: 13/13, runtime 1.069 s, mem 30012 kb, loc 45. Good baseline.

## Optimization trail (runs 2–8)

The promotion rule (improve ≥2 of 3 metrics; runtime only counts if >10% better) shaped
every decision. Each step targeted a specific bottleneck:

- **Run 2 — collapse to one class, hot-loop locals.** Merged the two classes, built
  adjacency in the constructor, bound `push`/`pop`/`adj` as locals. Result: loc 45→34 but
  runtime/mem unchanged. Only 1 metric improved → **kept best**. Lesson: micro-locals
  don't move runtime when C-level `heapq` dominates.

- **Run 3 — tentative-distance Dijkstra.** Switched from "push every unfinalized neighbour"
  to classic relaxation: keep a `dist[]` of best-known tentative costs and **push only on
  strict improvement**. Fewer heap pushes on graphs with many/parallel edges → runtime
  0.923 (−13.6%), mem 26653 (−3.4 MB, smaller heap), loc 37. **All 3 improved → new best.**
  This was the key algorithmic insight: reducing heap traffic helps both time and memory.

- **Run 4 — CSR layout via `array`.** ~26 MB pointed at the adjacency list of `(v, w)`
  tuples (~64 B per directed edge). Rebuilt as compressed-sparse-row: a `head[]` offset
  list plus flat `array('i')` neighbour and `array('q')` weight arrays (~12 B/edge).
  runtime 0.822 (−11%), mem **8886** (−18 MB), loc 52 (regressed). 2 of 3 → **new best.**
  Surprise: CSR was *faster* too (cache locality, no per-edge tuple object churn), not just
  smaller.

- **Run 5 — int32 weights + trim.** Stored weights as `array('i')` (4 B) instead of `'q'`
  (8 B) and trimmed the docstring/assignments. mem 7641 (−1.2 MB), loc 44; runtime tie.
  2 of 3 → **new best.** Weights fit int32 (no overflow); distances still accumulate in
  Python ints so no sum overflow risk.

- **Run 6 — packed-int heap.** Replaced heap 2-tuples with a single packed key
  `d * n + node` (decode by `divmod`). mem 5355 (−2.3 MB) but loc +2 and runtime tie →
  only 1 metric → **kept best.** Confirmed the heap's tuples were a real memory consumer.

- **Run 7 — packed heap, done right.** Same packing but with `divmod()` and an inlined
  relax check to claw back lines. mem 5355, loc 43, runtime tie → mem+loc → **new best.**

- **Run 8 — flat `array('q')` dist + `accumulate` build.** Replaced the Python `dist` list
  (a 28-byte int object per settled node) with a flat `array('q')` using a `-1` sentinel,
  and built CSR offsets with `itertools.accumulate`. runtime **0.712** (−15.3%), loc 42;
  mem tie. 2 of 3 → **new best, and the final answer.** Biggest surprise of the run: the
  flat dist array sped the search up sharply — integer `< 0` checks and contiguous access
  beat Python-list `is None` lookups.

## What didn't pan out / boundaries found

- **Run 9 — tuple heap + array dist (control).** Tested whether the packed-int encoding's
  `divmod`/multiply costs anything. runtime 0.717 (tie with 0.712) but mem +2.3 MB. So
  packing is **free memory savings** — the runtime win came entirely from the `array` dist,
  not the heap format. Kept best.
- Memory bottomed out at **5355 kb** across runs 6–8: that's the floor set by the input
  `edges` plus the two CSR arrays, which I can't shrink further without losing information.
- Runtime plateaued near **0.71 s**; beating it >10% would need an algorithmic change
  (e.g. bidirectional Dijkstra), which costs a second heap + dist array (memory regression)
  and real correctness risk — not worth it for no net promotion.
- I deliberately left run 10 unused: no 2-of-3 improvement was reachable, a re-grade of the
  best just reproduces stable median numbers, and a non-OOP variant — even if marginally
  smaller — would betray the style this agent is meant to represent.

## Why `best.py` is the final answer

It is the metric-optimal point reached under the promotion rule: **0.712 s, 5355 kb,
42 loc**, correct 13/13. It keeps an honest OOP shape — a single `Graph` class that
encapsulates construction (self-loop filtering, CSR packing) and the `shortest_path`
query — while every line in the hot path earns its place:
- **CSR via `array`** for compact, cache-friendly adjacency;
- **tentative-distance Dijkstra** to minimise heap traffic;
- **flat `array('q')` dist** with a `-1` sentinel for fast, allocation-free relaxation;
- **packed-int heap keys** to drop tuple overhead at no runtime cost.

## Key patterns for distillation

1. **Pick the algorithm from the problem's structure first** (non-negative weights →
   heap Dijkstra); don't pre-process what the algorithm handles for free (multi-edges).
2. **Profile by reasoning about the dominant cost, then attack it directly.** Each promoted
   run targeted one specific consumer (push count, tuple overhead, int-object boxing).
3. **In CPython, flat `array`/CSR storage beats lists-of-tuples on *both* memory and
   runtime** for large graphs — object overhead and pointer chasing dominate.
4. **Reducing heap traffic (tentative relaxation) is the single highest-leverage change**
   for Dijkstra — it improves time and memory together.
5. **Validate each change against the grader, keep only on real improvement**, and use
   control experiments (run 9) to attribute *which* change produced a win.
6. OOP and performance aren't in tension here: the class boundary cost is negligible once
   attributes are hoisted to locals in the hot loop.
