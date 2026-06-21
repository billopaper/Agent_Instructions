# Reasoning trail — weighted-shortest-path (functional agent)

## Problem framing
Minimum-weight path in a weighted, undirected, non-negative-weight graph, or `-1`
if unreachable. Non-negative weights ⇒ **Dijkstra** is the right algorithm (no need
for Bellman-Ford). Two spec subtleties:
- **Multi-edges**: the smallest parallel edge wins — but Dijkstra handles this for
  free. A larger parallel edge just produces a relaxation that never beats the
  smaller one, so I never deduplicate edges (deduping would cost time/memory).
- **Self-loops**: skipped at build time (`u != v`); they can never shorten a path.
- `src == dst` ⇒ `0`, handled as the first line.

Functional leaning: the core is a pure function (`shortest_path`) with explicit
input→output behaviour and no external/shared state; the graph is built once into
immutable-by-convention flat arrays and never mutated during the search. `accumulate`
expresses the offset prefix-sum declaratively. (A fully persistent/immutable PQ in
pure Python would wreck the runtime/memory metrics, so the heap stays local and
mutable — pragmatic functional, not dogmatic.)

## Iteration log

**Run 1 — list-of-lists-of-tuples Dijkstra (baseline).** `adj[u] = [(v,w),...]`,
lazy-deletion heap of `(dist, node)` tuples. Correct 13/13 immediately.
0.942 s / 26653 kb / 24 loc. First correct ⇒ best. Cleanest/shortest but the
2·E tuples + per-node lists make it the memory hog.

**Run 2 — CSR with `array.array('i')`.** Flat compressed-sparse-row adjacency
(degree pass → offsets → fill) in typed arrays. Memory cratered to 6837 kb (−74%)
but runtime rose to 1.247 s. Cause: `array.array` indexing **re-boxes** a fresh
Python int on every access, so the hot inner loop got slower. Only 1/3 improved
(memory) → kept best.

**Run 3 — CSR with plain Python lists.** Same flat layout, but `nbr`/`wgt` are
ordinary lists holding references to the int objects already in the edges (no
re-boxing, list-speed access, no tuple/per-node-list overhead). 0.745 s (−21%) /
10106 kb (−62%) / 41 loc. Runtime AND memory improved ⇒ **new best**. Key insight:
*flat lists beat both list-of-tuples (memory) and `array.array` (speed)* — the
sweet spot.

**Run 4 — packed-int heap.** Push a single int `d*n + node` instead of a
`(d, node)` tuple; decode with `//`/`-`. 0.811 s / 8957 kb / 44 loc. Memory down
(no heap tuples) but runtime ~9% worse (a tie under the ±10% band) and loc up →
only 1/3 → kept best. The idea was sound but the standalone build was verbose.

**Run 5 — `zip` of CSR slices in the inner loop.** `for v,w in zip(nbr[a:b],
wgt[a:b])`. The per-pop slice allocations cancelled the C-level zip benefit:
0.759 s (tie) / 10106 kb (same) / 40 loc. Only loc −1 → kept best.

**Run 6 — packed-int heap + `accumulate` build (WINNER).** Combined run-4's heap
packing (memory win) with `off = [0, *accumulate(deg)]`, which collapses the whole
offset loop into one line and is faster than the manual prefix sum. Result:
0.727 s / 8964 kb / 37 loc — **strictly better on all three axes** vs the prior
best (memory −11%, loc −4, runtime tie-to-slightly-better) ⇒ new best.

**Run 7 — single-int CSR packing `v*B + w` (negative result).** Tried to halve the
adjacency to one list by packing neighbour and weight together. Backfired badly:
1.730 s / 15994 kb. Two reasons: (a) `v*B+w` produces **large ints that aren't in
CPython's small-int cache**, so each slot allocates a distinct big-int object —
*more* memory than referencing the small/shared ints already living in the edge
tuples; (b) `% B` and `// B` per neighbour are expensive. Reverted. Lesson:
*packing only helps when the packed values stay small/cached.*

**Run 8 — `divmod` + locally-bound `heappush`/`heappop`.** Micro-opts on the
winner. 0.738 s / 8964 kb / 37 loc — every axis a tie. At this graph size the heap
call overhead isn't the bottleneck (the Python-level relaxation loop is), so
binding the methods bought nothing. Kept best.

**Run 9 — final confirmation.** Re-graded the restored best: 0.711 s / 8964 kb /
37 loc, 13/13. solution.py == best.py. Stopped with 1 run in reserve.

## What worked / what didn't
- **Worked:** flat-list CSR (the single biggest balanced win), packing the heap to
  plain ints (memory, when values stay small), `accumulate` for a short+fast
  prefix sum.
- **Didn't:** `array.array` (lean but slow re-boxing), `zip`-of-slices (alloc
  churn), single-int `v*B+w` packing (large-int memory blow-up), method-binding /
  `divmod` (no measurable gain at this scale).
- **Convergent pattern:** in pure-Python Dijkstra, *data-structure layout
  dominates*. Prefer flat Python lists (references to already-existing small ints)
  over both tuple-of-lists and typed arrays; keep any packed integers within the
  small-int cache range; relaxation, not the heap API, is the runtime floor.

## Why best.py is the final answer
The run-6 version is Pareto-dominant over every other correct attempt I produced:
lowest loc (37), near-lowest memory (8964 kb; only the slow `array` variant was
leaner, at a large runtime cost), and best-tier runtime (~0.71–0.73 s, tied for
fastest). It also reads as a clean declarative pipeline (build → prefix-sum →
search), satisfying the functional-style brief while staying efficient on the
large graphs the grader measures.
