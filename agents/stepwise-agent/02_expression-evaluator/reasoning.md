# Reasoning Trail — 02 Expression Evaluator (Stepwise Agent)

## Task recap
Implement `evaluate(expr)`: a hand-written parser for `+ - * /`, parentheses, unary
minus, decimals, true division, whitespace tolerance, and `ValueError` on division by
zero / unbalanced parens / dangling operators. Scored on correctness (gate), then peak
memory, runtime, and lines-of-code. 10 grader runs; `best.py` promotes only when ≥2 of 3
metrics strictly improve (runtime needs >10%; memory/LOC any strict decrease).

## Initial approach and why
I started with the textbook **recursive-descent parser** with a separate tokenizer:
grammar `expr := term (('+'|'-') term)*`, `term := factor (('*'|'/') factor)*`,
`factor := '-' factor | '(' expr ')' | number`. This is the simplest *correct* design
(stepwise principle: clarity first, brute force is fine), and recursive descent makes
precedence, left-associativity, and unary minus fall out naturally from the grammar
structure. Numbers were kept as `int` when integral and `float` when decimal, so
integer-only expressions return `14` not `14.0` (defensive about how the suite compares
results). Division-by-zero and structural errors raise `ValueError`.

## Iteration log

- **Run 1 — baseline (correct, rt 0.062, mem 525, loc 84).** Recursive descent with
  closures (`peek/advance` capturing `pos`) + manual tokenizer. 21/21. First correct →
  `best.py`.

- **Run 2 — regex tokenizer (reverted).** One change: replace the manual scanner with
  `re.match`. LOC dropped 84→73, but runtime ~doubled (0.062→0.109). **Insight: `import re`
  startup cost dominates** because the graded inputs are tiny — the import is a bigger
  cost than any parsing work. Only 1/3 improved (LOC). Reverted. *Lesson: avoid imports.*

- **Run 3 — module-level parse functions (NEW BEST, rt 0.072, mem 525→219, loc 84→61).**
  One change: moved the parse functions out of `evaluate` (no longer recreating 5 closures
  per call), passing `(tokens, pos)` and returning `(value, pos)`. **Memory more than
  halved (525→219)** + LOC down. 2/3 → promoted. *Insight: per-call closure allocation was
  a large slice of peak memory.*

- **Run 4 — precedence-climbing (reverted).** Merged `_expr`/`_term` into one
  `_parse(min_prec)` function. LOC 61→59, but memory stuck at 219 and runtime tied/worse.
  1/3 only. *Insight: source length doesn't move peak memory — allocations do.*

- **Run 5 — iterative two-stack / shunting-yard (reverted).** Different paradigm: explicit
  value/operator stacks, unary marker `'u'`, `want_operand` flag. Runtime 0.064 (~11%
  faster — no recursion overhead) but LOC ballooned to 78 and memory still 219. 1/3.
  *Insight: iterative is faster but verbose.*

- **Run 6 — SCANNERLESS recursive descent (NEW BEST, rt 0.086, mem 219→6, loc 61→56).**
  The breakthrough. I removed the intermediate **token list** entirely and parsed directly
  over the raw string with an index (`(s, i) -> (value, i)`, whitespace skipped inline).
  **Peak memory collapsed 219→6 KB** + LOC down. 2/3 → promoted. *Insight: building a token
  list was essentially the *entire* remaining memory cost on the large hidden input;
  scannerless parsing allocates almost nothing.* Cost: runtime rose (more function calls,
  recursion).

- **Run 7 — scannerless precedence-climbing (reverted).** LOC 56→52 but runtime rose to
  0.095 (repeated dict lookups + deeper same-precedence recursion). Memory tied at 6. 1/3.

- **Run 8 — scannerless + iterative (reverted).** The "missing quadrant": fast *and* tiny
  memory. Runtime 0.069 (~20% faster than run 6), mem 6, but LOC 74. 1/3. This mapped the
  **Pareto frontier**: run 6 owns (low-mem, low-LOC); run 8 owns (low-mem, fast). With
  memory pinned at the floor (6, a tie), beating run 6 required improving LOC *and* runtime
  *together*.

- **Run 9 — compress run 8 (reverted).** Partial compaction got LOC 74→66, runtime stayed
  fast (0.068). Still >56 LOC → 1/3. Confirmed LOC is counted per logical/physical line
  (merging statements reduces it), so denser code is a real lever.

- **Run 10 — compressed scannerless iterative (NEW BEST / FINAL, rt 0.070, mem 6, loc 47).**
  Took the fast iterative algorithm and collapsed it with guard-clause one-liners
  (`if not want: raise ...`) and combined assignments. **LOC 56→47 and runtime
  0.086→0.070 (−19%)**, memory at the floor. 2/3 → promoted. This broke the Pareto wall:
  the fast version, once compressed below the recursive version's line count, dominated it
  on the two non-floored metrics.

## What worked / what didn't
- **Worked:** stepwise one-change-per-run discipline made each metric movement
  attributable. The two big wins were structural, not clever: (1) module-level functions
  instead of per-call closures (mem 525→219); (2) scannerless parsing instead of a token
  list (mem 219→6). Both are pure allocation reductions.
- **Didn't work / dead ends:** regex (import cost), and every LOC-only tweak once memory
  hit its 6 KB floor (a single improved metric never promotes under the 2/3 rule).
- **Key patterns / insights:**
  1. For tiny graded inputs, **runtime is startup/allocation-bound, not algorithm-bound** —
     `import` cost is visible and recursion overhead matters more than asymptotics.
  2. **Peak memory is driven by intermediate data structures** (closures, token lists), not
     source size. Eliminating them is the highest-leverage memory move.
  3. The **2-of-3 promotion rule + a floored metric** forces you to win the other two
     simultaneously; partial wins stall. Recognizing the Pareto frontier (fast XOR compact)
     told me the only path was to compress the fast variant below the compact variant's LOC.

## Why `best.py` is the final answer
Run 10: a hand-written, scannerless, iterative two-stack (shunting-yard) evaluator. It is
the global optimum found across all three scored metrics — peak memory at the 6 KB floor
(tied-best, achieved by parsing the string directly with no token list), runtime ~19%
faster than the best recursive version (iteration avoids call/recursion overhead), and the
lowest LOC (47, via guard-clause idioms). It passes 21/21 and correctly handles precedence,
left-associativity, nested parens, right-associative unary minus (`--3`, `2 - -3`),
int/float distinction, decimals, whitespace, and all three error conditions. No other run
matched it on two metrics without losing a third.
