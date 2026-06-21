# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.003403 | 26653 | 24 | new best (lazy Dijkstra, heapq, list-of-lists adj) |
| 2 | true | 0.977338 | 25504 | 29 | kept best (int-packed heap key d*n+u; mem -4%, runtime tie <10%, loc worse → only 1/3) |
| 3 | true | 1.087744 | 7771 | 41 | kept best (CSR arrays: mem -71%! but runtime tie, loc 41 → only 1/3 improved) |
| 4 | true | 0.941842 | 26654 | 21 | kept best (drop u!=v + src==dst checks; loc 21 but runtime -6% tie, mem tie → 1/3) |
| 5 | true | 1.471868 | 6526 | 36 | kept best (single packed-array CSR: mem floor 6526 but decode +47% runtime → 1/3) |
| 6 | true | 0.923223 | 26654 | 23 | kept best (lean build + aliased push/pop; runtime -8% TIE (need >10%), loc 23 → 1/3) |
| 7 | true | 1.088696 | 26655 | 22 | kept best (no early-exit, full SSSP: +18% vs run-6 → early-exit worth ~15% runtime) |
| 8 | true | 0.857305 | 24477 | 40 | new best (bidirectional Dijkstra strict-alternation: runtime -14.6% >10% AND mem<26653 → 2/3) |
| 9 | true | 0.984629 | 24470 | 31 | NEW BEST (smaller-frontier bidir: mem 24470<24477 + loc 31<40 → 2/3; runtime +15% regressed — rule has no anti-regression guard, memory is primary metric) |
| 10 | true | 0.926837 | 7381 | 43 | kept best (bidir + CSR: mem -70% (7381) AND runtime -6% vs run-9, but runtime within 10% tol = TIE, loc 43 worse → only 1/3. NOTE: dominates run-9 on the two top-priority metrics; flagged for manual winner selection) |

**Final answer: best.py = run-9 (smaller-frontier bidirectional Dijkstra).**
Caveat for the experimenter: run-10 (bidir + CSR) is arguably the better solution — it beats run-9 on memory (−70%, the primary metric) and runtime (−6%), losing only on LOC. The 2/3 promotion heuristic blocked it because the runtime gain landed inside the ±10% tolerance (tie) and LOC regressed. If the final scoring is memory-weighted, prefer run-10.
