# Records — 02_expression-evaluator (functional agent)

Outcome: **never correct**. Every one of the 10 runs stably passed **20/21** hidden
tests with `error_class: AssertionError`. The single failing test was invariant to
every change attempted (number representation, unary-minus policy, scientific
notation, decimal edge forms, recursion limit). No version was promoted to `best.py`
via the promotion rule because none was ever `correct`; `best.py` holds the cleanest
20/21 variant as a final answer.

| run | correct | passed/total | runtime_s | peak_mem_kb | loc | what changed | action |
|-----|---------|--------------|-----------|-------------|-----|--------------|--------|
| 1 | no | 20/21 | 0.142 | 434 | 72 | recursive-descent, float (int-preserving), loose unary +/- | error (not correct) |
| 2 | no | 20/21 | 0.143 | 433 | 70 | removed unary plus | error — neutral |
| 3 | no | 20/21 | 0.137 | 433 | 70 | broadened decimal regex (accept `5.`) | error — neutral |
| 4 | no | 20/21 | 0.339 | 1021 | 74 | exact `Fraction` arithmetic | error — neutral (slower/heavier) |
| 5 | no | 20/21 | 0.133 | 434 | 89 | strict unary (leading / after `(` only) | error — neutral |
| 6 | no | 20/21 | 0.133 | 434 | 91 | + `sys.setrecursionlimit(1_000_000)` | error — neutral |
| 7 | no | 20/21 | 0.180 | 1897 | 74 | `Decimal` arithmetic, loose unary | error — neutral (heavier) |
| 8 | no | 20/21 | 0.143 | 434 | 70 | float + scientific-notation numbers | error — neutral |
| 9 | no | 20/21 | 0.139 | 434 | 76 | single unary minus (no stacking, op-adjacent OK) | error — neutral |
| 10 | no | 20/21 | 0.145 | 433 | 70 | require leading digit on decimals (`.5` raises) | error — neutral |

Final `solution.py` / `best.py`: run-1-style clean float textbook parser with lenient
`.5` support restored (loc 70, ~434 KB, ~0.14 s) — best metrics among the 20/21 variants.
