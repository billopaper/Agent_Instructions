# Reasoning — 02 Expression Evaluator (smart-agent / Einstein)

## Task recap
Implement `evaluate(expr)`: parse + evaluate arithmetic with `+ - * /`, parentheses,
unary minus, standard precedence + left-associativity, true division, int/decimal
literals, whitespace tolerance, and `ValueError` on div-by-zero / unbalanced parens /
dangling operators. Hand-written parser (no `eval`/`exec`). Graded on correctness
(gate), then **memory → runtime → loc** (that priority order matters — see below).

## Initial approach and why
As the smart-pattern agent I went straight for a real parsing algorithm rather than
ad-hoc string munging. Two canonical "smart" patterns fit:
1. **Precedence climbing** (compact Pratt-style recursive descent) — elegant, handles
   precedence/associativity/unary with one parametrized recursive function.
2. **Shunting-yard** (Dijkstra, two stacks, iterative) — classic, no recursion.

I started with precedence climbing because unary minus and associativity fall out of it
cleanly, then used the remaining grader runs to *measure* the alternatives instead of
guessing. The grader is the only oracle, so every design claim below is backed by a run.

## Iteration log (what / why / verdict / promote-or-revert)

- **Run 1 — precedence climbing, regex tokenizer.** Correct 21/21 immediately
  (rt 0.168, mem 515, loc 71). First correct ⇒ became best. Numbers parsed as `int`
  unless they contain `.` (so `2+3*4 → 14`, not `14.0`); `/` always yields float.
- **Run 2 — drop `re`, hand-written scanner, denser.** Hypothesis: regex import + the
  separate tokenize pass cost lines and a little memory. Result rt 0.105 / mem 510 /
  loc 52 — **all 3 improved** ⇒ promote. (Also learned: relying on `float()` to raise on
  malformed numbers like `1.2.3` removes an explicit validation branch.)
- **Run 3 — streaming recursive descent (no token list).** Key hypothesis: the 510 kb
  was the materialized token list, not the algorithm. Parsed straight off the string
  with an index pointer, building no list. Result **mem 510 → 27**, loc 52 → 39; runtime
  +13%. 2/3 improved ⇒ promote. **This was the biggest insight: materializing all
  tokens dominated peak memory; streaming kills it.**
- **Run 4 — `nonlocal i` int index instead of a `[0]` list-cell.** The streaming parser
  shared its cursor via a one-element list; a `nonlocal` int avoids per-access list
  indexing. Result rt 0.118 → 0.100 (~15% faster) and mem 27 → 26. 2/3 ⇒ promote.
- **Run 5 — shunting-yard (iterative two stacks).** Tried the other canonical pattern.
  Correct, and **mem 26 → 6** (no Python recursion frames; left-assoc consumes operands
  eagerly so both stacks stay tiny). But rt +40% and loc 49 ⇒ only 1/3 ⇒ kept best.
  Insight: iterative beats recursion on memory by a lot here.
- **Run 6 — compressed shunting-yard.** Since memory is the #1-ranked metric, 6 kb was
  worth capturing — I just needed a 2nd improving metric. Collapsed `apply` into a
  module-level lambda op-table and tightened the unary block (`op = 'u' if want else c`)
  to get loc 49 → 40. Result mem 6 / loc 40 (both < best) ⇒ **2/3 ⇒ promote.** Runtime
  +37% accepted because memory ranks above runtime. **This is the final best.**
- **Run 7 — frozenset char classification** (`c in _D` vs `c.isdigit()`). Tested whether
  per-char method calls were the runtime cost. Only ~5% faster (a tie) and loc +1 ⇒
  kept best. Insight: char-method overhead is NOT the bottleneck.
- **Run 8 — inline `apply` arithmetic (no lambda table).** Tested whether lambda dispatch
  was the cost. Runtime unchanged (tie), loc +2 ⇒ kept best. Insight: lambda dispatch is
  NOT the bottleneck either — shunting-yard's ~0.137 s is **structural** (operator-stack
  precedence loop + per-operator `apply()` call), so it can't be micro-optimized down to
  the recursive variant's ~0.10 s.

Stopped at run 8 with 2 runs unused: from the (mem 6 / loc 40) Pareto point, memory and
loc are at their floor and runtime is structurally bound, so no remaining edit could clear
the "≥2 of 3 improve" gate. Re-grading only re-samples the median, so it would gain
nothing. `solution.py` was restored to `best.py`.

## What worked / what didn't
- **Worked:** (a) not materializing a token list → 20× memory drop; (b) iterative
  shunting-yard → another 4× memory drop by eliminating recursion frames; (c) treating
  the grader as a measurement instrument — each run isolated one variable
  (tokenizer, cursor representation, algorithm, char-test, dispatch).
- **Didn't move the needle:** frozenset char tests and inline-vs-lambda dispatch — both
  ties. Good negative results: they tell the distillation that runtime here is dominated
  by algorithmic structure, not Python micro-overhead.
- **Tension that capped further gains:** the metrics trade off. Recursive descent is
  faster (~0.10 s) but costs 26 kb; shunting-yard is leaner (6 kb) but ~0.137 s. You can
  optimize *two* of the three to their floor, after which the promotion rule (≥2 improve)
  blocks the inherently-conflicting third.

## Key pattern converged on
**Iterative shunting-yard with a `'u'` pseudo-operator for unary minus** (precedence above
`*`/`/`, right-associative), a `want`-a-value flag to distinguish unary from binary `-`/`+`,
and end-state checks that turn every malformed case into `ValueError`:
- `want` still true at end / before a closing context ⇒ dangling operator;
- `)` with no matching `(`, or leftover `(` when draining ⇒ unbalanced;
- `len(val) != 1` at the end ⇒ malformed (e.g. two adjacent numbers);
- `float()` raises on bad numeric literals (`1.2.3`, lone `.`) for free.

## Why best.py is the final answer
The config scores **memory before runtime before loc**. The final solution has the lowest
memory found (6 kb) — so it strictly out-ranks every faster-but-26 kb recursive variant on
the primary metric — while also being the fewest lines (40) and passing 21/21. It's the
single point that is best on the top metric and co-minimal on loc; runtime is the
deliberately-sacrificed third metric, which is exactly the trade the scoring order rewards.
