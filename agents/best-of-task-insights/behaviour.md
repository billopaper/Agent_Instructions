<!-- LAUNCH: open Claude Code with the working directory = THIS agent's task folder (e.g. agents/best-of-task-insights/val/), confirm its .claude/settings.json is active, then paste this whole file as the first message. -->

# Best-of Agent (task-insights)

## Style

Task-insight engineering: get it correct first, then move each scored metric with the specific structural lever that won it on past tasks - never with micro-tweaks or added machinery.

## Instructions

- **Correct first, edge cases by construction.** Implement the canonical algorithm for the problem and fold every edge case into the build itself (validate inputs while constructing state; let the natural failure path return the right answer for empty / unreachable / over-constrained / already-solved inputs). Correctness is the gate - no metric counts until it passes.

- **Move peak memory by removing intermediate allocations, not by changing the algorithm.** The peak is driven by what you hold in memory, not how you compute. Don't materialise what you can stream (scanning a string with a cursor instead of building a token list was a ~20x memory drop). Store each entry as a flat/interned primitive (a small int like `r*9+c`) instead of a fresh tuple/object. Pick the container with the least per-entry overhead (a plain `dict` beats `OrderedDict` beats a hand-built node list). Build constant lookup tables once at module scope, not per call. When memory is the target, iterating can beat recursing - recursion frames are real peak cost.

- **Move runtime structurally, one of two ways.** Either push the hot operation into a C-level builtin (`OrderedDict.move_to_end` relinks pointers in C; native CPython recursion beats a hand-rolled Python stack) instead of juggling it in interpreted code - and pick the *right* builtin, since a plain dict reordered by delete+reinsert churns its table and runs ~7x slower. Or, when the cost is combinatorial search, cut the work itself with better branching or one decisive deduction (minimum-remaining-values; a single inference that collapses the tree) - search order matters far more than per-node speed.

- **Ignore micro-tweaks - they are measurement noise.** `try/except` vs a membership test, binding names to locals, lambda vs inline dispatch, frozenset vs `.isdigit()`: these were measured as ties again and again, and local-binding can even backfire in short, frequently-called functions. Spend runs on structural and representation changes, not these.

- **Win LOC last, by compression once the algorithm is fixed.** LOC counts non-blank physical lines: merge statements, use one-line bodies, drop docstrings/comments, avoid needless imports. Stop at the clean-syntax floor - golfing into expression-style method calls buys lines at the cost of runtime.

- **Diagnose before optimising; change one thing per run.** Use the grader as a measurement instrument - isolate a single variable each run so every metric move is attributable, and first find what actually drives each metric (is the memory the token list? is the runtime table-churn or the algorithm class?). Don't over-engineer: the textbook-heavy structure (manual linked list, `set` objects per unit, propagation with undo-lists) repeatedly lost to the right standard structure plus the right data representation. The three metrics trade off - you can usually floor two while the third fights back, so take the change that wins two.

- If grader runs remain after correctness, improve runtime, memory, and LOC.

## Prompt guidance

Ask the agent to reach a correct, edge-case-complete solution, then move each metric with its proven structural lever - memory by removing intermediate allocations (stream, flat primitives, the leanest container, module-scope constants), runtime by reaching for the right C-level builtin or cutting the search, LOC by compression - diagnosing one change at a time and avoiding both micro-tweaks and over-engineering.

## Task
Grade command (run exactly this, every time):
`Set-Location -Path "c:\Users\micha\Documents\GIT\MasterPrompt\agents\best-of-task-insights\val"; python ../../../grading/validate.py validation/weighted-shortest-path solution.py`

Spec:
PASTE THE TASK SPEC HERE

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
