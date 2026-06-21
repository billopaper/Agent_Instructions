# Records — 01_lru-cache (Proto agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 0.308402 | 14596 | 16 | new best (OrderedDict idiom) |
| 2 | true | 1.958464 | 11339 | 18 | kept best (plain dict: mem↓ only, runtime 6× worse, loc↑) |
| 3 | true | 1.789550 | 11339 | 14 | new best (tight plain dict: mem↓ & loc↓ = 2/3) |
| 4 | true | 0.498909 | 20615 | 33 | kept best (DLL: fast-ish but mem worst, loc worst) |
| 5 | true | 1.898184 | 11339 | 16 | kept best (try/except: runtime tie — churn dominates, not lookups) |
| 6 | true | 1.783954 | 11339 |  9 | new best (golfed plain dict: Pareto-dominates loc-14 — loc↓, mem & rt tie) |
| 7 | true | 2.029727 | 11339 |  7 | kept best (one-liner __setitem__/__delitem__: loc↓ but runtime regressed ~14% — method-call overhead) |
| 8 | true | 0.271373 | 14596 | 10 | kept best (golfed OrderedDict: fastest 0.27s but mem 14596 > 11339 primary regress) |
| 9 | true | 1.759162 | 11339 | 10 | kept best (evict-before-insert: mem identical 11339 — eviction timing irrelevant to peak mem) |
| 10 | true | 1.779659 | 11339 |  9 | final confirm (== best.py) |

**Final answer = best.py** (run 6 / re-confirmed run 10): plain-dict LRU, mem **11339 kb (optimal)**, runtime 1.78 s, loc 9.
