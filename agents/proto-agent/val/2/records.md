# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 1.014385 | 26653 | 25 | new best (heapq Dijkstra, adjacency list) |
| 2 | true | 1.221283 | 6837 | 38 | kept best (CSR arrays: mem -74% but runtime +20%, loc +13 → only 1/3) |
| 3 | true | 1.396770 | 6713 | 36 | kept best (CSR + zip(slice) iter: slicing alloc made runtime worse, 1.40) |
| 4 | true | 0.959750 | 25504 | 27 | kept best (int-encoded heap nd*n+v: mem -1149, runtime tie -5%, loc +2 → 1/3) |
| 5 | true | 0.961493 | 25504 | 24 | new best (run 4 golfed to 24 loc: mem improved + loc improved → 2/3) |
| 6 | true | 1.294017 | 4425 | 34 | kept best (CSR + int-heap = memory-optimal corner 4425 KB, but runtime +35%, loc +10 → 1/3) |
| 7 | true | 0.418006 | 8966 | 25 | new best (flat interleaved list [v,w,...] + int-heap: runtime -56% AND mem -65%, loc +1 → 2/3!) |
| 8 | true | 0.440789 | 8966 | 25 | kept best (zip(it,it) pairwise iter ≈ range-index, runtime tie, mem/loc tie → 0/3) |
| 9 | true | 0.499156 | 8981 | 24 | kept best (build via `adj[u]+=(v,w)`: loc 24 but temp tuples made runtime +19% & mem worse → 1/3) |
| - | - | - | - | - | restored solution.py = best.py (run 7); 1 run left unused (no 2/3 move remains) |
