# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.024126 | 26653 | 25 | new best (Dijkstra, list-of-lists adjacency) |
| 2 | true | 0.811820 | 9871 | 35 | new best (CSR flat-array adjacency; runtime -21%, mem -63%, loc +10) |
| 3 | true | 0.897639 | 8723 | 38 | reverted (int-packed heap: mem -12% but runtime +10%, loc +3; only 1/3 improved) |
| 4 | true | 1.430977 | 7972 | 39 | reverted (array module: mem -19% but runtime +76% from boxing, loc +4; only 1/3) |
| 5 | true | 0.831204 | 9871 | 36 | reverted (local-bound push/pop: runtime tie, mem same, loc +1; no improvement) |
| 6 | true | 0.747393 | 7753 | 54 | reverted (bidirectional Dijkstra: mem -21% improved, runtime -8% (TIE, <10%), loc +19; only 1/3) |
| 7 | true | 0.748122 | 7747 | 62 | reverted (bidir, expand smaller frontier: same as run 6; build cost is the runtime floor) |
| 8 | true | 0.886721 | 8723 | 28 | new best then superseded (compact int-packed-heap CSR; mem -12% and loc -20% both improved = 2/3; runtime worse) |
| 9 | true | 0.733091 | 7753 | 54 | new best then superseded (bidirectional re-grade; vs run 8: runtime -17% and mem -11% = 2/3) |
| 10 | true | 0.774312 | 7669 | 43 | NEW BEST / FINAL (int-packed bidirectional; vs run 9: mem -1% and loc -20% improved, runtime +6% TIE = 2/3) |
