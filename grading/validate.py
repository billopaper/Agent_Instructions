#!/usr/bin/env python3
"""External CLI grader. Grades a candidate against a task's HIDDEN suite and
prints one JSON verdict to stdout.

The ONLY state it keeps is a per-solution RUN COUNT, so the run budget is
hard-enforced (the agent cannot exceed it). Everything else — keeping the best
version (`best.py`) and the run log (`records.md`) — is the agent's job.

Usage:
    python grading/validate.py <task_id> <path-to-solution.py>

Exit codes: 0 = correct, 1 = not correct, 2 = invalid invocation, 3 = run budget spent.

The verdict never reveals test inputs/expected outputs. This file and everything
under grading/ is the answer key — it must live OUTSIDE every agent sandbox.
"""
import sys
import gc
import json
import time
import hashlib
import threading
import tracemalloc
import importlib
import importlib.util
import statistics
from pathlib import Path

# task_id -> module name under grading/suites/
SUITES = {
    "train/00_fizzbuzz": "fizzbuzz",
    "train/01_lru-cache": "lru_cache",
    "train/02_expression-evaluator": "expression_evaluator",
    "train/03_sudoku-solver": "sudoku_solver",
    "validation/weighted-shortest-path": "weighted_shortest_path",
}

GRADING_DIR = Path(__file__).resolve().parent
REPO = GRADING_DIR.parent
sys.path.insert(0, str(GRADING_DIR))
sys.dont_write_bytecode = True  # don't drop __pycache__ into the agent's folder


def _cfg(key, default):
    try:
        return json.loads((REPO / "experiment-config.json").read_text(encoding="utf-8")).get(key, default)
    except Exception:  # noqa: BLE001
        return default


def _run_limit() -> int:
    return int(_cfg("runLimit", 10))


def _measure_repeats() -> int:
    return max(1, int(_cfg("measureRepeats", 5)))


def _case_timeout() -> float:
    return float(_cfg("caseTimeoutSeconds", 5))


def _runtime_tolerance_pct() -> float:
    return float(_cfg("runtimeTolerancePct", 10))


def _call_with_timeout(fn, *args, timeout):
    """Run fn(*args); raise TimeoutError if it doesn't finish in `timeout` seconds.

    Uses a daemon thread (cross-platform, no SIGALRM). A timed-out candidate
    keeps running in a background thread until the grader process exits - we
    can't forcibly kill a Python thread - but since validate.py exits after one
    grading invocation, the zombie thread dies with the process.
    """
    result = [None]
    error = [None]

    def _target():
        try:
            result[0] = fn(*args)
        except BaseException as exc:  # noqa: BLE001 — capture and re-raise on main
            error[0] = exc

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        raise TimeoutError(f"case timed out after {timeout}s")
    if error[0] is not None:
        raise error[0]
    return result[0]


def _one_pass(suite, candidate, expected):
    """Run the whole suite once; return (passed, error_class, runtime_s, peak_bytes).

    Each case is wrapped in a per-case wall-clock timeout (caseTimeoutSeconds).
    On the first timeout we bail — a candidate that hangs is broken, and there's
    no point sinking the budget into more timed-out cases or skewed metrics.
    """
    timeout = _case_timeout()
    passed = 0
    error_class = None
    # Disable GC during the timed pass so collection pauses don't jitter the runtime
    # metric (allocation-heavy solutions - linked lists, constraint propagation - are
    # otherwise dominated by GC noise). Non-cyclic garbage is still freed by refcounting,
    # so peak memory is essentially unaffected. Always restored in finally.
    gc.collect()
    gc.disable()
    tracemalloc.start()
    start = time.perf_counter()
    try:
        for case, want in zip(suite.CASES, expected):
            try:
                got = _call_with_timeout(suite.run, candidate, case, timeout=timeout)
            except TimeoutError:
                error_class = "TimeoutError"
                break  # abort the pass — broken candidate
            except Exception as exc:  # noqa: BLE001
                if error_class is None:
                    error_class = type(exc).__name__
                continue
            if got == want:
                passed += 1
            elif error_class is None:
                error_class = "AssertionError"
        runtime = time.perf_counter() - start
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
        gc.enable()
    return passed, error_class, runtime, peak


def _count_path(task_id: str, solution: Path) -> Path:
    """One small counter file per (agent, task). The ONLY state the grader keeps.

    Filename is human-readable: `<agent>__<task_id>.count` (e.g.
    `stepwise-agent__train_01_fizzbuzz.count`). Agent is inferred from the solution
    path's grandparent dir (agents/<agent>/<task-folder>/solution.py); task_id is
    sanitized for filenames (`/` -> `_`). A short hash is appended only if the
    inferred agent doesn't look like a real agent folder, to keep ad-hoc test
    invocations collision-free.
    """
    sol = solution.resolve()
    safe_tid = task_id.replace("/", "_").replace("\\", "_")
    parts = sol.parts
    # Standard layout is agents/<agent>/<task-folder>/solution.py. A deeper nesting
    # such as agents/<agent>/<task-folder>/<rep>/solution.py (repeated runs of the
    # same task) gets a "__<rep>" suffix so each repetition keeps an INDEPENDENT
    # counter, while the 2-level layout is unchanged (backward compatible).
    if "agents" in parts:
        sub = parts[parts.index("agents") + 1:-1]   # (<agent>, <task>[, <rep>...])
        agent = sub[0] if sub else sol.parent.parent.name
        nest = "_".join(sub[2:])                     # nesting beyond agent/task
        label = f"{agent}__{safe_tid}" + (f"__{nest}" if nest else "")
    else:
        # Unusual invocation: hash the full path so it can't collide with a real run.
        h = hashlib.sha1(str(sol).encode("utf-8")).hexdigest()[:8]
        label = f"{sol.parent.parent.name}__{safe_tid}__{h}"
    d = GRADING_DIR / ".runstate"
    d.mkdir(exist_ok=True)
    return d / f"{label}.count"


def _fail(msg, code=2):
    print(json.dumps({"error": msg}))
    sys.exit(code)


def _loc(path: Path) -> int:
    """Lines of code: non-blank source lines."""
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def _load_candidate(path: Path):
    spec = importlib.util.spec_from_file_location("candidate", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # may raise — caller handles
    return module


def main(argv):
    if len(argv) != 3:
        _fail("usage: validate <task_id> <path-to-solution.py>")
    task_id, sol_path = argv[1].strip().lower(), Path(argv[2])

    if task_id not in SUITES:
        _fail(f"unknown task_id '{task_id}'; known: {sorted(SUITES)}")
    if not sol_path.is_file():
        _fail(f"solution file not found: {sol_path}")

    limit = _run_limit()
    count_path = _count_path(task_id, sol_path)
    count = int(count_path.read_text()) if count_path.is_file() else 0

    # Hard cap: once the budget is spent, refuse regardless of what the agent does.
    if count >= limit:
        print(json.dumps({"status": "run_budget_spent", "runs": count, "limit": limit}))
        sys.exit(3)

    count += 1
    count_path.write_text(str(count), encoding="utf-8")

    suite = importlib.import_module(f"suites.{SUITES[task_id]}")
    total = len(suite.CASES)

    # Loading the candidate is itself an attempt (syntax/import error counts as a run).
    try:
        candidate = _load_candidate(sol_path)
    except Exception as exc:  # noqa: BLE001 — report category only
        print(json.dumps({
            "correct": False, "passed": 0, "total": total, "metrics": None,
            "error_class": type(exc).__name__, "run": count, "runs_remaining": limit - count,
        }))
        sys.exit(1)

    expected = [suite.reference(case) for case in suite.CASES]   # untimed, deterministic
    loc = _loc(sol_path)                                          # static, measured once

    # Correctness gate (first pass). Only if correct do we repeat to de-noise
    # runtime/memory; one validate call still counts as a single run regardless.
    passed, error_class, rt0, pk0 = _one_pass(suite, candidate, expected)
    correct = passed == total
    runtimes, peaks = [rt0], [pk0]
    if correct:
        for _ in range(_measure_repeats() - 1):
            p, e, rt, pk = _one_pass(suite, candidate, expected)
            if p != total:                       # not reliably correct
                correct, passed, error_class = False, p, e or "AssertionError"
                break
            runtimes.append(rt)
            peaks.append(pk)

    # runtime_s = MEDIAN over repeats (a stable central value; unlike min it can't be
    # gamed by re-grading to catch a lucky low sample). rel_spread exposes the noise so
    # a comparison can ignore differences inside it. peak_memory = min (low-noise floor).
    runtime_med = statistics.median(runtimes)
    rel_spread = (max(runtimes) - min(runtimes)) / runtime_med if runtime_med else 0.0
    peak_best = min(peaks)

    print(json.dumps({
        "correct": correct,
        "passed": passed,
        "total": total,
        "metrics": {"runtime_s": round(runtime_med, 6), "peak_memory_kb": peak_best // 1024, "loc": loc},
        "runtime_rel_spread": round(rel_spread, 3),
        "runtime_tolerance_pct": _runtime_tolerance_pct(),
        "error_class": None if correct else error_class,
        "run": count,
        "runs_remaining": limit - count,
    }))
    sys.exit(0 if correct else 1)


if __name__ == "__main__":
    main(sys.argv)
