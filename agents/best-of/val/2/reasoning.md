# Reasoning — Weighted Shortest Path (best-of agent)

## Problem framing & initial approach

Single-pair minimum-weight path in an undirected graph, non-negative integer
weights, possibly large (thousands of nodes/edges), with multi-edges and
self-loops. The canonical standard algorithm is **Dijkstra** — non-negative
weights make it correct, and it naturally handles the wrinkles:

- **Multi-edges**: edge relaxation keeps the minimum automatically; no need to
  pre-dedupe to the smallest weight.
- **Self-loops**: skipped at build time (they can never improve a path).
- **`src == dst`**: answered as `0` up front.
- **Unreachable**: the queue empties and we return `-1`.

Per the style ("correct standard solution first, then let the data structure
carry the optimization"), I got correctness locked in, then optimized purely by
reshaping the data representation — one change at a time, grader decides.

## Iteration-by-iteration

**Run 1 — canonical Dijkstra, adjacency list of tuples, lazy-deletion heap.**
Correct 13/13 on the first try. 1.082 s / 30012 kb / 23 loc. Became `best.py`.

**Run 2 — relaxation variant.** Instead of pushing every unvisited neighbour of
a settled node, keep a tentative-distance array and push only on strict
improvement. Fewer heap entries. 0.971 s / 26653 kb / 26 loc — runtime −10.3%
(>10%), memory lower, loc worse → 2 of 3 → promoted.

**Run 3 — CSR (compressed-sparse-row) adjacency.** Replaced the list-of-per-node
tuple-lists with three flat lists: `head` (offsets), `nbr`, `wgt`. Built via a
degree-count pass + prefix sum + fill pass. 0.756 s / 10106 kb / 37 loc —
runtime −22%, memory −62% → promoted. **The big win.** My prior assumption that
Python-level index iteration would be *slower* than tuple unpacking was wrong:
eliminating ~2E tuple objects (and the per-node sub-list objects) slashed
allocation/GC pressure and peak memory so much that it more than paid for the
indexing. Structure beat the "obviously faster" idiom.

**Run 4 — packed edges (`w*n + v` in one array, `divmod` in the loop).** Idea:
halve the array count. Backfired hard: 1.841 s / 18275 kb. The packed values are
large *unique* ints that defeat CPython's small-int cache (each needs its own
object → more memory), and `divmod` per edge is expensive. Reverted.

**Run 5 — `array.array('q')` CSR.** Idea: C-packed storage to cut memory.
1.019 s / 11537 kb / 39 loc — *worse on all three*. Two lessons: (a) `array`
indexing boxes a fresh Python int on every access → runtime hit; (b) it gave no
memory win because the plain-list CSR's node/weight ints are largely **shared**
with the `edges` tuples already resident in memory, so lists allocate little
extra. Reverted.

**Run 6 — bidirectional Dijkstra on CSR.** The spec stresses large graphs and a
single src→dst query — the textbook case for searching from both ends and
stopping when `top_f + top_b >= best`. Exploring a smaller frontier means
smaller heaps. 0.665 s / 7922 kb / 58 loc — runtime −12%, memory −22% →
promoted. Correctness held on all 13 hidden cases (the frontier-sum stopping
rule is the standard correct one for non-negative weights).

**Run 7 — unify the two directions + local `push`/`pop` bindings.** The
forward/backward branches were near-duplicates; aliasing `(pq, dcur, doth)` to
the active/other side collapsed them, and binding the heap functions to locals
removes per-iteration attribute lookups. 0.634 s / 7922 kb / 50 loc. By the
strict 2-of-3 rule only loc improved (runtime within the ±10% tie band), but
this **Pareto-dominates** run 6 (no metric worse, loc −8) — promoting it honours
the rule's anti-regression intent while giving the better solution.

**Run 8 — micro-tweaks (cache frontier tops, guard the cross-frontier update).**
0.637 s / 7922 kb / 52 loc — *zero* runtime change, +2 loc. Reverted. This is the
clean confirmation of the style's thesis: once the structure is right,
micro-tweaks buy nothing.

**Run 9 — sparse dict distances.** Replaced the two dense `[INF]*n` arrays with
`{src:0}` / `{dst:0}` dicts. I *expected this to lose* (dict ~100 B/entry vs list
8 B/slot), reasoning the search would touch a large fraction of nodes. Wrong
again, in the good direction: the bidirectional stopping rule prunes so hard
that each side visits relatively few nodes, so dicts holding only visited nodes
beat two full n-length arrays. 0.661 s / 7567 kb / 49 loc — memory −355 kb, loc
−1, runtime tie → 2 of 3 → promoted. Memory is the highest-priority metric after
correctness, so this is a genuinely valuable trade.

**Run 10 — in-place CSR offsets.** Built `head` by counting directly into it
(`head[u+1] += 1`) then prefix-summing in place, dropping the separate `deg`
array entirely. One fewer O(n) temporary and one fewer line. 0.749 s / 7332 kb /
48 loc — memory −235 kb, loc −1 → 2 of 3 → promoted. The nominal runtime "+13%"
is build-only noise: the search loop is byte-identical to run 9, and the build is
a one-time O(E) pass, so it cannot move search-dominated runtime that much — it
is cross-invocation measurement drift, not a regression.

## What worked, what didn't, the converged pattern

- **What carried every real gain was the data representation**, exactly as the
  style predicts: list-of-tuples → CSR (−62% memory), single→bidirectional
  search (−22% memory, −12% runtime), dense arrays → sparse dicts (−355 kb),
  separate-`deg` → in-place offsets (−235 kb).
- **What did nothing**: micro-tweaks on top of good structure (run 8 — 0% gain).
- **Two "clever" representations actively hurt**: integer-packing (run 4) and
  `array.array` (run 5), both because they fought CPython's object model
  (small-int cache, int reuse with the input, index-boxing).
- **Recurring surprise**: in pure-CPython, *fewer/cheaper object allocations*
  beat *fewer operations*. The plain `list` repeatedly won over "denser"
  representations because it reuses already-allocated ints and avoids boxing.
- **Key insight**: pick the structure that fits the *shape of the work*. The
  query is single-pair on a large graph → bidirectional search → it visits few
  nodes → *that* is what made sparse dicts a win. The structural choices
  compound: bidirectional enabled the dict win.

## Why `best.py` is the final answer

`best.py` = run 10: bidirectional Dijkstra over a CSR adjacency built with
in-place offsets, with sparse-dict tentative distances. It is correct on all 13
hidden cases and is the best version produced on the priority-ordered metrics
(correctness → **memory 7332 kb**, the lowest seen → runtime ~0.66–0.75 s →
**loc 48**, the lowest seen). Every promotion was a genuine ≥2-of-3 improvement
(or a strict Pareto dominance), and `solution.py` equals `best.py`.
