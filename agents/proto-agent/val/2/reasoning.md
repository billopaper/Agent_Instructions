# Reasoning trail — weighted-shortest-path (proto-driven agent)

## Task in one line
Min-weight path in a weighted **undirected** graph with non-negative integer weights;
multi-edges (min wins), self-loops (ignore), `src==dst → 0`, unreachable → `-1`.
Large graphs → memory/runtime matter.

## Initial approach and why
Classic, well-known idiom: **Dijkstra with a binary heap** (`heapq`) over an
adjacency list. Non-negative weights ⇒ Dijkstra is correct and near-optimal; a heap
gives `O(E log V)`. Multi-edges need no special handling — the smaller parallel edge
relaxes a node first, so the min is found automatically. Self-loops are skipped at build
time (`u == v`). `src==dst` short-circuits to 0; if `dst` is never popped, return `-1`.
Lazy deletion (`if d > dist[u]: continue`) avoids a decrease-key, which Python's heap
lacks. Early exit on popping `dst` (it's finalized) saves the tail of the search.

This is the proto move: grab the standard pattern, get it correct, then mutate it.

## Iteration log

| run | variant | runtime_s | mem_kb | loc | verdict |
|-----|---------|-----------|--------|-----|---------|
| 1 | heapq Dijkstra, list-of-tuples adjacency, tuple heap | 1.014 | 26653 | 25 | correct → **best** |
| 2 | CSR `array('i')` adjacency, range-index iter | 1.221 | 6837 | 38 | mem −74% only → 1/3, kept |
| 3 | CSR + `zip(slice, slice)` iter | 1.397 | 6713 | 36 | slicing alloc → slower, kept |
| 4 | list-of-tuples + **int-encoded heap** (`nd*n+v`) | 0.960 | 25504 | 27 | mem −1149, rt tie, loc +2 → 1/3 |
| 5 | run 4 golfed to 24 loc | 0.961 | 25504 | 24 | mem + loc → **2/3, best** |
| 6 | CSR + int-heap (memory-optimal corner) | 1.294 | **4425** | 34 | mem −83% only → 1/3, kept |
| 7 | **flat interleaved list `[v,w,v,w]`** + int-heap | **0.418** | **8966** | 25 | rt −56% AND mem −65% → **2/3, best (final)** |
| 8 | flat list + `zip(it, it)` pairwise iter | 0.441 | 8966 | 25 | ≈ run 7, all ties → 0/3 |
| 9 | flat list, build via `adj[u] += (v,w)` | 0.499 | 8981 | 24 | loc only; temp tuples slowed it → 1/3 |
| 10 | (unused — no 2/3 move remained) | | | | |

## What I learned (the levers, mapped as a Pareto frontier)

The three metrics trade off, and the data pins the corners:

1. **Adjacency representation is the dominant memory lever.**
   - list-of-**tuples** (run 1): 26.6 MB — each edge is a 2-tuple object (~56 B) ×2 directions.
   - **flat interleaved list** `[v,w,v,w,...]` (run 7): 9.0 MB — drops the tuple objects, keeps Python ints.
   - `array('i')` CSR (run 6): 4.4 MB — drops the int objects too (4 B each), the memory floor.

2. **Surprise of the experiment: the flat interleaved list is also the FASTEST** (0.418 s),
   beating the tuple version (1.014 s) by 2.4×. Two reasons: building appends bare ints instead
   of allocating 2-tuples (far less GC pressure / peak), and the hot loop avoids per-iteration
   tuple unpacking. The compactness also helps cache locality. So flat-list is not a
   memory-for-speed trade — it wins **both** over tuples.

3. **`array('i')` is the memory floor but the runtime ceiling.** Every `arr[i]` read *boxes*
   a fresh Python int (C int → PyObject), so CSR (runs 2,3,6) ran ~1.2–1.4 s despite the
   tiny footprint. A Python `list` stores real int objects and just hands back a reference —
   faster access. Hence flat **list** beats CSR **array** on runtime, loses on memory.

4. **Int-encoded heap** (`push nd*n+v`, decode `divmod`) beats tuple heap modestly: smaller
   heap objects (one int vs a tuple+two ints) and faster int comparisons. Values stay within
   64-bit for these graphs, so no big-int slowdown. Worth ~5% runtime + ~1 MB.

5. **Iteration idioms are a wash:** `range(0,len,2)` indexing (run 7) ≈ `zip(it, it)` pairwise
   (run 8) ≈ within noise. `zip(slice, slice)` (run 3) is *worse* — slicing allocates copies.

6. **Build idioms matter:** two `.append` calls (run 7) beat `adj[u] += (v, w)` (run 9), because
   `+=` materializes a throwaway tuple per edge (slower build, slightly higher peak).

7. **Early exit on `dst` is a real runtime win** and the reason LOC is stuck at 25: removing it
   would shave 1 line but force exploring the whole component. LOC-down therefore costs runtime,
   so it can't combine with another improvement under the 2/3 rule.

## Why best.py (run 7) is the final answer

It sits on the good corner of the frontier: **fastest measured** (0.418 s) and **second-lowest
memory** (8966 KB), at a tiny 25 LOC. The only thing strictly lighter is the `array` CSR
(4425 KB) — but that costs 3× the runtime and 9 extra lines. Given correctness is locked
(13/13) and the rule promotes only on ≥2-of-3 strict improvement, no further move beats run 7:
lower memory demands arrays (slower), lower LOC demands dropping the early exit (slower). Runtime
and memory are both already near-optimal and pull in opposite directions. Run 7 is the
converged, balanced solution.

## Honest notes
- Promotion went run 1 → run 5 → run 7. Runs 2/3/6 were "wrong direction" on the rule (one
  metric only) but mapped the memory floor — useful, not wasted.
- I left 1 grader run unused on purpose: every remaining idea I could construct improved at most
  one metric against run 7, so spending the run couldn't change the answer.
- Key transferable insight for distillation: **in pure-Python graph code, a flat interleaved
  list of ints is the sweet spot — it beats both the "obvious" list-of-tuples (on speed AND
  memory) and the "clever" `array`/CSR (on speed).** Reach for `array` only when memory is the
  single dominant metric.
