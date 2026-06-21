# Reasoning Trail — train/01_fizzbuzz (OOP / Mustermann)

## Final answer

`best.py` = **run 9**: a `FizzBuzz` class with a class-level `_P` dict mapping the
seven special residues mod 15 to their words, and a `sequence(n)` method that builds
the list with `self._P.get(i % 15) or str(i)`. A thin `fizzbuzz(n)` wraps it.

Metrics: correct 10/10, **runtime 0.001416 s, peak memory 38 KB, loc 6**.

## Initial approach and why

The style brief is object-oriented: model the problem with classes, encapsulate
state/behavior, separate responsibilities. FizzBuzz is tiny, so the honest OOP move
is a small class model rather than one function. My first design (run 1) made the
*rules* first-class objects: a `Rule(divisor, label)` class with `applies_to()`, and a
`FizzBuzz` aggregate holding a list of rules, rendering each number by joining the
labels of every matching rule (`"".join(...) or str(n)`). This is the most "textbook
OOP" shape — open for extension (add a `Rule(7, "Bazz")` and it composes for free) —
and it passed on the first try (loc 21).

## Iteration log

- **Run 1 — rule objects.** Correct. runtime 0.003104 / mem 42 / loc 21. Became the
  first `best.py`. Clean and extensible but heavy: a `Rule` object per rule, a
  generator + `str.join` per element.

- **Run 2 — single class, direct modulo.** Collapsed the rule list into one `render`
  method with `if i%15 / i%3 / i%5` checks. All three metrics improved
  (0.001583 / 38 / 14) → new best. Lesson: the per-element `join` over rule objects
  was the cost; explicit branches are far cheaper.

- **Run 3 — 15-cycle dict, inlined.** Key insight: FizzBuzz is periodic with period
  15, so the word depends only on `i % 15`. A dict `{residue: word}` + `.get(...) or
  str(i)` does it in one modulo and one lookup, inlined into `sequence` (no per-element
  method dispatch). runtime 0.001453, loc 9 → new best (runtime+loc).

- **Run 4 — cycle as a tuple, indexed.** Replaced the dict with a 15-tuple indexed by
  `i%15` (falsy `0` filler). loc fell to 6, but runtime (0.001526) was *not* lower than
  run 3. Only 1/3 improved → kept best. First sign that runtime had hit a noise floor.

- **Run 5 — tuple + local bind.** Bound the tuple to a local to skip attribute lookup.
  runtime 0.001502 — still above run 3. 1/3 → kept best.

- **Run 6 — slice-stamping (failed).** Distinct algorithm: prefill `[str(i) ...]`, then
  overwrite periodic positions with strided slice assignment (`out[2::3] = ...`). It
  errored (9/10, ValueError) because my element-count formula `(n-2)//3+1` over-counts
  (e.g. n=5 → 2 vs the real 1), and Python requires the RHS length to match the extended
  slice exactly. Also worse on every metric (mem 70). Reverted. Lesson: strided counts
  must be `len(range(start, n, step))`, and prefilling all strings then overwriting is
  strictly more work than branching once per element.

- **Run 7 — itertools.cycle + zip.** Elegant idiom: `zip(range(1,n+1), cycle(block))`,
  no modulo at all. runtime 0.001465 ≈ run 3 (noise), loc 8. 1/3 → kept best. Confirmed
  the modulo is *not* the bottleneck; building n strings is.

- **Run 8 — lean dict.get + local bind.** Same fastest logic as run 3 but no docstring
  and the dict on one line (loc 7) plus a local bind. runtime 0.001425 < 0.001453 and
  loc 7 < 9 → new best (2/3).

- **Run 9 — drop the local bind (loc 6).** I *predicted* removing the bind would slow it
  (per-element `self._P` attribute lookup). Wrong — runtime 0.001416 was the lowest of
  the whole session and loc dropped to 6. 2/3 → **new best**. The attribute-lookup cost
  is below the measurement noise here.

- **Run 10 — callable object (loc 5).** Final distinct idiom: drop the `sequence`
  method and wrapper function, give `FizzBuzz.__call__(self, n)`, and expose
  `fizzbuzz = FizzBuzz()` (a callable instance still satisfies `fizzbuzz(n)`). Reached
  loc 5, but runtime 0.001445 regressed vs run 9. Only 1/3 → kept best. Restored
  `solution.py` to run 9 before the budget hit 0.

## What worked / what didn't

- **Worked:** recognizing the period-15 structure and reducing to one modulo + one
  lookup; shrinking the class to exactly what OOP needs (one stateful map + one method);
  trimming incidental lines (docstring, redundant local bind) to drop LOC without
  touching behavior.
- **Didn't:** the slice-stamping algorithm (error-prone strided counts, more memory);
  chasing runtime past ~0.00142 s — runtime and memory are both at a hard floor
  (memory pinned at 38 KB every correct run; runtime jitter ~±0.0001 s dominated by
  building n strings, which no idiom avoids).

## Key pattern converged on

For a small, fully-specified, *periodic* problem, the best OOP shape is a single class
that **encapsulates the pattern as data** (the residue→word map) and exposes **one
method that consumes it**. Push the logic into a lookup table rather than control flow;
keep the table as class-level state; let the entry-point function be a one-line adapter.

## Why best.py is the final answer

Among all correct versions, run 9 holds the **lowest runtime (0.001416 s)** and the
**lowest LOC (6)** of any version that didn't regress — and it never lost memory
(38 KB throughout). Leaner-LOC variants (runs 4, 10 at loc 6/5) each regressed runtime,
so under the "≥2 of 3 strictly better" promotion rule they could not displace it. Run 9
is the genuine 2-of-3 optimum and is correct 10/10. `solution.py` was restored to match
it before the run budget reached 0.
