# Reasoning Trail — 01_lru-cache (OOP agent / Mustermann)

## Problem framing (OOP lens)
An LRU cache is a small object with two responsibilities: (1) **storage** — map key→value
with O(1) lookup; (2) **recency** — a total order over keys so the least-recently-used one can
be evicted in O(1). The whole design question is which structure carries the recency order.
I modelled `LRUCache` as the single abstraction that *encapsulates* both, exposing only
`get`/`put` over a hidden store. State and behaviour live together; the recency mechanism is a
private implementation detail behind the interface.

## Initial approach (run 1) — explicit doubly-linked list + hashmap
The canonical OOP LRU: a `_Node` class (with `__slots__`) for each entry, a `dict` mapping
key→node for O(1) lookup, and a doubly-linked list with head/tail sentinels encoding recency
(most-recent just after head, eviction candidate just before tail). Private helpers `_remove`
and `_add_front` keep the list manipulation in one place.
- **Verdict:** correct 11/11, runtime 0.353s, memory 18268 KB, loc 52. → first `best.py`.
- This is the most *explicit* model (every pointer visible) but also the heaviest: Python-level
  `_Node` objects cost memory, and the pointer juggling runs in interpreted code.

## Run 2 — delegate recency to `collections.OrderedDict` (the winner)
Same two responsibilities, but recency is delegated to an `OrderedDict`: leftmost = LRU,
rightmost = MRU. `get`/`put` call `move_to_end` to refresh recency and `popitem(last=False)` to
evict. The class is a thin, well-encapsulated wrapper (`_store` is private; only `get`/`put`
are public).
- **Verdict:** correct 11/11, runtime 0.262s, memory 14596 KB, loc 23.
- **All three metrics improved** vs run 1 (runtime −26%, memory −20%, loc 52→23). Promoted.
- Why it wins: `OrderedDict` is a C-level dict + intrinsic doubly-linked list. `move_to_end`
  just relinks pointers in C — no Python objects per entry, no array churn. It collapses both
  responsibilities into one optimized structure.

## Run 3 — plain `dict`, recency via delete+reinsert (memory champion, runtime-disqualified)
Python 3.7+ dicts preserve insertion order, so I tried dropping `OrderedDict` entirely:
refresh recency by `pop(key)` then reinsert; evict via `del store[next(iter(store))]`.
- **Verdict:** correct, runtime **1.953s**, memory **11339 KB**, loc 24.
- Memory dropped (~22% under run 2 — a plain dict has no linked-list overhead), but runtime
  blew up **7×**. Root cause: del+reinsert on every access leaves tombstones in the dict's
  entries array; once it fills, the dict resizes/compacts (O(n)), and this churn repeats. There
  is no C-level "move to end" for a plain dict. Only 1 of 3 metrics improved → reverted.
- Key insight: **insertion-ordered ≠ cheaply reorderable.** `OrderedDict.move_to_end` is the
  whole point.

## Run 4 — subclass `OrderedDict` (cleanest, but can't promote)
`class LRUCache(OrderedDict)`: the cache *is* its recency list, removing the `_store`
indirection and the `store =` aliases.
- **Verdict:** correct, runtime 0.287s (tie, within ±10%), memory 14596 KB (tie), loc 21.
- Only loc improved (1/3) → kept best. Also note: subclassing a builtin **leaks the full dict
  API** (`cache[k]`, `cache.move_to_end`, …), weakening encapsulation. For the OOP style the
  composition wrapper (run 2) is the more principled design, so I'm content it stayed best.

## Run 5 — `try/except` get on the subclass (regression)
Replaced the membership check with `try: move_to_end(key) except KeyError: return -1`, hoping
to save a lookup on hits.
- **Verdict:** correct, runtime **0.429s** (worse), memory 14596, loc 22. Kept best.
- Why worse: this workload is **miss-heavy** (capacity-1 caches + heavy eviction → many `get`s
  return -1). Python exception setup/teardown on the common miss path costs more than a cheap
  `in` test. EAFP loses to LBYL when the "exception" is actually frequent.

## Run 6 — subclass + `__slots__` (confirms the memory floor)
Added `__slots__ = ("_capacity",)` to drop the per-instance `__dict__`.
- **Verdict:** correct, runtime 0.273s (tie), memory **14596 KB** (unchanged), loc 22. Kept best.
- Insight: peak memory is dominated by the **stored entries and the OrderedDict's internals**
  during the graded workload, not by one instance's `__dict__`. `__slots__` saves nothing
  measurable here. This pins the memory floor for *any* OrderedDict-based design at 14596 KB.

## Why I stopped at run 6 (runs 7–10 unused)
After run 6 the design space had collapsed to a clear Pareto picture:
- **OrderedDict family** (wrapper / subclass / +slots): memory locked at 14596, runtime C-bound
  at ~0.26–0.29s (all within one tie band), differing only by ±1–2 loc.
- **Plain dict:** the only sub-14596 memory option (11339), but runtime-disqualified (1.95s).
- **DLL+Node objects:** strictly heavier (18268).
- **try/except:** strictly slower for this workload.

To *promote* over run 2 I'd need ≥2 of 3 metrics strictly better. Memory can't beat 14596
without the plain dict (which loses runtime), and runtime is C-bound so it can't be driven >10%
below 0.262 reliably — the variants only tie. No remaining idiom can clear the 2-of-3 bar, and
re-grading near-duplicate OrderedDict variants only chases runtime noise (the median-over-repeats
grader makes that futile by design). Burning runs 7–10 would add noise rows, not signal. I judged
six distinct, well-characterised data points the more valuable experimental output.

## Final answer: `best.py` = run 2 (OrderedDict composition wrapper)
- **Correct** (11/11) and the best balanced point: runtime 0.262s, memory 14596 KB, loc 23.
- It dominated the explicit-DLL baseline on all three metrics, and no later variant beat it on
  the required two-of-three.
- It is also the **best OOP fit**: composition over inheritance keeps the cache properly
  encapsulated (only `get`/`put` public, `_store` hidden), delegating the hard recency work to a
  single C-optimized structure. The pattern that emerged: *model the two responsibilities
  explicitly, then pick the one standard structure (OrderedDict) that already discharges both in
  C, and wrap—don't inherit—to preserve the interface.*
