<!-- LAUNCH: open Claude Code (model = Haiku 4.5) with the working directory = THIS agent's task folder (agents/vanilla-haiku/val/), then paste this whole file as the first message. -->

# Vanilla Agent (Haiku 4.5)

## Instructions

- Solve the Task
- If grader runs remain after correctness, improve runtime, memory, and LOC.

## Prompt guidance

Ask the agent to design implement the solution.

## Task
Grade command (run exactly this, every time):
`Set-Location -Path "c:\Users\micha\Documents\GIT\MasterPrompt\agents\vanilla-haiku\val"; python ../../../grading/validate.py validation/weighted-shortest-path solution.py`

Spec:
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

## Workflow & confinement (hard rules)

You run inside your own task folder via Claude Code; your task is in the **Task** section above. **You get 10 tries (grader runs) for this task** - the grader enforces it: each verdict shows `runs_remaining`, and after the 10th run it refuses (exit 3). The grader returns `correct`, `passed`/`total`, `metrics` (runtime_s, peak_memory_kb, loc), `error_class`, plus `run`/`runs_remaining`. Keeping your best version and the log is YOUR job - the grader stores neither.

Loop (you have 10 runs - **use all of them**. best.py only updates on improvement, so further attempts cannot regress your best. Once correct, try different approaches/idioms/algorithms - exploration is the point of the experiment, and the verdicts populate records.md):
1. Write or edit `solution.py`.
2. Grade it by running the **grade command from the Task section above** (it already has this task's id).
3. Append one row to `records.md`: run number, correct, the three metrics, action (`new best` / `kept best` / `reverted` / `error`).
4. Maintain `best.py`:
   - The first correct solution becomes `best.py`.
   - Overwrite `best.py` with a newer correct result ONLY if it **improves at least 2 of 3 metrics**. memory and loc count as improved when strictly lower (they are exact); runtime counts as improved only when **more than 10% lower** than the current best - a runtime difference within +/-10% is a tie, neither better nor worse (the grader reports the **median** over repeats, so re-grading to chase a lucky time achieves nothing). Otherwise keep `best.py` and restore `solution.py` from it before the next try.
5. Watch `runs_remaining`. Before it hits 0, make sure `solution.py` equals `best.py` - that file is your final answer.


When done (after run 10 or whenever you stop): write `reasoning.md` in this folder summarizing the **full reasoning trail**:
- your initial approach and why;
- for each iteration: what you tried, why, what the grader returned, and whether you promoted or reverted;
- what worked, what didn't, and the key insight or pattern you converged on;
- why `best.py` is your final answer.
Be specific and honest about successes and failures - this is the experiment's raw material for distilling a master prompt.

Confinement:
- Your whole world is your own task folder. Read and write ONLY files inside it (`solution.py`, `best.py`, `records.md`). Do not explore upward.
- The grade command is the ONLY thing you may touch outside this folder. You must NOT `ls`, `cd` into, open, or inspect `grading/`, the hidden tests, reference solutions, or any parent/sibling directory - and never try to discover the expected outputs.
- Do not test or inspect your solution outside the grader in any way. No `test_*.py` or `conftest.py`. No `python -c`, no REPL `import solution`, no debug prints, no inline calls to your solution function from the shell, no "just to see what happens" runs. The grader's verdict is the **ONLY** way you verify behavior - `solution.py` is what gets graded, nothing else.
