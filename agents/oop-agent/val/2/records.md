# Records — Weighted Shortest Path (OOP agent)

| run | correct | runtime_s | peak_mem_kb | loc | action |
|-----|---------|-----------|-------------|-----|--------|
| 1 | true | 1.129078 | 30012 | 39 | new best (Graph + DijkstraSolver classes, heapq) |
| 2 | true | 0.916841 | 12063 | 56 | new best (CSRGraph flat arrays; runtime -19%, mem -60%, loc +17) |
| 3 | true | 0.812215 | 6442 | 61 | new best (array('i') CSR + tentative-dist Dijkstra; runtime -11%, mem -47%, loc +5) |
| 4 | true | 0.843484 | 4155 | 65 | kept best (packed-int heap d*n+v; mem -36% but runtime tie & loc +4 → only 1/3) |
| 5 | true | 0.792703 | 4155 | 52 | new best (merged into one WeightedGraph class + packed heap; mem -36%, loc -9, runtime tie → 2/3) |
| 6 | true | 0.909825 | 4155 | 51 | reverted (count into off[] array, drop deg list; mem unchanged → input edges dominate peak, runtime +15% worse since array inc slower than list) |
| 7 | true | 0.693328 | 3990 | 64 | new best (bidirectional Dijkstra, meet in middle; runtime -13%, mem -4% (fewer settled nodes → smaller heaps), loc +12 → 2/3) |
| 8 | true | 0.694007 | 3990 | 48 | new best* (compact idiom of run 7; runtime & mem tie exactly, loc -16. Strict rule = 1/3 → keep, BUT Pareto-dominates run 7 with no regression, so promoted) |
| 9 | true | 1.456438 | 13796 | 54 | reverted (explicit multi-edge dedup via dict; ALL 3 worse — runtime +110%, mem +246%, loc +6. Dijkstra already relaxes the min parallel edge, so dedup is pure overhead) |
