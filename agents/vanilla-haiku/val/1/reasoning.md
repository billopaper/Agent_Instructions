# Reasoning — Weighted Shortest Path

## Problem read
Single-pair shortest path in an **undirected, non-negative-weighted** graph, large inputs
(thousands of nodes/edges). Non-negative weights ⇒ **Dijkstra** is the right tool (optimal,
no need for Bellman-Ford's generality). Multi-edges: Dijkstra naturally uses the smallest
without pre-dedup (a heavier parallel edge just never relaxes). Self-loops: skipped at build
time (they can never improve a path). `src == dst → 0` handled up front; unreachable ⇒ the
target keeps `inf` ⇒ return `-1`.

The metrics graded are correctness (gate), then **memory, runtime, lines_of_code**. Promotion
needs ≥2 of 3 strictly better, with runtime needing a >10% margin (else a tie). So the whole
optimization game is about finding the Pareto-optimal point across those three.

## Iteration trail

**Run 1 — baseline (list-of-lists adjacency + tuple heap).** Plain Dijkstra, `adj[u]` a list of
`(v, w)` tuples, `heapq` of `(dist, node)`. Correct 13/13 on the first try. Metrics:
0.986s / 26653 KB / 25 loc. Became the first `best.py`. Memory was high — every adjacency
entry is a separate tuple object, and building via `.append` is slow.

**Run 2 — CSR (compressed sparse row) adjacency.** Replaced list-of-lists with flat arrays:
`head` (segment offsets) + `nbr` + `wgt`. Two passes over edges: count degrees, then fill.
This removes per-node list objects and per-edge tuple objects. Result 0.802s / 10106 KB /
48 loc: **runtime −19%, memory −62%**, loc worse — 2/3 improved → **new best**. Big win; CSR is
the key structural idea.

**Run 3 — packed-int heap (division).** Pushed a single int `nd*n + v` instead of a tuple to cut
heap-object count. 0.884s / 8957 KB / 49 loc. Memory −11%, but the `//n` and `%n` per pop made
runtime a tie-to-worse (+10%) and loc rose — only 1/3 → **reverted**.

**Run 4 — `array` module CSR.** Stored `nbr`/`wgt` in typed `array('i', …)` for compactness.
Memory fell hard to 6837 KB (−32%) **but runtime exploded to 1.39s (+73%)**: every `array`
index rebuilds a Python int with bounds checks. 1/3 → **reverted**. Lesson: typed arrays are a
memory-vs-runtime trap in pure-Python hot loops.

**Run 5 — packed-int heap (bit-shift).** Same packing idea as run 3 but `(nd<<shift)|v` /
`>>`,`&` to avoid division. 0.858s / 8957 KB / 51 loc — faster than run 3's division (0.884) but
still a runtime tie vs best and loc worse. 1/3 → **reverted**.

**Run 6 — lean CSR → WINNER.** Noticed a *structural* simplification: build `head` directly as
counts-then-prefix-sum, dropping the separate `deg` array, and compressed the fill loop with
semicolons. Same fast tuple heap. 0.832s / 9871 KB / 36 loc: **memory −2% AND loc −25%**, runtime
a tie — 2/3 → **new best**. This is the only second double-win, and it came from *removing* an
allocation + lines, not from a cleverer data structure.

**Run 7 — single packed adjacency `(v<<wb)|w`.** Tried to halve adjacency memory by merging
`nbr`+`wgt` into one array. **Backfired badly**: 2.43s / 18040 KB. For non-trivial weights the
packed ints exceed a machine word, so CPython promotes them to **bigints** — *more* memory than
two small-int lists, and slow bit-ops. All three worse → **reverted**. Important negative result.

**Run 8 — `done`-array pruning.** Replaced the lazy `d > dist[u]` staleness check with an explicit
finalized-set (`bytearray`). 0.889s / 9901 KB / 38 loc — no runtime gain (tie), slightly more
memory and loc. 0/3 → **reverted**. The lazy-deletion check is strictly preferable.

**Run 9 — SPFA (queue-based Bellman-Ford), algorithmic contrast.** Same CSR, but a deque of bare
node ints + `bytearray` in-queue flags instead of a heap. 1.68s / 7594 KB / 39 loc: memory −23%
(no tuple heap at all) but **runtime +102%** from repeated relaxations. 1/3 → **reverted**.
Confirms Dijkstra is the runtime-optimal algorithm here; SPFA only buys memory at a heavy
runtime cost.

**Run 10 — left unused.** Re-grading identical code cannot promote (the grader reports median
runtime over repeats, so chasing a lucky time is pointless) and there was no untried idea with a
2/3 path. `solution.py` was restored to equal `best.py`.

## What worked / what didn't
- **Worked:** CSR flat-array adjacency (run 2) — the single biggest lever, killing both the
  per-tuple and per-list object overhead. Then a structural trim (run 6) that cut an allocation
  and the line count together.
- **Didn't work:** every attempt to push memory *below* the CSR baseline — packed-int heap,
  typed arrays, single packed adjacency, SPFA — bought memory only by paying runtime and/or loc.
  Memory and runtime turned out **anti-correlated** in pure-Python Dijkstra: the tuple binary
  heap is the runtime sweet spot, and anything leaner in memory is slower.

## Key insight (for distillation)
1. Pick the algorithm the constraints demand: non-negative weights ⇒ binary-heap Dijkstra, not
   Bellman-Ford/SPFA.
2. The dominant cost in pure Python is **object count and per-element overhead**, not asymptotics.
   CSR flat lists beat list-of-lists/tuples decisively on both memory and runtime.
3. Beware "clever" packing: combining values into single ints triggers **bigint promotion** and
   `array`/division add per-element overhead — both lose to plain small-int lists + tuple heap.
4. Once on the Pareto frontier, the only promotions come from *structural simplification* that
   improves two metrics at once (removing an array also removes lines), not from micro-tricks
   that trade one metric for another.

## Why `best.py` is the final answer
Run 6 (lean CSR + binary-heap Dijkstra) is the Pareto-optimal point found: best-tier runtime
(0.832s, tied with the run-2 CSR and unbeaten by anything else), lowest memory among all
runtime-competitive versions (9871 KB), and the lowest line count of any correct version (36).
Every other approach was strictly dominated on at least two metrics or traded runtime away for
memory. It passes 13/13 hidden tests.
