# Reasoning — Weighted Shortest Path (proto-driven agent)

## Task in one line
`shortest_path(n, edges, src, dst)` on an undirected, non-negative-weight graph;
return min total weight or -1. Large inputs ⇒ algorithm + data structures decide
the runtime/memory metrics.

## Initial approach and why
This is a textbook **non-negative weighted shortest path**, so the known idiom is
**Dijkstra with a binary heap** (`heapq`) and lazy deletion. The prototype-driven
move is to drop in that well-worn pattern first, get correctness, then mutate the
data structures iteratively to chase the metrics. Multi-edges and self-loops need
no special handling: Dijkstra's `nd < dist[v]` relaxation naturally keeps the
smaller of parallel edges, and self-loops (`u == v`) can be skipped at build time.

## Iteration log (what / why / verdict / promote-or-revert)

1. **Classic heap Dijkstra**, adjacency = list of lists of `(v, w)` tuples, heap of
   `(dist, node)` tuples. Correct on the first try — 13/13. runtime 0.947, mem 26653,
   loc 25. → first **best**.

2. **Int-packed heap**: push `nd*n + v` instead of a tuple, decode with `% / //`.
   Hypothesis: integer comparison is cheaper than tuple comparison. Verdict: mem
   25504 (better, single ints weigh less than tuples) but runtime 0.98 (tie) and
   loc 28 (worse). Only 1 metric improved → **kept best**. Surprise: packing did
   *not* speed things up on this interpreter.

3. **Compact int-pack**: same idea, squeezed with `divmod` + a semicolon. mem 25504
   (better), loc 23 (better), runtime tie. 2 of 3 → **new best**.

4. **Packed adjacency** `w*n + v` stored in the per-node lists (decode with
   `divmod` in the inner loop): replaces 2·E tuple objects with single ints. mem
   dropped hard to 16129, but runtime 1.15 (worse, the per-edge `divmod`) and loc
   24 (worse). 1 of 3 → **kept best** — but the memory signal was strong.

5. **Compact packed adjacency**: same structure, collapsed with single-line `if`s
   and semicolons to loc 19. mem 16129 (better), loc 19 (better), runtime worse.
   2 of 3 → **new best**. Insight: per-edge `divmod` trades runtime for memory.

6. **CSR via `array('q')`**: two flat machine-int arrays (`to`, `wt`) addressed by a
   prefix-sum `head`, instead of Python lists of objects. mem 9016 (big drop — no
   per-element object overhead), runtime 1.03 (>10% better than 1.15 — direct
   `wt[i]` read, no per-edge divmod), loc 24 (worse). 2 of 3 → **new best**.

7. **CSR + `array('q')` dist**: tried to also compact `dist`. mem 9030 (slightly
   *worse* — the `b'\xff'*(8n)` init creates a transient bytes object, and `dist`
   wasn't the bottleneck), loc 21 (better), runtime tie. 1 of 3 → **kept best**.

8. **Single packed CSR array** (`adj[i] = w*n + v`, one `array('q')` instead of
   two): halves edge storage to 8 bytes/edge. mem 6525 (better), loc 21 (better),
   runtime 1.60 (much worse — per-edge `divmod` is back). 2 of 3 → **new best**.

9. **Two `array('i')` (int32) CSR arrays**: 4 bytes × 2 = 8 bytes/edge (same as the
   packed `'q'`) but read directly with no decode. runtime 1.03 (35% faster than
   run 8!), mem 6526 (+1 KB — a tie, not strictly lower), loc 21 (tie). Only
   runtime improved → **kept best**. This is the painful one: run 9 is essentially
   Pareto-equal to run 8 on memory and *much* faster, but the 2-of-3 rule with a
   1 KB memory tie refuses it.

10. **int32 CSR, early-exit removed** to reach loc 20 (return `dist[dst]`, whose -1
    sentinel covers unreachable). Goal: beat run 8 on runtime AND loc. Verdict:
    runtime 1.475 — only 7.8% under 1.60, i.e. *within* the 10% tolerance = tie;
    mem tie; loc 20 (better). 1 of 3 → **kept best**. Dropping early exit forced a
    full-graph sweep, eating most of the speed advantage.

## What worked
- Dijkstra-from-a-snippet was correct immediately; all 10 runs stayed correct.
- **CSR with `array`** is the decisive structure: flat machine-int arrays cut peak
  memory from ~26 MB to ~6.5 MB by removing Python per-object overhead.
- Packing two fields into one int (`w*n + v`, `nd*n + v`) is a clean, compact idiom
  and lowers LOC, but its `divmod` decode costs real runtime in the hot loop.

## What didn't
- Int-packing the *heap* didn't speed anything up (run 2); tuple comparison was
  already fine on this interpreter.
- Compacting `dist` into an `array` (run 7) backfired on peak memory via the init
  temporary.
- Removing early exit to win a LOC point (run 10) gave back the runtime.

## Key insight / pattern converged on
For large sparse graphs in CPython, **memory is dominated by representation
overhead, not by the algorithm** — moving adjacency from lists-of-tuples to flat
`array` CSR is the single biggest lever. There is a clean three-way trade:
- two `array('q')`        → fastest, highest memory (run 6: 9016 / 1.03 / 24)
- one packed `array('q')` → lowest memory, slow `divmod` decode (run 8: 6525 / 1.60 / 21)
- two `array('i')`        → low memory *and* fast — the genuine sweet spot
                            (run 9: 6526 / 1.03 / 21)

## Why best.py is what it is — and an honest caveat
`best.py` is **run 8** (single packed `array('q')` CSR: mem 6525, runtime 1.60,
loc 21), because it is the last solution the promotion rule (≥2 of 3 strictly
better) accepted.

Honest caveat for the distillation: **run 9 is arguably the better engineering
answer** — two `int32` arrays give effectively the same memory (6526 vs 6525, a
1 KB noise difference) at 35% less runtime, with identical LOC. It failed to
promote only because the tied metric (memory) came out 1 KB higher, so it scored
1-of-3 instead of 2-of-3. Promoting the memory-optimal-but-slow run 8 earlier
created a baseline that the faster run 9 could not dislodge under a strict
2-of-3 rule. Lesson for the master prompt: when two correct solutions are
Pareto-comparable and one is far faster at near-identical memory, a strict
"improve ≥2 of 3, ties don't count" gate can lock in a worse-overall winner;
the metric priority in the config (memory > runtime > loc) suggests run 8 is the
intended winner anyway, but the run 9 trade-off deserves to be on record.
