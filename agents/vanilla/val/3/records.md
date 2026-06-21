# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 1.109435 | 30012 | 22 | new best (first correct) |
| 2 | yes | 1.241491 | 14069 | 37 | reverted (only memory improved; runtime +12%, loc up) |
| 3 | yes | 0.962269 | 26653 | 25 | new best (runtime -13%, memory lower; loc +3) |
| 4 | yes | 1.003156 | 9239 | 42 | reverted (memory big win 9239, but runtime tie & loc 42) |
| 5 | yes | 1.023347 | 18416 | 29 | reverted (packed-int: memory 18416 mid, runtime tie) |
| 6 | yes | 0.953810 | 26653 | 27 | reverted (local-bind ~1% faster = tie; not worth +2 loc) |
| 7 | yes | 0.512122 | 16589 | 35 | NEW BEST (dedup multi-edges: runtime -47%, memory lower) |
| 8 | yes | 0.464638 | 16595 | 29 | kept best (runtime -9.3% = tie <10%; mem equal; loc better but only 1/3) |
| 9 | yes | 0.470706 | 16595 | 31 | kept best (local-bind no help; runtime tie, only loc better) |
| 10 | yes | 0.470401 | 16589 | 35 | final confirm (solution.py == best.py, run 7 dedup-Dijkstra) |
