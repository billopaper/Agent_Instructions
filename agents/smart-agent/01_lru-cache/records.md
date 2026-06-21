# Records — 01_lru-cache (smart-pattern agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 0.308847 | 14596 | 16 | new best — OrderedDict (move_to_end / popitem) |
| 2 | true | 1.745506 | 11339 | 15 | new best — plain dict (pop/reinsert); memory+loc improved (2/3), runtime regressed ~5.6x (tombstone compaction) |
| 3 | true | 0.391158 | 20614 | 36 | kept best — DLL+hashmap (list-nodes); fast but memory+loc worst (1/3 improved) |
| 4 | true | 0.298561 | 14596 | 16 | kept best — OrderedDict subclass (multi-line); only runtime improved (1/3) |
| 5 | true | 0.295550 | 14596 | 13 | new best — OrderedDict subclass (terse one-line bodies); runtime+loc improved (2/3) |
| 6 | true | 1.759165 | 11339 | 12 | new best — dict subclass (terse, no import); memory+loc improved (2/3); memory is top-priority metric |
| 7 | true | 1.730662 | 11339 | 11 | kept best — dict subclass minus no-op super().__init__(); strict Pareto improvement over run6 but only loc strictly improved (mem/runtime tie) → 2/3 rule blocks promotion |
