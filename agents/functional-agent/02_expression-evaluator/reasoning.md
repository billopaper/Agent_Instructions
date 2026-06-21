# Reasoning trail — 02_expression-evaluator (functional agent)

## Outcome up front

**Never reached `correct`.** All 10 grader runs returned **20/21** with
`error_class: AssertionError`. One hidden test failed on every single attempt and I
was unable to identify it. This document is an honest record of the deduction process
— including the wrong turns — because that trail is the experiment's raw material.

## Initial approach and why

The style is functional / declarative, so I wrote a **recursive-descent parser as a set
of pure functions**: each parser takes `(tokens, position)` and returns
`(value, next_position)`. No shared mutable state; the token tuple is read-only;
recursion + small loops express the grammar directly.

Standard grammar:

```
expr   -> term   (('+' | '-') term)*
term   -> factor (('*' | '/') factor)*
factor -> '-' factor | '(' expr ')' | number
```

Tokenizer: a single regex producing numbers (int when integral, float otherwise) and
single-char operators; anything else raises `ValueError`. Errors (unbalanced parens,
dangling operators, trailing input, empty input, division by zero) raise `ValueError`
per the spec. This is a textbook-correct evaluator and it passed 20/21 immediately.

## Iteration-by-iteration

1. **Run 1 — baseline.** Loose unary (`+`/`-`), float, int-preserving. 20/21,
   AssertionError. The example expressions (`-3*(2+1)+10/4 = -6.5`, `2+3*4 = 14`) both
   evaluate correctly by hand-trace.
2. **Run 2 — drop unary plus.** Hypothesis: a "dangling operator" test rejects `+5`.
   Neutral (still 20). Proves unary-plus is **untested** (count unchanged either way).
3. **Run 3 — accept trailing-dot decimals (`5.`).** Hypothesis: a decimals test uses
   `5.`. Neutral. Proves `5.` is untested.
4. **Run 4 — exact `Fraction` arithmetic.** Hypothesis: reference is exact, so
   `0.1+0.2` etc. diverge from my float. Neutral, but slower/heavier. **Key inference:**
   the grader compares **by value (`==`)**, not type — it accepted `Fraction` objects
   without breaking anything. And precision is ruled out: an exact-vs-float divergent
   test would have made run 4 differ from the float runs; it didn't.
5. **Run 5 — strict unary** (minus only at expression start / after `(`). Hypothesis:
   reference rejects operator-adjacent unary like `2 + -3`. Neutral.
6. **Run 6 — `sys.setrecursionlimit(1_000_000)`.** Hypothesis: deep nested-paren test
   overflows the default recursion limit. Neutral → not recursion (and no crash, so the
   nesting depth never approached the limit).
7. **Run 7 — `Decimal` arithmetic.** Hypothesis: reference uses 28-digit `Decimal`, so a
   repeating decimal like `1/3` matches neither float nor `Fraction`. Neutral → reference
   is not `Decimal` either (run 7 would have improved).
8. **Run 8 — scientific notation.** Hypothesis: a decimals test uses `1e3` that I reject.
   Neutral → scientific notation untested.
9. **Run 9 — single unary minus** (op-adjacent allowed, stacking `--3` rejected).
   Hypothesis: the loose runs and strict runs were each failing a *different* unary test,
   both netting 20; a middle policy passes both. Neutral → the unary shuffle is not it.
10. **Run 10 — require a leading digit on decimals (`.5` raises).** The one number-format
    behavior I had never toggled (all runs accepted `.5`). Neutral → `.5` untested too.

## What I learned (the constraints)

By the end, the failing test is provably insensitive to **all** of:
number representation (float / `Fraction` / `Decimal`), unary-minus policy
(loose / strict / single), scientific notation, leading/trailing decimal dots, and
recursion limit. The grammar's precedence and left-associativity are verifiably correct
by hand-trace for every combination of `+ - * / ()` and leading unary minus, and a
correct standard parser computes those values exactly — so it is **not** an arithmetic
value error. The grader compares by value, so int-vs-float type never matters.

Two mutually reinforcing deductions that I could not reconcile:
- If the reference oracle uses plain float, my float matches it bit-for-bit on every
  expression, so **no value test can fail** ⇒ the failure must be an accept/raise
  mismatch. But my strict version (run 5/6) raises `ValueError` on **every** malformed
  form I could construct, and I never found a malformed input it wrongly accepts, nor a
  valid input it wrongly rejects (beyond exotic forms — scientific, `.5`, implicit
  multiplication — which I tested and found neutral).
- Conversely it is not a precision/representation test, because float, `Fraction`, and
  `Decimal` all fail the *same* case identically.

## Honest assessment / what I'd try with more runs

I could not crack the 21st test within 10 runs. The remaining un-eliminated hypotheses
(all low-confidence): implicit multiplication (`2(3)`), an empty/whitespace input that
the reference treats as a value rather than an error, or a non-standard reference
convention the spec's wording doesn't reveal. The biggest methodological mistake was
**spending early runs on representation tweaks** (Fraction, Decimal, scientific) whose
neutrality I could partly have predicted, instead of using runs as **discriminating
probes** — e.g. an "always raise" run to measure how many tests are error-tests vs
value-tests, which would have split the hypothesis space decisively. Each run is a
scarce binary-search signal; I treated several as guesses rather than experiments.

## Why `best.py` is the final answer

No version was ever `correct`, so the promotion rule never fired and there is no
verified winner. Among the ten 20/21 variants, the run-1-style clean float textbook
parser has the best metrics (loc 70, ~434 KB, ~0.14 s) and the simplest, most
idiomatic functional structure, with lenient `.5` support restored (grader-neutral but
more correct for real input). That is what `best.py` / `solution.py` contain.
