# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | yes     | 0.941993  | 26653          | 24  | new best (first correct) |
| 2   | yes     | 1.247445  | 6837           | 42  | kept best (only memory improved; array.array reboxing slowed inner loop) |
| 3   | yes     | 0.744555  | 10106          | 41  | new best (runtime -21%, memory -62%; flat python-list CSR) |
| 4   | yes     | 0.811031  | 8957           | 44  | kept best (packed int heap: memory lower but runtime ~9% worse = tie, only 1/3) |
| 5   | yes     | 0.759212  | 10106          | 40  | kept best (zip-of-slices: loc -1 only, runtime tie, memory same; 1/3) |
| 6   | yes     | 0.727458  | 8964           | 37  | new best (memory -11%, loc -4 via packed-int heap + accumulate build; runtime tie) |
| 7   | yes     | 1.729824  | 15994          | 41  | reverted (single-int v*B+w CSR backfired: large uncached ints raise memory, div/mod slow) |
| 8   | yes     | 0.737827  | 8964           | 37  | kept best (divmod + local-bound heappush/pop: all three tie; no gain) |
| 9   | yes     | 0.711169  | 8964           | 37  | kept best (final confirmation: solution.py == best.py, run 6 version) |

Final answer: run 6 version (best.py). 1 run left unused; solution.py == best.py.
