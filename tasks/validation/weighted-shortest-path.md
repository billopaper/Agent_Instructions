# Weighted Shortest Path

## Language
Python

## Goal
Implement `shortest_path(n, edges, src, dst)` returning the minimum total weight of a path from `src` to `dst` in a weighted undirected graph, or `-1` if `dst` is unreachable.

## Rules
- Nodes are integers `0 .. n-1`.
- `edges` is a sequence of `(u, v, w)` triples: an undirected edge between `u` and `v` with integer weight `w >= 0`.
- **Multiple edges** between the same pair may appear - the usable weight is the smallest of them.
- **Self-loops** (`u == v`) may appear; they never help and can be ignored.
- Return the minimum total weight from `src` to `dst`. If `src == dst` the answer is `0`. If `dst` cannot be reached, return `-1`.
- Inputs may be **large** (thousands of nodes and edges), so an efficient algorithm is expected - the grader's runtime/memory metrics are measured on large graphs, not toy ones.

## Example
| n | edges | src | dst | result |
|---|-------|-----|-----|--------|
| 5 | `[(0,1,4),(0,2,1),(2,1,1),(1,3,1),(3,4,3)]` | 0 | 4 | 7 |
| 3 | `[(0,1,2)]` | 0 | 2 | -1 |
| 1 | `[]` | 0 | 0 | 0 |

(For `n=5`: `0→2→1→3→4` costs `1+1+1+3 = 7`, beating `0→1→3→4` = `4+1+3 = 8`.)

## Verification
Graded against a hidden test suite; you receive only a verdict (`correct`, `passed`/`total`) and metrics - never the test inputs or expected outputs. It exercises: `src == dst`, unreachable targets (`-1`), single-node and edge-less graphs, multi-edges (minimum wins), self-loops, small hand-checkable graphs, and **large graphs** where the choice of algorithm and data structures determines runtime and peak memory. The visible `Example` above is not graded.
