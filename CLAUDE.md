# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **scaffold for a multi-agent programming experiment**, not an application. The same set of programming challenges is to be solved independently by several agents, each constrained to a different programming style. Solutions are then scored on correctness and on memory/runtime/lines-of-code. As of now the repo contains only specifications (Markdown) and configuration (JSON) — there is no source code, build system, test runner, or git history yet. Implementation files (`prompt-template.md`, `solution/`, `tests/`, `notes/` per agent) are described in the specs but have not been created.

## The experiment model

**The real objective is prompt distillation.** Five style-agents solve the *training* tasks; for each task a winner is chosen; the winners' plans are distilled into one **master prompt**; that prompt is then tested in-distribution (the train tasks) and out-of-distribution (a held-out validation task no agent saw). The end product is the master prompt — hence the repo name.

`experiment-config.json` is the single source of truth that ties everything together. It declares:
- `agentCount: 5` × `trainTaskCount: 3` (+ a `00_fizzbuzz` control and `validationTaskCount: 1` held out) — every agent solves every train task. (Plus two extra agents outside the styled five: `vanilla` = no-instructions control, `best-of` = distilled prompt.)
- `runLimit: 10` with `failureIfRunsExhausted: true` — each agent gets 10 grader runs per task (solve + optimize combined). **The grader enforces it**: it keeps a per-solution counter in `grading/.runstate/` and refuses (exit 3) after the 10th run. The agent is also told "10 tries" in its prompt and sees `runs_remaining` each verdict. Not correct within 10 = failure. (Replaced the old token budget, which a subscription's CLI can't measure anyway.)
- `promotionRule` — the **agent** promotes a new correct result to its `best.py` only if ≥2 of 3 metrics improve (strictly lower); no 2× guard.
- `measureRepeats: 5` — once a solution is correct, the grader runs it this many times and reports **min** runtime and **min** peak memory (de-noising). `loc` is read once from source. Repeats are internal — they don't consume the run budget.
- `temperature: 0.92` — intentionally high so agents diverge instead of converging on the same solution.
- `grading` — all tasks are scored by an **external CLI grader** with hidden tests (`grading/README.md`); agents never see test inputs/expected outputs, only `correct` + metrics. The visible `Example` in each task is *not* graded.
- `metrics`: `correctness` (pass/fail gate), then `memory`, `runtime`, `lines_of_code`.
- `phases`: `solve → verify → optimize → meta-plan` (per agent/task), then `extract-master-prompt → eval-master-train → eval-master-validation` (experiment-level). These describe the intended process; runs are currently driven manually in console mode.

The phase contract: an agent must pass correctness in **solve/verify** first. Only after correctness, and only if grader runs remain (`optimizeWithRemainingRuns: true`), does it enter **optimize** to improve memory/runtime/LOC — re-running the grader after each change. **meta-plan** records the winner's *plan* (approach, decisions, edge cases) as the raw material for distillation.

## Cross-file mappings (important — names differ across files)

The five styles thread through three places with **non-matching identifiers**. When wiring agents to config, reconcile these:

| config `styles` key | agent folder        | `agentAliases` name |
|---------------------|---------------------|---------------------|
| `stepwise`          | `agents/stepwise-agent/` | Wirth          |
| `functional`        | `agents/functional-agent/` | Opa          |
| `oop`               | `agents/oop-agent/` | Mustermann          |
| `smart-pattern`     | `agents/smart-agent/` | Einstein          |
| `prototype-driven`  | `agents/proto-agent/` | Proto             |

Each style's methodology and prompt guidance lives in `agent-styles.md` and is restated per-agent in `agents/<name>/README.md`.

## Tasks

All tasks are **Python**, split into `tasks/Train/` (seen by agents) and `tasks/Validation/` (held out for the generalization test — never run base agents on it). Per-task difficulty lives under `tasks` in `experiment-config.json`.

**Control task** (`tasks/train/00_fizzbuzz`): trivial; checks the convergence assumption, not scored as a real task.

| task | difficulty | entry point |
|------|------------|-------------|
| 00 fizzbuzz | easy (control) | `fizzbuzz(n)` |

**Train set** (`tasks/train/`, the 3 scored tasks — inputs are scaled so memory/runtime are real metrics):

| task | difficulty | entry point |
|------|------------|-------------|
| 01 lru-cache | medium | `LRUCache(capacity).get/put` |
| 02 expression-evaluator | medium-hard | `evaluate(expr)` |
| 03 sudoku-solver | hard | `solve(board)` |

**Validation set** (`tasks/validation/`, held out — folder `val`):

| task | difficulty | entry point |
|------|------------|-------------|
| weighted-shortest-path | hard | `shortest_path(n, edges, src, dst)` |

Each task file follows the same shape: **Language → Goal → Rules → Example → Verification**. Rules are the spec; the `Example` is illustrative only (not graded); `Verification` points at the external endpoint and lists the *categories* the hidden suite covers. Treat Rules + Verification categories as the acceptance criteria.

## Grading layer (`grading/`)

`grading/` is the **hidden answer key — no agent may read it** (see its own README). It holds the CLI grader and per-task suites; it must stay outside every agent sandbox.

- `grading/validate.py` — CLI: `python grading/validate.py <task_id> <solution.py>`. Prints one JSON verdict (`correct`, `passed`/`total`, `metrics`, `error_class`, `run`, `runs_remaining`) and exits `0`/`1`/`2`/`3`. Its only state is a per-solution run counter in `grading/.runstate/` that enforces `runLimit`. `task_id` is case-insensitive. New tasks register in the `SUITES` dict.
- `grading/suites/<task>.py` — each exposes `reference(case)` (trusted oracle), `CASES` (hidden inputs), and `run(candidate, case)` (call adapter). **Only FizzBuzz is implemented so far**; the other 6 tasks are not yet built.

The grader returns counts + a failure *category* only — never the failing input, expected output, or produced output. An agent **may run** it but never reads the suites. Its only state is the run counter (enforces the 10-run cap). Everything else lives in the agent's own folder: `best.py` (best correct version), `records.md` (per-run log), and `reasoning.md` (the full reasoning trail written at the end, raw material for master-prompt distillation).

## How a run works (console mode)

There is no automated orchestrator — **you** are the driver. For each agent, fill the `## Task` section of `agents/<agent>/behaviour.md` (set the task id in the grade command, paste the task spec), launch a Claude Code session with the agent's task folder as the working directory (e.g. `agents/stepwise-agent/00_fizzbuzz/`), and paste the whole `behaviour.md` as the first message. The agent loops (≤10 runs, grader-enforced): edit `solution.py` → run the grader → log the run in `records.md` → keep `best.py` per the promotion rule. It restores `best.py` into `solution.py` before its runs run out. Ranking/winner-selection and master-prompt distillation are done manually afterward.

## Agent sandbox layout (`agents/<style>-agent/`)

- `behaviour.md` — style + prompt constraints + workflow/confinement rules.
- one **folder per task** (e.g. `00_fizzbuzz/`) containing `solution.py` and `.claude/settings.json` (the task folder is the agent's cwd / sandbox).

Confinement: the agent's whole world is its **task folder** — it reads/writes only there. It **may run** the grader (`python ../../../grading/validate.py <task_id> solution.py`) but does **not** read `grading/`, the hidden tests, or other agents. The task + style reach it via the pasted launch prompt (it does not read `tasks/` or `behaviour.md` from disk). Enforcement: `<task>/.claude/settings.json` denies the file tools from leaving the folder and from reading `grading/`, while allowing `python`. Tool denies don't bind a raw shell — for a hardened run, launch agents under a separate OS account or container that cannot read `grading/`. Folders `00_fizzbuzz/`, `01_lru-cache/`, `02_expression-evaluator/`, `03_sudoku-solver/`, and `val/` exist per agent.

## Schemas

`experiment-config.json` is the experiment's configured model (counts, run limit, metrics, task split, phases). There is no separate schema file; result shape is ad hoc per run.

## Open decisions

Unresolved: the language/difficulty balance, whether each agent folder becomes a separate git repo or stays a logical sandbox, and building the remaining 6 grading suites + agent task folders (only FizzBuzz exists end-to-end). The `agent-styles.md` "X = 45<" discrepancy is fixed (now `X = 5`).
