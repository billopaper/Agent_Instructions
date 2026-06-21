# Reasoning — 01_lru-cache (stepwise agent)

## Style applied
Stepwise refinement: start with the simplest correct thing, then change exactly **one**
thing per iteration, keeping correctness as the gate at every step. Each run below is a
single focused change, graded before the next change is considered.

## Initial approach and why
I began with the most obvious correct implementation — a `dict` for storage plus a Python
`list` holding keys in recency order (LRU at the front, MRU at the end). It is trivially
easy to reason about: `get`/update do `list.remove(key)` then `append`; eviction does
`pop(0)`. Brute force, maximum clarity. The point of step 1 is a correct anchor, not speed.

## Iteration log

**Run 1 — dict + list (O(n) recency).** Correct, 11/11. Metrics: 40.69s, 12444 KB, 22 loc.
First correct → `best.py`. The 40s runtime is the tell: `list.remove` and `pop(0)` are O(n),
and the hidden suite scales inputs, so every operation pays a linear scan.
*(A second grader process was launched by accident on the same file; I stopped it before it
counted, so it consumed no run. Lesson recorded: launch one grader at a time.)*

**Run 3 — `collections.OrderedDict` (one change: replace the dict+list).** Correct.
0.287s, 14596 KB, 16 loc. `move_to_end` and `popitem(last=False)` are C-level O(1), so
runtime collapsed ~140x and loc dropped. Runtime + loc improved (2 of 3) → promoted.
The one regression: memory rose (12444 → 14596) because OrderedDict maintains an internal
doubly-linked list on top of the hash table.

**Run 4 — plain `dict` (one change: drop OrderedDict, use insertion order).** Correct.
2.03s, 11339 KB, 16 loc. Python 3.7+ dicts preserve insertion order, so recency =
`d[k] = d.pop(k)` (move to end) and LRU = `next(iter(d))`. Memory dropped to the leanest of
all approaches (no linked-list overhead), but runtime rose to ~2s: repeated pop+reinsert
churns the dict's table and triggers periodic rebuilds, which `move_to_end` avoids by simply
relinking. Only memory improved (1 of 3) → kept best, recorded as a real tradeoff.

**Run 5 — plain dict, merged the `get` reinsert into one line (one change).**
`self.store[key] = value = self.store.pop(key)` collapses the temp-var dance to a single
readable line. Correct. 1.99s, 11339 KB, 15 loc. vs best: memory **and** loc strictly lower
(2 of 3) → **promoted to final best.py**. Runtime regressed, but the experiment ranks metrics
**memory > runtime > loc**, so winning the #1 metric (memory) plus #3 (loc) at the cost of #2
is the rule-correct and priority-aligned trade.

**Run 6 — manual doubly-linked list + dict (one change: classic textbook O(1)).**
Correct. 0.394s, 20614 KB, 35 loc. The "optimal" structure is fast (close to OrderedDict)
but pays heavily: explicit node objects are the heaviest memory of all four approaches and
more than double the loc. Only runtime improved (1 of 3) → kept best. Valuable as the
opposite corner of the design space, and a reminder that "textbook optimal" optimizes the
wrong axis when memory and loc are scored.

**Run 7 — re-grade of best.py.** 1.96s, 11339 KB, 15 loc, 11/11. Confirms the submitted
file's metrics are stable (median over repeats), matching run 5 within tolerance.

## What worked / what didn't
- **Worked:** stepwise single-change discipline made each metric shift attributable to one
  cause — the O(n)→O(1) jump (run 3), the memory/runtime tradeoff of the storage choice
  (runs 3 vs 4), and a clean loc trim (run 5).
- **Didn't:** the manual DLL — more code and more memory bought only the runtime I'd already
  largely have from OrderedDict. Over-engineering against the scored metrics.

## Key insight
For an LRU cache there is a genuine **memory-vs-runtime tradeoff in the storage primitive**:
- `OrderedDict` / manual DLL keep an explicit linked list → O(1) relink, **fast**, but extra
  per-entry memory.
- a plain `dict` carries no link overhead → **least memory**, but recency updates churn the
  table → slower.

There is no dict-based structure that is simultaneously lowest-memory and fastest; the linked
list is exactly the memory you pay for the speed.

## Why best.py is the final answer
Plain dict, 15 loc — the lowest **memory** (11339 KB) and lowest **loc** (15) of every
approach tried, and correct on all hidden categories. It wins the experiment's top-priority
metric (memory) and the third (loc); it satisfies the promotion rule (≥2 of 3 strictly
improved over the previous best) at the only price being runtime, the #2 metric. Memory and
loc are at the dict-store floor, so no remaining single refinement could improve 2 of 3 —
which is why I stopped with 3 runs in reserve rather than churn for a lucky median.
