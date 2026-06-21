# Records — 02_expression-evaluator

| run | correct | runtime_s | peak_kb | loc | action |
|-----|---------|-----------|---------|-----|--------|
| 1 | true | 0.040515 | 43 | 82 | new best |
| 2 | true | 0.115601 | 526 | 58 | reverted (regex: loc down but mem+runtime much worse) |
| 3 | true | 0.047995 | 37 | 63 | new best (mem 37<43, loc 63<82 — 2/3 improved) |
| 4 | false | 0.052737 | 35 | 51 | error (`'' in '+-'` is True → end-of-input misread) |
| 5 | true | 0.052270 | 33 | 51 | new best (mem 33<37, loc 51<63 — 2/3 improved; fixed run 4 bug w/ tuple membership) |
| 6 | true | 0.073066 | 6 | 73 | kept best (shunting-yard iterative: mem 6<33 huge, but loc 73 & runtime worse — only 1/3) |
| 7 | true | 0.073675 | 6 | 55 | kept best (compacted SY: mem 6<33 but loc 55>51 — only 1/3) |
| 8 | true | 0.071745 | 6 | 53 | kept best (more compact: loc 53>51 still — only 1/3) |
| 9 | true | 0.080529 | 6 | 42 | new best (mem 6<33, loc 42<51 — 2/3; one-line ifs got loc under) |
| 10 | true | 0.072589 | 7 | 44 | reverted (local-bound append/pop: rt within tie, mem 7>6, loc 44>42 — 0/3) |

**Final answer: best.py = run 9** (iterative shunting-yard, mem 6 kb, loc 42, rt ~0.08s). solution.py restored to match.
