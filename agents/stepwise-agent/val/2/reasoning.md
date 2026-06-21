# Reasoning — Weighted Shortest Path (stepwise agent)

## Problem framing & initial approach

Single-source single-target minimum-weight path in an **undirected, non-negative-weight**
graph, possibly large (thousands of nodes/edges), with multi-edges (min wins) and self-loops
(ignored). Non-negative weights ⇒ **Dijkstra** is the right algorithm class; Bellman-Ford
(O(VE)) would be far too slow on large inputs.

Following the stepwise style: start with the simplest correct implementation, then introduce
**one** focused refinement per iteration, always re-grading and keeping correctness first.

Multi-edges need no special handling: Dijkstra's `nd < dist[v]` relaxation naturally keeps the
cheapest edge. Self-loops are skipped at build time. `src == dst` short-circuits to 0.

## Iteration-by-iteration trail

- **Run 1 — forward Dijkstra, list-of-tuples adjacency, heapq.** First correct (13/13).
  Metrics `(0.951s, 26653 KB, 25 loc)`. Became `best.py`. This is the simple baseline.
- **Run 2 — micro-opt: localize `heappush/heappop`, `INF` constant.** `(0.964s, 26653, 26)`.
  Runtime tie, memory tie, loc +1. **No gain → reverted.** Lesson: attribute-lookup
  micro-opts don't move this workload; the cost is elsewhere.
- **Run 3 — CSR adjacency via `array` (structural, memory-targeted).** Packed neighbor/weight
  arrays instead of per-node lists of tuples. `(1.190s, 7964, 47)`. **Memory −70%** but
  runtime +25% and loc +22 → only 1/3 → kept best. Lesson: pure-Python `array` indexing in
  the hot loop is slower than unpacking tuples from a list. Memory and runtime are **traded
  off** by the adjacency representation.
- **Run 4 — CSR + `zip(nbr[a:b], wt[a:b])` iteration.** `(1.295s, 7965, 48)`. Slower than
  run 3 — per-pop slice allocation costs more than direct indexing. Reverted idea.
- **Run 5 — bidirectional Dijkstra (algorithmic, runtime-targeted).** Search from `src` and
  `dst`, expand the smaller frontier, stop when `top_f + top_b ≥ best`. `(0.868s, 24469, 43)`.
  Memory strictly lower **and** runtime 8.7% lower — but 8.7% is **within the 10% tolerance =
  a tie**, so only 1/3 counts. Kept best. The single most important result: bidirectional
  raw-dominates run 1 on both memory and runtime, yet the rule scores it 1/3.
- **Run 6 — bidirectional + `nd < best` pruning + cached heap tops.** `(0.875s, 24433, 45)`.
  Neutral: the `top_f+top_b ≥ best` stop condition already eliminates late work, so the prune
  rarely fires. Still 1/3.
- **Run 7 — bidirectional + CSR (combined).** `(1.004s, 5411, 68)`. **Memory champion: −80%**
  vs run 1 (bidirectional explores fewer nodes ⇒ smaller heaps, plus packed adjacency). It
  **dominates run 3** (lower memory and faster). But runtime +6% and loc +43 → 1/3.
- **Run 8 — compact forward Dijkstra (loc-targeted).** Same algorithm as run 1, semicolon-
  joined relaxations. `(0.951s, 26653, 22)`. Identical runtime/memory, loc −3 → it **weakly
  dominates run 1**, but only 1/3 improves, so the rule still blocks promotion.

Runs 9–10 left unused: I had mapped the full frontier and confirmed no 2/3 improvement is
reachable; re-grading byte-identical code only chases median noise (which the grader filters),
so I restored `solution.py` from `best.py` instead of spending runs.

## What worked, what didn't, key insight

- **Worked:** the simplest correct Dijkstra (run 1) is already excellent and hard to beat.
  CSR is a genuine, large memory lever (−70 to −80%). Bidirectional is a genuine runtime +
  memory lever.
- **Didn't:** attribute-localization and zip-slicing micro-opts; pruning on top of an already
  tight bidirectional stop condition.
- **Key insight — a Pareto frontier, not a single winner:**
  - run 1 / run 8: fastest & simplest (run 8 = run 1 with fewer lines).
  - run 6: bidirectional — best balance, raw-beats run 1 on memory **and** runtime.
  - run 7: minimum memory (5411 KB), dominates run 3.
  These three points don't dominate each other across all metrics. **Memory and runtime are
  coupled through the adjacency representation** (list-of-tuples = fast/heavy; CSR =
  slow/light), and the best runtime lever (bidirectional, ~8–9%) sits **just under the 10%
  promotion threshold**. Consequently *no* candidate improves ≥2 of 3 metrics over run 1:
  memory+runtime is impossible (runtime never qualifies), memory+loc is impossible (low-memory
  code is verbose), runtime+loc is impossible (runtime never qualifies).

## Why `best.py` is the final answer

Under the promotion rule (overwrite only on ≥2/3 strictly-improved, runtime needing >10%),
**run 1 is never displaced**, so `best.py` = the run-1 forward Dijkstra. It is correct (13/13),
the simplest, and fastest-tier.

**Honest caveat for the human ranker / prompt distillation:** the rule's outcome diverges from
raw quality here. Run 8 weakly dominates run 1 (same speed/memory, 3 fewer lines). If memory is
weighted highest (as the config's metric order suggests), run 7 (−80% memory) or the balanced
bidirectional run 6 (raw-better than run 1 on both memory and runtime) would be preferable. The
10%-runtime-tolerance + ties-aren't-improvements rule is what kept the naive baseline as `best`
despite strictly-better Pareto points existing — a finding worth carrying into the master
prompt.
