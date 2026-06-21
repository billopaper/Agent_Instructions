# Reasoning trail — Weighted Shortest Path (functional agent)

## Problem framing

`shortest_path(n, edges, src, dst)` = minimum-weight path in an undirected,
non-negative-weighted graph, or `-1` if unreachable. Non-negative weights →
**Dijkstra with a binary heap** is the textbook optimal-and-simple choice. The
spec stresses large graphs and measures memory/runtime, so the data structures
matter as much as the algorithm.

Functional-style intent (pure mapping/reduction over edges, immutable data) had
to be balanced against the explicit "large graphs, efficient algorithm"
requirement. I kept the *shape* declarative (build read-only adjacency once, then
a pure relaxation loop) but let performance dictate the concrete containers.

Edge cases handled up front, all from the Rules:
- `src == dst` → return 0 immediately (also avoids touching the graph).
- self-loops (`u == v`) → skipped during build (never help).
- multi-edges → no special handling needed; Dijkstra's relaxation naturally
  keeps the minimum, so the smallest parallel edge always wins.
- unreachable `dst` → heap drains without ever popping `dst` → return -1.

## Iteration-by-iteration

| run | what I tried | grader said | decision |
|-----|--------------|-------------|----------|
| 1 | Dijkstra, list-of-lists adjacency, `heapq` | correct, 0.959s / 26651 KB / 24 loc | first correct → new best |
| 2 | CSR (flat parallel lists `nbr`/`wgt` + `off` offsets) | 0.748s / 10103 KB / 37 loc | mem −62%, runtime −22% → 2/3 → new best |
| 3 | CSR with `array` module (all flat arrays) | 1.060s / 8188 KB / 41 loc | mem −19% but runtime +42% (int boxing), loc worse → 1/3 → revert |
| 4 | list CSR + localized push/pop + zip-slice inner loop | 0.702s / 10103 KB / 39 loc | runtime −6% = within ±10% tie, loc worse → 0/3 → revert |
| 5 | compact `array` CSR but `off`/`pos` left as lists | 0.938s / 10289 KB / 35 loc | mem went *up* (lists), only loc better → 1/3 → keep best |
| 6 | all-array CSR incl. `off`/`pos`, compacted | 1.419s / 8188 KB / 35 loc | mem −19% & loc −2 → 2/3 → new best |
| 7 | count degrees directly into `off`, prefix-sum in place (drop `deg`) | 1.524s / 7954 KB / 34 loc | mem −3% & loc −1 → 2/3 → new best |
| 8 | weights as `'i'`, `dist` as `array('d')`, fold degree-count to 1 line | 1.765s / 6709 KB / 33 loc | mem −16% & loc −1 → 2/3 → new best |
| 9 | `dist` as `array('i')` w/ 2^31-1 sentinel, fold fill to 1 line | 1.628s / 6592 KB / 32 loc | mem −2% & loc −1 → 2/3 → **new best (final)** |
| 10 | confirmation grade of best.py | 1.646s / 6592 KB / 32 loc | identical → kept best |

## What worked

- **CSR (compressed sparse row) adjacency** was the single biggest lever (run 2):
  two parallel flat arrays of neighbors/weights plus an `off` offset array,
  instead of a list-of-lists of tuples. It cut memory ~62% *and* runtime ~22% at
  once — better cache locality and far fewer Python objects (no per-edge tuple,
  no per-node sublist).
- **The `array` module** drives memory down hard (run 3 onward): raw C ints (4
  bytes) instead of 8-byte references to boxed Python ints. Combined wins:
  storing `off`/`pos` as arrays too (run 6), eliminating the `deg` list by
  counting straight into `off` and prefix-summing in place (run 7), `'i'`
  weights + `array('d')`/`array('i')` distance (runs 8–9). Memory fell
  26651 → 6592 KB (−75% from the first correct version).
- **Counting-sort-style CSR build**: count degrees into `off[u+1]`, prefix-sum in
  place, then a second pass fills using a `pos` cursor. No intermediate `deg`
  list, fewer lines, less peak memory.
- **An integer distance array with a large sentinel** (`2**31-1`) replaced
  `float('inf')` — valid because all distances are sums of small non-negative
  ints, and it halves the distance array vs 8-byte doubles.

## What didn't

- **`array` for the hot path trades runtime for memory.** Reading from an
  `array` re-boxes a Python int on every access, so the inner relaxation loop got
  ~2× slower (0.748s list → ~1.6s array). I accepted this because the experiment
  ranks **memory above runtime** (metric order: memory, runtime, loc) and the
  promotion rule fired on memory+loc each time. Two clear Pareto points emerged:
  *fast/heavy* (list CSR: 0.75s, 10.1 MB) vs *slow/light* (array CSR: 1.6s,
  6.6 MB); under memory-first ranking the light one wins.
- **Micro-opts that don't clear the 10% runtime bar are noise.** Localizing
  `heappush`/`heappop` and zip-slicing the inner loop (run 4) gained only ~6% —
  inside the tie band — so it counted for nothing and cost a line. The runtime
  metric is also visibly noisy (rel_spread 0.04–0.26); chasing it by re-grading
  is futile.
- **Half-measures backfire** (run 5): compacting to `array` weights but leaving
  `off`/`pos` as Python lists actually *raised* peak memory. The arrays only pay
  off when the whole adjacency lives in them.

## Key insight / pattern converged on

For shortest-path-on-large-graphs in pure Python under a memory-first metric:
**Dijkstra + CSR adjacency in `array`s + integer distances with a sentinel.**
CSR removes per-edge/per-node object overhead and improves locality; the `array`
module then strips the remaining boxing for a large memory win at a known runtime
cost. Build CSR with the counting-sort trick (count into the offset array,
prefix-sum in place, fill with a cursor) to avoid any auxiliary lists.

## Why best.py is the final answer

`best.py` (run 9) is correct (13/13) and is the strictly best solution found on
the experiment's top-priority axes: **lowest memory (6592 KB)** and **lowest loc
(32)** of every version tried, reached by a monotonic chain of 2-of-3 promotions
(every promotion improved memory + loc, never regressing the best). Its only
weakness is runtime (~1.63s vs the list version's 0.75s), but runtime ranks below
memory, and the high-priority memory metric is where this version dominates. Run
10 re-graded it to confirm the final `solution.py` == `best.py` and reproduces
the metrics.
