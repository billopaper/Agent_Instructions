# Reasoning — weighted-shortest-path (smart-pattern agent)

## Problem framing & initial approach

The task is single-pair shortest path in an **undirected graph with non-negative
integer weights**. That immediately fixes the canonical pattern: **Dijkstra with a
binary heap** (`heapq`), O(E log V). Non-negativity rules out Bellman-Ford as the
right tool; the single-pair (not all-pairs) shape and "inputs may be large" hint
that the *constant factors and the search frontier size* are where metrics are won.

Three spec subtleties, all handled structurally rather than by special-casing:
- **Multi-edges (min wins):** lazy Dijkstra handles this for free — the shorter
  parallel edge simply relaxes first; no dedup needed.
- **Self-loops:** provably harmless. A loop `(u,u,w)` can only ever offer
  `dist[u]+w >= dist[u]`, which never relaxes. So the `if u != v` filter is
  optional (confirmed in run 4).
- **`src == dst` → 0, unreachable → -1:** both fall out of a clean Dijkstra
  (`dist[src]=0`; unreached stays `inf` → `-1`).

## Iteration log (what I tried, why, what happened)

1. **Lazy Dijkstra, list-of-tuples adjacency** (24 loc). Correct first try, 13/13.
   Baseline: runtime 1.003 s, mem 26653 KB. → first `best`.
2. **Int-packed heap** (`key = d*n + node` instead of `(d,node)` tuples). Hypothesis:
   smaller heap entries + faster int comparison. Result: mem −4%, runtime tie (−2.6%),
   loc worse. Only 1/3 → kept best. **Insight: the heap-entry representation is *not*
   the bottleneck** — the cost is the sheer number of Python-level relaxations.
3. **CSR adjacency with `array` module** (two arrays: `to` int32, `wt` int64).
   Hypothesis: tuples dominate memory. Result: **mem −71% (7771 KB)**, runtime tie,
   loc 41. Confirmed the list-of-tuples was the memory hog — but only 1/3 (memory),
   so no promotion. **Key tradeoff discovered: compact array storage ⇒ slower
   per-edge iteration** (range + double index vs C-level tuple unpacking).
4. **Lean build** (drop `u!=v` and the redundant `src==dst` guard). loc 21,
   runtime −6% (tie), mem tie. 1/3 → kept best. Cheap and clean but not promotable.
5. **Single packed array** (`w*n+node` in one `array('q')`). New **memory floor
   6526 KB**, but the per-edge decode (`e%n`, `e//n`) cost **+47% runtime**. The
   memory-vs-runtime tradeoff in its starkest form. 1/3.
6. **Lean build + aliased `push`/`pop`** (tuple heap). Runtime **0.923 s — but only
   −8% vs baseline, just inside the ±10% tie band**. loc 23. 1/3 (loc). The runtime
   floor for list-based unidirectional Dijkstra here is ~0.92, and noise
   (`rel_spread` ~0.04–0.14) makes sub-10% gains uncountable by design.
7. **No early-exit** (full SSSP, return `dist[dst]`). Runtime jumped to 1.089
   (+18% vs run 6). **Proves the `if u==dst: return d` early-exit is worth ~15%** on
   the hidden large graphs — dst is reached well before the component is exhausted.
8. **Bidirectional Dijkstra (strict alternation).** The real "smart pattern" for
   *single-pair* search: grow frontiers from both `src` and `dst`, meet in the
   middle (edge-relaxation `mu` update, terminate on `topf+topb >= mu`). Searching
   from both ends explores far fewer nodes → **runtime 0.857 (−14.6%, clears 10%)
   AND mem 24477 (< 26653)**. **2/3 → first genuine promotion.** This is the headline
   insight: the data structure wasn't the lever; *the search strategy* was.
9. **Bidirectional, smaller-frontier strategy** (always expand the side with the
   smaller top key — the textbook-"better" variant; also collapses the two symmetric
   blocks into one → loc 31). Surprise **negative result: runtime 0.985 (+15% vs
   run 8)** — the per-iteration branch + 3-tuple alias rebind cost more than strict
   alternation saved on this workload. But mem 24470 (< 24477) and loc 31 (< 40) →
   **2/3 → promoted** (memory is the primary metric; rule has no anti-regression
   guard on the third).
10. **Bidirectional + CSR** (fuse run 8's search with run 3's storage). **mem 7381
    (−70%) AND runtime 0.927 (−6% vs run 9, and faster than the slow run-9 best)**,
    loc 43. But −6% runtime is inside the ±10% tie band, and loc regressed →
    only 1/3 strictly improved → **not promoted**.

## What worked, what didn't, the converged insight

- **Worked:** Bidirectional Dijkstra was the decisive idea — the only change that
  improved *two* metrics at once (runtime + memory together, run 8) by shrinking the
  explored frontier rather than fiddling with constants.
- **Didn't move the needle:** int-packing the heap (run 2), the "smarter"
  smaller-frontier rule (run 9, slower here than plain alternation).
- **The fundamental Pareto wall:** in pure Python, *fast iteration* (list-of-tuples,
  C-level unpacking) and *low memory* (CSR `array`) are mutually exclusive — memory
  trades against both runtime and loc. No single representation gets two of
  {low-mem, low-runtime, low-loc} beyond what bidirectional search buys you.
- **Early termination matters** (~15%, run 7) and **the heap representation does
  not** (run 2) — both non-obvious without measuring.

## Why `best.py` is the final answer (and an honest caveat)

`best.py` = **run 9 (smaller-frontier bidirectional Dijkstra)**, because it is the
last solution the 2/3 promotion rule accepted (memory 24470 + loc 31 both strictly
better than the prior best).

**Honest caveat for winner selection / distillation:** run 9 is *not* the solution I
would ship. **Run 10 (bidirectional + CSR) dominates it on the two highest-priority
metrics** — memory 7381 vs 24470 KB (−70%, and memory is the experiment's primary
metric after correctness) and runtime 0.927 vs 0.985 s (−6%) — losing only on LOC
(43 vs 31). The mechanical 2/3 promotion rule blocked run 10 for two structural
reasons worth feeding back into the master prompt:
1. the runtime tolerance (±10%) reclassified a *real* 6% gain as a "tie," and
2. LOC is weighted equally with memory, so a small loc regression can veto a
   massive primary-metric win.

If the final scoring is memory-weighted (as the metric ordering memory > runtime >
loc suggests), **run 10 is the better answer** and should be preferred manually.
I kept `best.py` = run 9 to stay faithful to the stated promotion rule rather than
silently override it — the records + this note give the experimenter everything
needed to pick run 10.

## Distilled pattern (for the master prompt)

For shortest-path / single-pair graph queries with non-negative weights:
1. Reach for **Dijkstra** first; get it correct with a plain lazy heap.
2. The biggest single lever for *single-pair* queries is **bidirectional search**
   (meet-in-the-middle) — it cuts both runtime and memory by shrinking the frontier.
3. **Early-exit** the moment the target is settled.
4. Memory is bought with **CSR/`array` adjacency**, but it costs iteration speed —
   only spend it when memory is the scored priority.
5. Measure before believing: heap-entry encoding and "theoretically better" frontier
   policies did nothing (or hurt) here; only frontier-size reductions paid off.
