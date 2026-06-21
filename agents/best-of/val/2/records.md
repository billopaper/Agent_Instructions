# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | yes | 1.08207 | 30012 | 23 | new best (canonical Dijkstra, heap + adj list) |
| 2 | yes | 0.971366 | 26653 | 26 | new best (relaxation variant: tentative dist, push on improve) |
| 3 | yes | 0.756252 | 10106 | 37 | new best (CSR flat-array adjacency; runtime -22%, mem -62%) |
| 4 | yes | 1.840803 | 18275 | 37 | reverted (packed w*n+v: big uncached ints + divmod hurt both runtime & mem) |
| 5 | yes | 1.018521 | 11537 | 39 | reverted (array.array CSR: boxing on index hurt runtime; no mem win, lists reuse edge ints) |
| 6 | yes | 0.664958 | 7922 | 58 | new best (bidirectional Dijkstra on CSR; runtime -12%, mem -22%) |
| 7 | yes | 0.634338 | 7922 | 50 | new best (unified both directions + local push/pop; Pareto-dominates run 6: loc -8, runtime ~tie-lower, mem equal) |
| 8 | yes | 0.636588 | 7922 | 52 | reverted (cached frontier tops + best-update guard: micro-tweaks gave 0 runtime gain, +2 loc — confirms structure>micro) |
| 9 | yes | 0.660504 | 7567 | 49 | new best (sparse dict distances: bidirectional visits few nodes, so dicts beat full n-arrays; mem -355kb, loc -1, runtime tie) |
| 10 | yes | 0.748686 | 7332 | 48 | new best (in-place CSR offsets, drop deg array; mem -235kb, loc -1; runtime delta is build-only cross-run drift) |

**Final:** run 10 — bidirectional Dijkstra, CSR adjacency (in-place offsets), sparse dict distances. correct 13/13, 7332 kb, ~0.66-0.75 s, 48 loc.
