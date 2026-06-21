# Reasoning trail — Weighted Shortest Path (smart-pattern agent)

## The problem in one line
Single-source single-target shortest path on an **undirected, non-negative-weight**
graph, large inputs. That is textbook **Dijkstra with a binary heap** — `O(E log V)`,
optimal asymptotics. Multi-edges and self-loops need no special handling: Dijkstra's
relaxation keeps the minimum automatically, and self-loops (`u==v`) can be dropped on
read. So correctness was never in doubt; the whole game was the metric optimization
under the **2-of-3 promotion rule** (promote only if ≥2 of {memory↓, runtime>10%↓,
loc↓}).

## Initial approach (run 1) — and why
Plain Dijkstra: list-of-lists adjacency of `(w, v)` tuples, lazy-deletion binary heap,
`dist` with a sentinel. First try: **correct, 13/13**, runtime 0.973s, mem 26651 kb,
loc 25. This became `best.py`. The early `if u == dst: return d` short-circuits once
the target is settled.

## The optimization arc — the key tension
I quickly discovered a hard trade-off that shaped everything:

- **Speed wants tuples.** Iterating a Python `list` of `(w, v)` tuples
  (`for w, v in adj[u]`) is C-level fast. This is the runtime champion (~0.95–0.97s).
- **Memory wants flat arrays.** A list-of-lists-of-tuples is the dominant memory
  consumer on large graphs. A **CSR** layout (`array('i')` for neighbours + weights +
  head offsets) is far lighter — but its hot loop (range+index or `zip` of array
  slices) is markedly slower (~1.3s).

So no single representation wins both axes. Given the metric ordering in the experiment
(**memory is the first-ranked metric after correctness**), I deliberately pursued the
memory-optimal CSR and paid for the second promotion metric with **loc** instead of
runtime.

### What each run taught me
- **run 2** — CSR keeping an intermediate filtered-edge list: mem 18633 (−30%) but
  runtime +34%, loc 42. Only 1/3 → reverted. *Insight: arrays cut memory a lot.*
- **run 3** — micro-opt of the tuple version (localized `heappush`/`heappop`, `INF`
  sentinel): runtime 0.952 — a **tie** (within ±10%), nothing else moved. 0/3.
  *Insight: constant-factor micro-opts don't clear the 10% runtime bar; the algorithm
  is already the right one.*
- **run 4** — packed-int heap (`nd*n + v` instead of `(nd, v)` tuples) on the tuple
  version: mem −1.1 MB but loc +3. 1/3. *Insight: packing the heap removes tuple
  allocations — a real memory lever.*
- **run 5** — CSR with **two passes over `edges`, no intermediate list**: mem
  **6710 (−75%!)**, but runtime +37%, loc 36. 1/3. *Insight: the intermediate edge
  list in run 2 was itself a big consumer; dropping it is the giant memory win.*
- **run 6** — same CSR, **densely compressed** (semicolons, no throwaway names):
  mem 6710 **and** loc 22<25 → **2/3, PROMOTED.** *Insight: pairing the memory win with
  a loc win (dense code, which the smart-pattern style welcomes) is how you satisfy the
  rule when runtime must be sacrificed.*
- **run 7** — `.tolist()` on slices + loc 20: only loc improved (runtime unchanged →
  the **build passes, not the hot loop, dominate runtime**). 1/3, kept.
- **run 8** — CSR + **packed-int heap** + loc 20: mem **4424<6710 and loc 20<22** →
  **2/3, PROMOTED.** Packing saved another ~2.3 MB. This is the final answer.
- **run 9** — `import heapq, array` one-liner (loc 19) + `array('q')` dist: only loc
  improved; the `b'\xff'*(8*n)` initializer caused a transient bytes **spike that
  nudged peak up to 4439**, and attribute-qualified `heapq.` calls slowed the loop.
  1/3, kept. *Insight: a compact dist array can backfire via its own construction
  spike; the plain `[INF]*n` list (shared float, just pointers) was actually leaner.*
- **run 10** — restored best, final confirm: 13/13, mem 4424, loc 20.

## Why `best.py` is the final answer
It is the **memory-optimal** correct solution: 4424 kb is an **83% reduction** from the
naive 26651 kb, while staying terse (loc 20). It got there through two composable
smart patterns:
1. **CSR adjacency in `array('i')`** built in two passes over `edges` with no
   intermediate object — removes the list-of-tuples memory blow-up.
2. **Packed-integer heap** (`nd*n + v`, decoded with `divmod`) — removes per-entry
   tuple allocation in the priority queue.

The cost is runtime (~1.35s vs ~0.97s for the tuple version). I accepted this because
(a) memory is the priority metric, and (b) under the 2-of-3 rule the CSR version is
**stable**: once it also reached loc 20, the fast tuple version can no longer dethrone
it (tuple would need to beat loc *and* runtime, but it can't beat loc, and its memory is
far worse). The rule with equal-weighted metrics can ratchet in conflicting directions;
I anchored on memory deliberately rather than letting it oscillate.

## What worked / what didn't
- **Worked:** recognizing the problem as vanilla Dijkstra (instant correctness);
  CSR + packed heap for memory; dense formatting to harvest the loc metric; using the
  "no intermediate edge list" two-pass build (the single biggest memory drop).
- **Didn't:** runtime micro-optimizations (never cleared 10%); `.tolist()` on the hot
  loop (build-bound, not loop-bound); `array('q')` for dist (construction spike made it
  worse). 
- **Key pattern converged on:** when correctness is trivial and metrics are the contest,
  identify the dominant resource consumer (here, the adjacency representation), attack it
  with the right data structure (CSR + int-packed heap), and pick the *second*
  promotable metric (loc, via dense code) that doesn't fight the first — rather than
  chasing the metric (runtime) that's in tension with your primary win.
