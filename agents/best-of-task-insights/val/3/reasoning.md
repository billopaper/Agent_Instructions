# Reasoning — weighted-shortest-path (best-of, task-insight engineering)

## Problem & initial approach
Undirected, non-negative weighted graph; min-weight path `src → dst`, `-1` if unreachable. With `w >= 0` and "inputs may be large", the canonical algorithm is **Dijkstra with a binary heap** (`heapq`, C-level). I committed to that from run 1 and folded every edge case into construction rather than special-casing:
- `src == dst → 0` returned up front.
- self-loops skipped at build (`if u != v`) — they never help.
- multi-edges need no dedup: Dijkstra finalizes the smallest tentative distance first, so the cheapest parallel edge wins naturally.
- unreachable → the natural fall-through `return -1` (and a `-1`/`INF` distance sentinel is unambiguous since all real distances are `>= 0`).
- single-node / edgeless work by construction.

Correctness held at **13/13 on every single run** — the algorithm class was right from the start, so all 10 runs went into moving metrics.

(Note: the grade command in the brief used `../../../grading` but this folder is one level deeper (`val/3`), so the real path is `../../../../grading`. Corrected on run 1.)

## Iteration log
| run | approach | runtime | mem(kb) | loc | outcome |
|-----|----------|---------|---------|-----|---------|
| 1 | heapq Dijkstra, adj = list of tuples, push every unvisited neighbor | 1.201 | 30012 | 22 | first correct → best |
| 2 | tentative-dist relaxation: push **only on strict improvement** | 0.952 | 26653 | 25 | runtime −21% & mem ↓ → **best (2/3)** |
| 3 | CSR adjacency on `array` (flat packed ints) | 1.303 | 7957 | 37 | mem −70% but runtime +37%, loc ↑ → 1/3, kept |
| 4 | int-encoded heap on tuple-adj base | 0.968 | 25504 | 27 | mem −1.1MB only, runtime tie → 1/3, kept |
| 5 | CSR on **Python lists** + tentative-dist | 0.837 | 9871 | 36 | runtime −12% & mem −63% → **best (2/3)** |
| 6 | CSR on `array`, minified | 1.301 | 7957 | 25 | mem floor & loc ↓ → **best (2/3)** |
| 7 | + `dist` as `array('q')` | 1.357 | 7957 | 24 | mem unchanged, loc ↓ → 1/3, kept |
| 8 | + `wt` as 32-bit `array('I')` | 1.368 | 6712 | 24 | mem −16% & loc → **best (2/3)** |
| 9 | + **int-encoded heap key `nd*n+v`** + merged init line | 1.357 | 4425 | 23 | mem −34% & loc ↓ → **best (2/3)** ← final |
| 10 | list-CSR + int-heap (fast corner) | 0.851 | 8723 | 23 | runtime fast but mem 2× → 1/3, kept |

## What drove each metric (the diagnoses)
- **Runtime, lever 1 (run 2):** the biggest win wasn't a faster heap, it was *fewer heap operations*. Run 1 pushed an entry for every unfinalized neighbor; switching to a tentative-distance array and pushing **only on strict improvement** cut heap churn → −21% runtime *and* lower peak. One structural change, two metrics.
- **Memory is the adjacency representation, not the heap (runs 3–4).** Run 3 (CSR on `array`) cut memory 70% by deleting ~2·E tuple objects; run 4 (int-heap on tuple-adj) cut only ~1MB. That isolated the variable: the **list-of-tuples adjacency is the memory hog**, the heap is secondary — *on a memory-heavy base*.
- **The representation trade-off, resolved (run 5).** `array` CSR was lean but slow because every `wt[i]`/`nbr[i]` access *boxes a fresh Python int* in the hot loop. Swapping to **Python lists** (CSR layout, but list slots hold existing int objects → no boxing) recovered the speed *and* beat the tuple version on both runtime and memory. List-CSR was the key insight: flat layout + no per-access boxing.
- **Then the memory corner (runs 6–9), once I prioritized memory (the #1 scored metric):**
  - `array` CSR minified to 25 loc → memory floor 7957 at the cost of runtime (run 6).
  - `dist` as `array` did **nothing** (run 7) — proof the peak is the E-sized edge arrays, not the V-sized `dist`.
  - `wt` as 32-bit `'I'` halved the weight array → 6712 (run 8); weights fit 32-bit while sums stay safe in the 64-bit `dist`.
  - **int-encoding the heap** (`nd*n+v` as one int instead of a `(nd,v)` tuple) cut another 34% → **4425** (run 9). So once the adjacency was packed, the heap *did* become a large share of peak — the diagnosis flips with the base.

## What didn't work / was noise
- int-encoded heap on a tuple-adj base (run 4) was runtime-neutral: `divmod` per pop offset the single-int comparison gain, and the memory saving was tiny because adjacency dominated.
- `dist` container choice was invisible at peak (run 7) — V-sized structures don't matter when E-sized ones set the peak.
- No micro-tweaks were even attempted (try/except vs membership, local binding) — past tasks showed these are measurement noise.

## Why best.py (run 9) is the final answer
Two clean Pareto corners emerged:
- **Run 9** (`array`-CSR + 32-bit weights + int-heap): 1.357s / **4425kb** / 23 loc — memory and loc optimal.
- **Run 10** (list-CSR + int-heap): **0.851s** / 8723kb / 23 loc — runtime optimal.

The experiment's metric priority is **memory > runtime > lines_of_code**. Run 9 wins the top metric decisively (4425 vs 8723, ~2×) and ties loc, conceding only runtime (#2). It also dominates the original solution: same correctness, 6.8× less memory than run 1. I deliberately did **not** let the mechanical "2-of-3" rule promote a runtime-fast but memory-heavy variant over it, because that would regress the highest-priority metric — the rule is a heuristic for monotone progress, not a license to trade the #1 metric for two lower ones.

**Key pattern for distillation:** get the canonical algorithm correct with edge cases by construction; then move metrics with *structural* levers diagnosed one at a time — (a) cut heap operations by pushing only on improvement, (b) pack adjacency into flat CSR (lists when runtime matters, `array` + narrowest int type when memory matters), (c) int-encode heap entries to collapse tuples once adjacency is packed. The memory bottleneck *moves* as you optimize (adjacency → heap), so re-diagnose after each change; and let the scored-metric priority, not a blind 2-of-3 count, pick the final among Pareto-equivalent corners.
