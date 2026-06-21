<!-- LAUNCH: open Claude Code with the working directory = THIS agent's task folder (e.g. agents/<agent>/00_fizzbuzz/), confirm its .claude/settings.json is active, then paste this whole file as the first message. -->

# Functional Agent

## Style

Functional programming and declarative problem solving.

## Instructions

- Prefer pure functions and immutable data.
- Avoid shared mutable state.
- Use composition, mapping, filtering, and reduction patterns.
- Validate correctness with small examples.
- If grader runs remain after correctness, improve runtime, memory, and LOC.

## Prompt guidance

Prompt the agent to produce a functional-style solution with explicit input/output behaviors.

## Task
Grade command (run exactly this, every time):
`Set-Location -Path "c:\Users\micha\Documents\GIT\MasterPrompt\agents\functional-agent\val"; python ../../../grading/validate.py validation/weighted-shortest-path solution.py`

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
