# Records — Weighted Shortest Path (vanilla agent)

| run | correct | runtime_s | peak_memory_kb | loc | action | notes |
|-----|---------|-----------|----------------|-----|--------|-------|
| 1   | yes     | 1.646343  | 4308           | 19  | new best | CSR adjacency (array module) + Dijkstra with int-encoded heap (nd*n+v). No stale-skip. |
| 2   | yes     | 1.364072  | 4308           | 20  | kept best | Added stale-entry skip `if d > dist[u]: continue`. Runtime -17% but loc 20>19 → only 1/3 improved, not promoted. |
| 3   | yes     | 1.333492  | 4308           | 18  | new best | Stale-skip + merged imports + one-lined fill-loop body. Runtime -19% vs best AND loc 18<19 → 2/3 improved. |
| 4   | yes     | 1.370511  | 4425           | 18  | reverted | Micro-opts: local push/pop aliases + `divmod`. Runtime tie, mem 4425>4308 (divmod tuple alloc), loc tie → not better. |
| 5   | yes     | 0.933201  | 26653          | 14  | new best | Classic list-of-lists adjacency + tuple heap. Runtime -30% AND loc 14<18 → 2/3 improved. Memory 6x worse (tuples stored permanently). |
| 6   | yes     | 1.344801  | 6595           | 19  | reverted | CSR arrays + tuple heap. Runtime ties run3 → int-encoding was NOT the villain; the slow part is `array` indexing in the inner loop vs list-of-tuples iteration. Only 1/3 vs run5. |
| 7   | yes     | 1.000803  | 25504          | 14  | reverted | List adjacency + int heap. Mem only 1.1MB < run5 → the heap isn't the memory driver; the list-of-tuples adjacency (2·E tuples) is. Runtime tie, only 1/3 vs run5. |
| 8   | yes     | 2.074240  | 45745          | 19  | reverted | Pre-dedup multi-edges via dict. All 3 metrics worse — graphs aren't dup-heavy; dict overhead dominates. `nd < dist[v]` already handles multi-edges for free. |
| 9   | yes     | 0.962349  | 25504          | 13  | new best | List adjacency + int heap + walrus `:=`. vs run5: mem 25504<26653 AND loc 13<14 (runtime tie) → 2/3 improved. Dominates run5. **FINAL.** |

Run 10 unused: with 1 run left, no 2/3 improvement over run9 was identifiable (memory is bounded by the list-of-tuples adjacency; runtime near the pure-Python floor; loc-only cuts can't promote). `solution.py` == `best.py` == run9. Re-grading to chase a lucky time is pointless (grader reports the median).
