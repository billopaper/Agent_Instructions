# Run Log — 01_lru-cache (OOP agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.352639  | 18268          | 52  | new best (DLL + hashmap, explicit _Node class) |
| 2   | true    | 0.262171  | 14596          | 23  | new best (OrderedDict wrapper; all 3 metrics improved) |
| 3   | true    | 1.952845  | 11339          | 24  | reverted (plain dict del+reinsert; mem down but runtime 7x worse, only 1/3 improved) |
| 4   | true    | 0.286793  | 14596          | 21  | kept best (subclass OrderedDict; loc down but mem tie, runtime tie -> 1/3) |
| 5   | true    | 0.429335  | 14596          | 22  | kept best (subclass + try/except get; runtime worse - miss-heavy workload penalizes exceptions) |
| 6   | true    | 0.273483  | 14596          | 22  | kept best (subclass + __slots__; mem unchanged - entries dominate peak, not instance __dict__; 1/3) |

Stopped exploring after run 6 (runs 7-10 left unused). Rationale: the meaningfully distinct
approaches were all measured (DLL+Node, OrderedDict wrapper, OrderedDict subclass, subclass+__slots__,
try/except get, plain dict). Every OrderedDict variant ties on the two pinned metrics (memory 14596,
runtime ~C-bound) and varies only +/-1-2 loc; the only sub-14596 memory option (plain dict) is
runtime-disqualified. No remaining variant can improve 2 of 3 metrics over run 2, and re-grading
near-duplicates only chases runtime noise (which the rules discourage). Final best = run 2.
