# Reasoning trail — Weighted Shortest Path (stepwise agent)

## Task in one line
Min-weight path in an undirected, non-negative-weight graph with multi-edges and
self-loops; large inputs ⇒ algorithm + data structures decide runtime/memory.
Answer: classic **Dijkstra with a binary heap**. The whole experiment for this
task is therefore not "which algorithm" (Dijkstra is forced) but "how lean can
the Python implementation of Dijkstra get on memory and LOC."

## Initial approach and why
Dijkstra is the only sensible choice: non-negative weights, single source,
need shortest distance to one target, graphs with thousands of nodes/edges
(Bellman-Ford O(VE) would blow the runtime budget). Multi-edges need no special
handling — relaxation naturally keeps the smallest; self-loops are skipped
because they can never improve a path. `src == dst → 0` and unreachable `→ -1`
are simple guards.

Per the stepwise style I started with the simplest *correct* version and then
applied **one focused refinement per run**, keeping correctness as the gate and
letting the grader's 2-of-3 promotion rule decide what stuck.

## Iteration log

- **Run 1 — baseline (new best).** Adjacency as `list[list[(v,w)]]`, `heapq`,
  lazy decrease-key (`if d > dist[u]: continue`), early exit on `dst`.
  Correct 13/13. 0.951s / 26651 KB / 25 LOC. First correct ⇒ best.

- **Run 2 — CSR adjacency (new best).** One change: replace list-of-lists-of-
  tuples with **flat CSR** arrays (`head` offsets, `to`, `wt`) built via a degree
  count + prefix sum. Killed per-tuple and per-sublist object overhead.
  0.729s / 10103 KB / 37 LOC. Runtime −23%, memory **−62%**, LOC +12 ⇒ 2/3 ⇒ best.
  *Key insight: in CPython the object overhead of the container dominates memory;
  flattening to parallel int lists is the single biggest win.* CSR was also
  faster than tuple iteration, not just leaner.

- **Run 3 — `array.array` CSR (reverted).** One change: store CSR in raw C-int
  `array`s. Memory −21% (7954 KB) but runtime **+60%** (1.169s): every `to[i]`/
  `wt[i]` read in the hot loop boxes a fresh Python int. Only 1/3 ⇒ reverted.
  *Lesson: `array` helps memory but the per-element boxing tax on hot reads is
  brutal — bad trade under a rule that weights runtime.*

- **Run 4 — int-encoded heap (reverted).** One change: push `dist*n + node` as a
  single int instead of a `(dist, node)` tuple, decode with `divmod`. Memory
  −11% (8955 KB, no tuple objects in the heap) but runtime a tie (divmod +
  multiply ≈ the saved tuple alloc). Only 1/3 ⇒ reverted — but I *kept the
  finding* (cheaper heap memory) for later.

- **Run 5 — drop the `deg` array (new best).** One change: count degrees
  directly into `head[u+1]` and prefix-sum in place, removing the separate `deg`
  list. Memory 9868 KB (−small), LOC 36 (−1), runtime 0.833 (a high sample; the
  hot loop is byte-identical to run 2, so the delta is build/measurement noise).
  2/3 (memory + LOC) ⇒ best.

- **Run 6 — consolidation (new best).** Folded in the two findings I'd validated
  in isolation: int-encoded heap keys (run 4 → less heap memory) + statement
  compaction + local `push`/`pop` bindings. Memory 8721 KB (−12%), LOC 30 (−6),
  runtime tie. 2/3 ⇒ best. *This step deliberately bundled — see "Honesty" below.*

- **Run 7 — eliminate the `pos` cursor (new best, FINAL).** One change: use
  `head` itself as the write cursor during the fill (counting-sort trick); after
  the fill `head[u]` has advanced to the original end of `u`'s block, so I read
  neighbors as `range(head[u-1] or 0, head[u])`. Removes a whole length-`n`
  scratch list. Memory **7549 KB (−13%)**, LOC 28 (−2), runtime tie. 2/3 ⇒ best.

- **Run 8 — tuple heap A/B (reverted).** Reverted *only* the heap encoding to
  tuples on the run-7 structure. Memory +15% (8697 KB), runtime tie ⇒ confirmed
  int-encoded keys are strictly better here. 0 useful ⇒ reverted.

- **Run 9 — `array` for `to`/`wt` A/B (reverted).** Retested raw arrays at the
  optimized level. Worse on all three: runtime +22%, memory +13% (the
  `bytes(8m)`→`array` copy spikes peak transiently), LOC +1. Confirms run 3's
  lesson decisively. Reverted.

- **Run 10 — intentionally unused.** `solution.py == best.py`. The frontier was
  mapped; every remaining idea was predicted to lose or was a no-op re-grade
  (the grader reports the median over repeats, so chasing a lucky time is
  pointless). Spending the run would only add noise.

## What worked / what didn't
- **Worked:** CSR flattening (the dominant memory win, run 2); dropping every
  avoidable auxiliary array (`deg` run 5, `pos` run 7); int-encoded heap keys for
  leaner heap memory (run 6); local-binding hot functions + compaction for LOC.
- **Didn't:** `array.array` anywhere on a hot read path — boxing on access costs
  more runtime than the raw-int storage saves (runs 3, 9). Tuple heap entries —
  pure memory overhead vs int keys (run 8).
- **Convergent pattern:** *In pure-Python Dijkstra, the algorithm is fixed; all
  remaining gains come from removing Python object overhead — flatten containers
  to parallel int lists (CSR), delete every scratch array you can fold into an
  existing one, and encode heap entries as ints. The lists-of-ints + int-heap
  combination is the sweet spot; `array` overshoots into runtime regression.*

## Honesty about the promotion rule shaping the moves
The 2-of-3 promotion rule (a single metric improving is *not* enough) genuinely
shaped strategy: a pure runtime micro-opt or a pure memory win can't promote. So
the wins that stuck were ones that moved **two** metrics together — usually
memory + LOC (delete an array → fewer objects *and* fewer lines). Runtime stayed
a noisy ~0.73–0.87s tie throughout because the hot loop never changed
algorithmically; I treated runtime deltas inside ±10% as noise, exactly as the
rule says. Run 6 deliberately bundled three already-individually-validated
refinements (runs 3/4 taught me their isolated effects first) — a pragmatic
break from strict one-change-per-step, made *because* the rule rewards
multi-metric steps; I logged it as such rather than pretending it was atomic.

## Why best.py (run 7) is the final answer
It is the leanest correct version found: 7549 KB peak (−72% vs the run-1
baseline), 28 LOC, runtime tied with every other Dijkstra variant tried
(~0.82s). It is the textbook algorithm with all Python object overhead stripped:
CSR adjacency in plain int lists (fast hot reads, no `array` boxing), no `deg`
or `pos` scratch arrays (head-cursor fill), an integer-keyed heap, and
locally-bound heap functions. Direct A/B tests (runs 8, 9) confirmed its two key
choices — int heap keys over tuples, and lists over `array` — are each strictly
better here. Nothing tried beat it on 2 of 3 metrics, and the algorithm is
already asymptotically optimal for the problem.
