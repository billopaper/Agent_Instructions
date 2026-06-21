# Reasoning — 01_lru-cache (smart-pattern agent)

## Final answer
`best.py` = **`dict` subclass** (plain dict, insertion-order eviction):

```python
class LRUCache(dict):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity
    def get(self, key):
        if key not in self: return -1
        self[key] = self.pop(key)
        return self[key]
    def put(self, key, value):
        if key in self: del self[key]
        elif len(self) >= self.capacity: del self[next(iter(self))]
        self[key] = value
```

Metrics: **runtime 1.759 s · peak_memory 11339 kb · loc 12** (run 6). Correct 11/11 on every run.

## Initial approach and why
Smart-pattern brief = pick the smartest idiomatic structure. For LRU the textbook "smart" Python answer is `collections.OrderedDict` with `move_to_end` (O(1) recency refresh) and `popitem(last=False)` (O(1) LRU eviction). I started there (run 1): correct first try, 0.309 s / 14596 kb / 16 loc → first `best.py`.

## Iteration trail
- **Run 1 — OrderedDict wrapper.** Correct. 0.309 / 14596 / 16. New best (baseline).
- **Run 2 — plain `dict` wrapper** (exploit dict insertion-order since 3.7; move-to-end via `pop`+reinsert, evict via `next(iter(...))`). Correct. 1.746 / **11339** / 15. Memory and loc both strictly lower → 2/3 → promoted. **But runtime regressed ~5.6×.** Insight: plain-dict `del`+reinsert on every churn accumulates tombstones, forcing CPython to periodically O(n)-compact the table; OrderedDict relinks a linked list and barely mutates its underlying dict, so it avoids compaction under get-heavy churn.
- **Run 3 — doubly-linked-list + hashmap** (classic O(1), list-as-node to avoid a Node class). Correct. 0.391 / **20614** / 36. Fast but heaviest memory and most loc → only 1/3 improved → kept best. Confirms: explicit linked nodes cost the most memory.
- **Run 4 — OrderedDict *subclass*** (the cache *is* an OrderedDict; multi-line). Correct. 0.299 / 14596 / 16. Only runtime improved vs best (1/3) → kept best. Subclassing did **not** lower memory vs the wrapper.
- **Run 5 — OrderedDict subclass, terse** (one-line `if` bodies). Correct. 0.296 / 14596 / **13**. Runtime + loc improved vs best (2/3) → promoted. Fast *and* terse.
- **Run 6 — `dict` subclass, terse** (no import). Correct. 1.759 / **11339** / **12**. Memory + loc improved vs best (2/3) → promoted. This is the current/final best.
- **Run 7 — `dict` subclass minus the no-op `super().__init__()`.** Correct. 1.731 / 11339 / **11**. A *strict Pareto improvement* over run 6 (never worse, better on loc), but memory tied and runtime tied (within ±10%), so only **1** metric strictly improved → the 2-of-3 rule **blocked** promotion → kept run 6. (Quirk noted below.)

## The real structure: a Pareto frontier from one algorithmic fact
Maintaining **exact** LRU order keyed by a hash needs one of:
- **O(1) relink** (OrderedDict / DLL) → an extra linked-list layer → ~2× per-entry memory; OR
- **pop + reinsert** in a plain dict → tombstone compaction → ~5.6× runtime.

So you cannot get *light AND fast* with a terse structure. The three corners:
| variant | runtime | memory | loc |
|---|---|---|---|
| OrderedDict subclass (A) | 0.296 (fast) | 14596 (heavy) | 13 |
| dict subclass (B, final) | 1.759 (slow) | **11339 (light)** | 12 |
| DLL + hashmap | 0.391 (fast) | 20614 (heaviest) | 36 |

A and B are Pareto-incomparable; the DLL is dominated for this scoring.

## Why B (the light one) is the final answer — the key strategic insight
The **experiment ranks metrics lexicographically: memory > runtime > lines_of_code.** Memory is the top non-correctness metric, and plain dict sits at the **memory floor** (~11339 kb — half of OrderedDict's per-entry cost; I could find nothing correct that goes lower). So the lightest correct solution is the experiment-optimal one, and B wins the ranking despite its slow runtime.

Crucially, the **2-of-3 promotion rule is a local proxy that is *not* aligned with that lexicographic priority.** From B, I could have golfed a fast OrderedDict subclass down to ~10 loc (dropping the no-op `super().__init__()`), improving runtime + loc = 2/3, and the rule would *permit* swapping `best.py` to it — but that move trades away the #1 ranked metric (memory) for the #3 (loc) plus a #2 (runtime) I don't need. Chasing the promotion rule via loc-golf would push me *off* the memory-optimal point. Recognizing this, I deliberately stopped at run 7 with 3 runs unused rather than burn them on rule-permitted-but-ranking-harmful oscillation between the two Pareto corners.

## What worked / what didn't
- **Worked:** OrderedDict as the safe correct baseline; exploiting dict insertion-order for the memory win; subclassing to cut the wrapper indirection and loc; reasoning about CPython internals (tombstone compaction, OrderedDict's linked layer) to *explain* the runtime/memory split rather than treat it as noise.
- **Didn't:** the DLL (worst on two of three metrics here); assuming subclassing OrderedDict would save memory (it didn't — the linked layer dominates); expecting a single solution to dominate all three metrics (the frontier forbids it).

## Two rule quirks worth distilling into the master prompt
1. **2-of-3 vs lexicographic priority mismatch.** A "≥2 metrics improve" promotion gate can walk the agent away from the lexicographically top-ranked metric. A smart agent should optimize the *declared metric priority*, using the promotion rule only when it agrees with it — and stop, rather than oscillate, between Pareto corners.
2. **2-of-3 can reject a strict Pareto improvement.** Run 7 dominated run 6 (≤ on every metric, < on loc) yet was blocked because only one metric *strictly* improved (the other two tied). The gate should arguably treat "≥1 strictly better and none worse" as promotable.
