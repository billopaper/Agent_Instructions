# Records — 01_lru-cache (stepwise agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 40.688256 | 12444 | 22 | new best (dict + list, O(n) recency) |
| 2 | — | — | — | — | accidental duplicate launch, stopped before counting |
| 3 | true | 0.287096 | 14596 | 16 | new best (OrderedDict, O(1) recency; runtime + loc improved) |
| 4 | true | 2.030274 | 11339 | 16 | kept best (plain dict: memory better but only 1 of 3, runtime 7x worse) |
| 5 | true | 1.985647 | 11339 | 15 | new best (plain dict, merged get reinsert; memory + loc improved, 2 of 3) |
| 6 | true | 0.393584 | 20614 | 35 | kept best (manual doubly-linked list: fast but heaviest memory + most loc, 1 of 3) |
| 7 | true | 1.957371 | 11339 | 15 | kept best (re-grade of best.py; confirms stable median metrics) |

Stopped at run 7 with 3 runs in reserve. `solution.py` == `best.py` (run 5 design). No further 2-of-3 promotion reachable: memory (11339) and loc (15) are at the dict-store floor, and a runtime-only gain does not satisfy the rule.

## Design space mapped
| approach | runtime_s | mem_kb | loc | note |
|----------|-----------|--------|-----|------|
| dict + list (O(n)) | 40.69 | 12444 | 22 | brute force baseline |
| OrderedDict | 0.287 | 14596 | 16 | fastest; linked-list overhead = most memory of the O(1) dicts |
| **plain dict (FINAL)** | 1.96 | **11339** | **15** | lowest memory + lowest loc |
| manual DLL | 0.394 | 20614 | 35 | fast but heaviest memory + most loc |
