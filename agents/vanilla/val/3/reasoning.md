# Reasoning — Weighted Shortest Path

## Problem framing
Single-pair shortest path in a weighted **undirected** graph, non-negative integer
weights, possibly large (thousands of nodes/edges). Classic Dijkstra with a binary
heap is the right tool: O((V+E) log V), non-negative weights guaranteed. Multi-edges
and self-loops are spec'd; self-loops are dropped (`u == v`), multi-edges are handled
because Dijkstra naturally ignores the worse of two parallel edges. `src == dst → 0`,
unreachable → `-1`.

## Iteration trail

**Run 1 — baseline lazy Dijkstra (list-of-tuples adjacency).** Correct 13/13.
`1.109s / 30012 KB / 22 loc`. First correct → `best.py`. Standard textbook version:
push every relaxation, skip already-settled nodes on pop, return when `dst` is popped.

**Run 2 — CSR / compact arrays (`array('i')`/`array('q')`).** Idea: a list of lists
of tuples is memory-heavy in CPython (~56 B per tuple). Flattening to compressed
sparse row with typed arrays should slash peak memory. Result: `1.241s / 14069 KB /
37 loc`. Memory **halved**, but runtime regressed ~12% (per-edge `to[i]`/`wt[i]` array
indexing is slower than tuple unpacking) and loc ballooned. Only 1/3 improved →
reverted.

**Run 3 — decrease-key pruning on the fast list adjacency.** Kept the fast
`for v, w in adj[u]` iteration but added a tentative-distance array: only push when
`nd < dist[v]`, skip stale pops via `d > dist[u]`. Fewer redundant heap pushes →
both faster and a smaller heap. Result: `0.962s / 26653 KB / 25 loc`. Runtime −13%
(>10%) **and** memory lower → 2/3 → **promoted**. This became the runtime-optimal
"clean Dijkstra" baseline.

**Run 4 — CSR + pruning + local heap binding.** Tried to grab CSR's memory win *and*
the pruning speedup together. Result: `1.003s / 9239 KB / 42 loc`. Memory crushed to
9 MB, but runtime only tied 0.962 (array indexing overhead cancels the pruning gain)
and loc 42. Only 1/3 → reverted. **Key tension confirmed: in pure Python, compact
storage (arrays) and fast iteration (tuples) pull in opposite directions; they sit on
a Pareto frontier and the 2-of-3 rule won't promote a pure memory play.**

**Run 5 — packed-int adjacency (`w*n+v`, one int per neighbor).** A middle point:
list of single ints (smaller than tuples) decoded with `% n` / `// n`. Result:
`1.023s / 18416 KB / 29 loc`. Memory landed *between* tuples (26653) and CSR (9239),
exactly as predicted, but the two divisions per edge made runtime a tie. 1/3 →
reverted. Good data point mapping the memory/runtime curve.

**Run 6 — local heap binding on the tuple version.** `push = heapq.heappush; pop =
heapq.heappop`. Result: `0.954s / 26653 KB / 27 loc` — ~1% faster = a tie. The C-level
heap operations dominate; rebinding the lookup saves almost nothing. Not worth +2 loc.
Reverted. **Insight: this micro-opt is noise here.**

**Run 7 — dedup multi-edges (per-node dict of min weights).** Decisive. Built
adjacency as a dict per node keeping the minimum weight per neighbor. Result:
`0.512s / 16589 KB / 35 loc`. Runtime **−47%** and memory lower → 2/3 → **promoted**.
The huge speedup reveals the hidden large graphs contain **many duplicate/parallel
edges**: collapsing them to the minimum weight shrinks the effective edge set the heap
ever sees, cutting both heap traffic (runtime) and stored neighbors (memory). This was
the single most important discovery — an *algorithmic* win that dwarfs every
data-structure micro-opt above.

**Run 8 — cleaner dedup (pre-allocated `[{} for _ in range(n)]`, `dict.get`).** Same
idea, tidier build without `None` guards. Result: `0.464s / 16595 KB / 29 loc`.
Runtime −9.3% vs run 7 — **just under the 10% bar, so a tie**; memory equal; loc
better. Only 1/3 strictly improved → kept run 7 by the rule. (Genuinely a nicer
solution, but the promotion rule treats sub-10% runtime as a tie.)

**Run 9 — clean dedup + local binding.** `0.471s / 16595 KB / 31 loc`. Binding again
did nothing (0.464 → 0.471 is noise). Runtime still a sub-10% tie → kept run 7.

**Run 10 — final confirmation.** Re-graded the restored `best.py` (run 7 code):
`0.470s / 16589 KB / 35 loc`, 13/13. Notably the *same* run-7 code measured 0.470 here
vs 0.512 at run 7 — proving runs 7/8/9 were all within measurement noise and the "tie"
classifications were correct.

## What worked / what didn't
- **Worked (big):** deduping parallel edges to per-node minimums (run 7). An
  algorithmic property of the data, not a code trick. Halved runtime.
- **Worked (moderate):** decrease-key pruning (run 3) — fewer heap pushes, faster and
  lighter than naive push-everything.
- **Didn't move the needle:** local function binding (~1%, runs 6/9).
- **Pure trade-offs, never 2/3:** CSR arrays (run 4, min memory 9 MB but slow + verbose)
  and packed ints (run 5, mid memory, slow). Memory and runtime conflict in CPython;
  the 2-of-3 rule structurally favors the runtime/loc-balanced point over a pure
  memory minimum.

## Why `best.py` is the final answer
`best.py` is the run-7 dedup Dijkstra: `0.512s / 16589 KB / 35 loc`, correct 13/13.
It is the only solution that won **two** metrics (runtime −47%, memory) over the
baseline, driven by the real insight (collapse duplicate edges). The cleaner run-8/9
variants are arguably nicer code and effectively tie it on runtime/memory while using
fewer lines, but each improved only **one** strict metric (loc) — the runtime edge fell
~1 percentage point short of the 10% promotion threshold — so the rule correctly keeps
run 7. If the goal were code quality over the letter of the metric rule, run 8 (clean
`[{} for _ in range(n)]` + `dict.get`, 29 loc, same speed/memory) would be the pick;
under the 2-of-3 promotion rule, run 7 stands.
