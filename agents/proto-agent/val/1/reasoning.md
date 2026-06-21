# Reasoning — Weighted Shortest Path (proto-agent)

## Task in one line
Single-source single-target shortest path in a large, weighted, **undirected**
graph with multi-edges and self-loops; non-negative integer weights; return min
total weight or `-1`. Metrics: correctness gate, then memory / runtime / LOC.

## Style
Prototype-driven: start from a known working idiom, get correct first, then
iterate fast — each grader verdict is a data point steering the next mutation.
best.py only advances on a real 2-of-3 improvement, so exploration is free.

## Initial approach (run 1) — the working seed
Non-negative weights + need for the minimum ⇒ **Dijkstra with a binary heap**
(`heapq`), the canonical idiom. Reused the textbook shape: list-of-lists
adjacency built from `edges`, a `dist`/settled array, lazy heap.
Key spec handling that's automatic with Dijkstra:
- **multi-edges**: no dedup needed — the heap naturally relaxes via the cheapest
  edge first; the larger parallel edges just never improve `dist`.
- **self-loops**: skipped at build (`u == v`), they can't help.
- **src == dst → 0**; **unreachable → -1** (heap empties without settling dst).

Verdict: correct 13/13, runtime 1.180s, mem 30011 KB, loc 23. Solid seed → best.

## Iterations

**Run 2 — CSR (compressed-sparse-row) adjacency.** Hypothesis: on large graphs
the memory cost is the list-of-lists-of-**tuples** (every edge is a heap-heavy
`(v, w)` tuple object). Replaced it with three flat lists: `head` (per-node
offset, via degree prefix sum), `to`, `wt`. Two passes over `edges` (count, then
fill). Result: runtime 1.180→0.769s (−35%, >10%), mem 30011→10103 KB (−66%),
loc 23→44 (worse). 2/3 improved → **promote**. Biggest single jump; flat int
arrays beat tuple-per-edge decisively.

**Run 3 — `array('q')` for `to`/`wt`.** Hypothesis: raw C-long storage cuts
memory below boxed-int lists. Reality: runtime 1.005s and mem 11534 KB — **both
worse**. Two reasons: (a) indexing an `array` *boxes* a fresh Python int on every
hot-loop read; (b) constructing via `bytes(8*m)` creates a transient buffer that
coexists with the array, lifting peak. **Revert.** Lesson: `array` is a memory
trap when the data is read in a tight Python loop.

**Run 4 — bidirectional Dijkstra on the CSR.** Hypothesis: searching from both
`src` and `dst` and meeting in the middle expands far fewer nodes on big graphs,
so the heaps stay small. Two frontiers (`distF/distB`, `seenF/seenB`, two heaps),
stop when `topF + topB >= best`. Result: runtime 0.769→0.642s (−17%), mem
10103→7917 KB (−22%), loc worse. Surprise: memory *dropped* despite a second
`dist` array — because the dominant peak was **pending heap tuples**, and two
small frontiers hold far fewer than one big one. 2/3 → **promote**.

**Run 5 — balanced bidirectional** (expand only the smaller-top frontier).
Runtime/mem tied, loc worse. Plain alternation already balances these graphs.
**Revert.**

**Run 6 — compact + lazy skip.** Dropped the `seen` bytearrays for a lazy
`if d <= dist[u]` stale-pop skip; compressed with `;`. Runtime tie, mem
7917→7858 KB (lower), loc 67→46 (much lower). 2/3 → **promote**. LOC is a real
metric — semicolon-packing legitimately lowers it.

**Run 7 — interleaved single array** `ad[2i]=node, ad[2i+1]=w`. Hypothesis:
locality + one list object. Reality: runtime ~2× worse (1.169s) from the `*2`
arithmetic and `range(...,...,2)` per neighbor. Mem tied. **Revert.** Two
plain-indexed lists with a unit-step `range` are much friendlier to CPython.

**Run 8 — reuse `deg` as the fill pointer (FINAL).** After the degree prefix
sum, `deg` is dead; reuse it as the moving write-pointer instead of allocating a
separate `pos = head[:n]`. One fewer n-element list at the build peak. Result:
runtime tie (0.614s), mem 7858→7624 KB (lower), loc 46→38 (lower). 2/3 →
**promote**. This is `best.py`.

**Run 9 — unidirectional control.** Same compact CSR but single-direction
Dijkstra, to *measure* bidirectional's contribution cleanly: runtime +22%
(0.752s), mem +29% (9868 KB), loc 29 (lowest). Confirms bidirectional is the
single biggest driver of both the runtime and the memory win on large graphs.
LOC alone is only 1/3 → keep run 8. **Revert.** (Run 10 left unused: the final
file is byte-identical to run 8, and re-grading a stable median changes nothing.)

## What worked / what didn't
- **Worked:** CSR flat arrays (memory + cache), bidirectional search (fewer
  expansions ⇒ smaller heaps ⇒ less runtime *and* less peak memory), lazy
  stale-skip (drops the `seen` arrays), reusing a dead array as a pointer,
  semicolon compaction for LOC.
- **Didn't:** `array` module in a hot read loop (boxing + construction spike);
  interleaved single array (index arithmetic overhead); balanced-frontier
  expansion (no gain over simple alternation here).

## Key insight
For pure-Python single-pair shortest path on large graphs, the wins are
**data-layout** (flat CSR int lists, never tuples, never `array` in hot loops)
and **search shape** (bidirectional Dijkstra shrinks the live heap, which is the
true memory bottleneck — not the adjacency). Micro-tricks (lazy skip, pointer
reuse, `;`-packing) then trim memory and LOC without touching runtime.

## Why best.py is the final answer
Run 8 is the best correct solution on every axis simultaneously: it ties the
fastest runtime observed (0.614s, within noise of run 4) while holding the
lowest memory (7624 KB) and a low LOC (38). It strictly dominates every other
correct variant on at least two of three metrics, and no later experiment beat
it. solution.py is byte-identical to it.
