# Records — 01 LRU Cache (functional agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 0.283633 | 14596 | 16 | new best (OrderedDict, canonical O(1)) |
| 2 | yes | 1.968579 | 11339 | 15 | new best (plain dict; mem & loc improved, runtime ~7x worse) |
| 3 | yes | 1.789190 | 11339 | 13 | new best (declarative pop/get; weakly dominates run 2: loc 13<15, mem equal, runtime ~9% lower=tie) |
| 4 | yes | 0.556676 | 24595 | 27 | kept best (timestamp+lazy-heap; faster but worst memory & loc) |
| 5 | no  | 30.032963 (timeout) | 7525 | 15 | error/reverted (rebuild-on-evict compaction; TLE, but shows compact-dict memory floor ~7525) |
| 6 | yes | 1.879779 | 11339 | 13 | kept best (confirmation re-grade of run 3; solution.py == best.py) |
| 7 | yes | 0.499818 | 20615 | 35 | kept best (manual doubly-linked-list + dict; fast but heavy & verbose) |

**Stopped at run 7 (3 runs unused).** Design space mapped (dict / OrderedDict / DLL / heap / compaction). Run 3 is provably unbeatable under the ≥2-of-3 promotion rule: lowering memory below 11339 needs compaction (TLE); faster runtime needs a heavier structure (raises memory) — no variant improves 2 of 3 over run 3. Final answer = run 3.

## Final answer (best.py)
Plain-dict LRU, declarative `pop`/`get`: **correct 11/11, runtime ~1.8s, peak memory 11339 KB, loc 13.** Wins the priority metric (memory) and loc; trades runtime, which the metric ordering (memory > runtime > loc) deprioritizes.
