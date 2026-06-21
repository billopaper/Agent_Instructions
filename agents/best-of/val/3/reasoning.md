# Reasoning — Weighted Shortest Path (best-of agent)

## Problem framing
Minimum-weight path in an undirected, non-negative-weight graph, or `-1` if unreachable.
The canonical algorithm is **Dijkstra with a binary heap** — non-negative weights, single
source/target, large inputs (thousands of nodes/edges). Multi-edges and self-loops are handled
*for free* by Dijkstra: relaxation keeps the smallest tentative distance, so a heavier parallel
edge is simply never accepted, and a self-loop (`d + w >= d`) is never an improvement. Edge cases
called out by the spec — `src == dst → 0`, unreachable → `-1`, single-node / edge-less graphs —
fall straight out of the standard formulation.

Fit-for-purpose plan: get the canonical Dijkstra correct first, then optimize by **reshaping the
data representation** (the lever that actually moves memory/runtime), changing one thing per run
and letting the grader decide.

## Iteration trail

- **Run 1 — canonical heapq Dijkstra, adjacency list of `(v,w)` tuples.**
  Correct, 13/13. `1.002s / 26653 KB / 25 loc`. First correct → `best.py`. Baseline established.
  Edge cases handled with no special-casing beyond skipping self-loops at build time.

- **Run 2 — reshape to CSR (compressed sparse row).** Replaced the per-node list-of-tuples with
  three flat arrays: `start` (prefix-sum offsets), `to`, `wt`. This removes one Python list object
  per node and one tuple object per directed edge.
  Result `0.827s / 10106 KB / 45 loc`: runtime −17%, **memory −62%**, loc worse. 2/3 → **promoted**.
  This was the decisive win and confirms the style's premise: the structure, not the lines, carried it.

- **Run 3 — back CSR with the typed `array` module.** Hypothesis: raw machine ints beat boxed ints.
  Result `1.664s / 9590 KB / 50 loc`: memory only −5% (CPython already *shares* the existing int
  objects from the edge tuples, so the list-of-pointers version stored almost no new int objects),
  while runtime **doubled** from per-read boxing on every `array` access. 1/3 → **reverted**.
  Insight: `array` helps only when you also compute in C; in a pure-Python hot loop it's a net loss.

- **Run 4 — pack the heap entry into a single int `d*n + v`.** The heap held 2-tuples (heavyweight:
  a tuple object plus tuple comparison per push/pop). Packing makes each entry one plain int.
  Result `0.900s / 8957 KB / 50 loc`: **memory −11%** (no tuple objects), runtime a tie, loc worse.
  Only 1/3 → reverted *as written* — but the memory win was real and worth keeping if I could also
  fix loc and recover the runtime.

- **Run 5 — packed heap, written concisely, decode via `divmod`.** Kept the run-4 packing, decoded
  with `d, u = divmod(pop(pq), n)` (one C call instead of separate `%` and `//`), and tightened the
  source. Result `0.814s / 8957 KB / 35 loc`: runtime tie (even a hair faster — `divmod` paid back
  run 4's decode cost), **memory −11%**, **loc −22%**. 2/3 → **promoted. This is the final answer.**

- **Run 6 — `zip(to[s:e], wt[s:e])` inner loop.** Hoped C-level iteration would beat `range`+index.
  `0.841s / 8958 KB / 36 loc`: slice allocation per visited node offset the gain. 0/3 → reverted.

- **Run 7 — explicit parallel-edge dedup via a dict (`min` weight per pair).** Hypothesis: if the
  hidden graphs are heavy multigraphs, shrinking the edge set helps both metrics.
  `2.387s / 28052 KB / 45 loc`: ~3× worse on both — the dict build dominates and the test graphs
  don't have enough duplicates to repay it. 0/3 → reverted. Confirms Dijkstra already absorbs
  multi-edges more cheaply than any explicit pre-pass.

- **Run 8 — settled `bytearray` instead of the `d > dist[u]` stale check.** `0.828s / 8986 KB / 37 loc`:
  the byte check is no cheaper than the float compare and adds `n` bytes + 2 loc. 0/3 → reverted.

## What worked / what didn't
- **Worked:** choosing the *data representation* — CSR (run 2) crushed memory; packing the heap key
  (runs 4–5) shaved another 11% and, written concisely with `divmod`, also won loc with no runtime cost.
- **Didn't:** every micro/structural tweak that fought CPython's grain — typed arrays (boxing),
  zip-slices (alloc), edge dedup (dict overhead), settled array (no cheaper, extra memory).
- **Key insight:** in pure-Python Dijkstra the cost and the memory live in *object count and object
  weight*, not in line-level cleverness. CSR removes per-node/per-edge objects; an int heap key
  removes per-entry tuple objects. Reusing existing int objects (lists of pointers) actually beats
  `array` here. The algorithm itself already handles multi-edges/self-loops, so don't pay to dedup them.

## Why `best.py` (run 5) is the final answer
It is the canonical, fully-correct Dijkstra (13/13 across all spec categories) on the representation
that fits the problem best: CSR adjacency + a single-int packed heap. It is the **Pareto-best**
solution seen — lowest memory (8957 KB), lowest loc (35), and runtime tied with the fastest variant
(0.814s, within the grader's 10% tolerance of every faster reading). Runs 9–10 were left unused: the
remaining ideas are micro-variations the fit-for-purpose style explicitly avoids, and all measured as
ties or regressions, so the promotion rule could only ever revert them. `solution.py` is identical to
`best.py`.
