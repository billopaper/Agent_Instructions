# Reasoning trail — 01 FizzBuzz (stepwise / Wirth agent)

## Final answer

```python
def fizzbuzz(n, _P=("FizzBuzz", "", "", "Fizz", "", "Buzz", "Fizz", "", "", "Fizz", "Buzz", "", "Fizz", "", "")):
    return [_P[i % 15] or str(i) for i in range(1, n + 1)]
```

Metrics at promotion (run 4): correct 10/10, runtime 0.001407 s, peak memory 38 KB, loc 2.

## Initial approach and why

Stepwise refinement says: start with the simplest *correct* thing, clarity over cleverness, then
introduce exactly one change per iteration with correctness as the top priority. So run 1 was the
textbook explicit `if/elif` over `i % 3` / `i % 5`, appending to a list. It passed 10/10 immediately
(runtime 0.001754 s, mem 38 KB, loc 12) and became `best.py`. Establishing a correct baseline first
meant every later step was pure optimization against a known-good reference, never a correctness gamble.

## Iteration-by-iteration

- **Run 1 — baseline if/elif loop.** Correct. `new best`. Purpose: lock in correctness.
- **Run 2 — collapse to a list comprehension with `i % 15`.** One change: structure. loc 12→2 (big),
  but runtime measured slightly *worse* (0.00194) and memory tied. Promotion rule needs ≥2 of 3 metrics
  strictly lower; only loc moved → `kept best`. First sign that **memory is pinned at 38 KB** and
  **runtime is noisy**.
- **Run 3 — single-modulo lookup table (`_P[i % 15] or str(i)`), tuple as a module global.** One change:
  replace three modulo/branch tests with one modulo + one index. Runtime 0.001815 (~tied), loc 3, mem 38.
  Still only loc-ish improvement vs the loc-12 baseline but runtime didn't clear the bar → `kept best`.
- **Run 4 — move the lookup tuple into a default argument (`_P=(...)`).** One focused change: a default
  arg is a *local* inside the function, and local lookups are faster than globals in CPython, especially
  inside a tight comprehension. Runtime dropped to 0.001407 (< 0.001754) **and** loc 2 (< 12): 2 of 3
  strictly improved → **`new best`**. This is the winner.
- **Run 5 — collapse to a `lambda` bound to the name (loc 1).** loc 1 < 2, but runtime regressed to
  0.002009 and the body is identical to run 4, so any "win" would be pure noise. Only 1 of 3 → `kept best`.
  Also stylistically against Wirth/PEP8 (named `def` preferred over lambda-to-name).
- **Run 6 — modulo-free `zip(range(...), cycle(_P))`.** Tests whether the modulo was a bottleneck.
  Runtime 0.001483 (~tied with best), but the `import itertools` pushes loc to 3. Conclusion: the modulo
  is *not* the bottleneck; nothing gained. `kept best`.
- **Run 7 — explicit `for`/`append` loop with the lookup table** (the most clarity-forward Wirth form).
  Runtime 0.001745 and loc 5 — slower and longer than the comprehension. Confirms the comprehension is
  the right container-building structure. `kept best`.
- **Run 8 — classic `"Fizz"*(i%3<1)+"Buzz"*(i%5<1) or str(i)`.** Worst runtime (0.002373) **and** the
  only run where memory moved (41 KB, up from 38): the per-element string multiply/concat creates
  transient string objects that raise peak memory. `kept best`. Most informative negative result.
- **Run 9 — re-grade best.py to confirm + leave solution.py == best.py.** Correct, mem 38, loc 2;
  runtime sampled high (0.002699), underlining that runtime variance dwarfs the real differences.
  Stopped here with 1 run in reserve — the answer is locked and re-rolling for a lucky runtime sample
  would be gaming noise, not refinement.

## What worked, what didn't, key insight

- **Worked:** the single-modulo **lookup table** + **list comprehension** + **default-arg local** for the
  table. That trio is the frontier here: minimal transient allocation (memory stays at the 38 KB floor),
  fast local lookups, and just 2 lines.
- **Didn't:** lambda (loc 1 but same-or-worse speed, un-idiomatic), itertools/cycle (no speedup, +loc from
  import), explicit loop (slower, +loc), string-multiply (slower *and* +memory).
- **Key insight about the metric space:** memory was effectively constant at 38 KB (interpreter/measurement
  floor) for every allocation-frugal version — the *only* approach that disturbed it was the string-multiply
  idiom, and it made things worse. With memory fixed, promotion (≥2 of 3) realistically required winning
  **runtime AND loc together**, and runtime is heavily noise-dominated (min-of-5 still swung 0.0014–0.0027
  for identical code). So the durable levers are **loc** (deterministic) and **avoiding transient
  allocations** (keeps memory at the floor); chasing runtime is mostly chasing noise.

## Why best.py is the final answer

Run 4 is the only version that strictly beat the baseline on 2 of 3 metrics, and across all later
exploration nothing matched it on loc without losing runtime or memory (or readability). It is correct
(10/10), at the loc floor for a clean idiomatic `def`, at the memory floor, and at the fast end of the
noisy runtime band. It is also the most in-style result for a stepwise/Wirth agent: a single clear
comprehension whose only "trick" — the default-arg lookup table — is a well-understood CPython idiom,
not a clever obfuscation. solution.py equals best.py.
