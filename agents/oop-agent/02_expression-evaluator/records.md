# Run log — 02_expression-evaluator (OOP agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | yes     | 0.083951  | 2219           | 105 | new best (first correct) |
| 2   | yes     | 0.055349  | 7              | 79  | new best (3/3 improved: streaming, no token list) |
| 3   | yes     | 0.046830  | 7              | 80  | kept best (runtime ~15% lower but loc 80>79, mem tie: only 1/3) |
| 4   | yes     | 0.048024  | 7              | 67  | new best (2/3 improved: loc 67<79, runtime ~13% lower) |
| 5   | yes     | 0.050537  | 7              | 66  | kept best (precedence-climbing; loc 66<67 but runtime/mem tie: only 1/3) |
| 6   | yes     | 0.061907  | 7              | 59  | kept best (prec-climb + float()-validated number; loc 59<67 but runtime worse: 1/3) |
| 7   | yes     | 0.079359  | 6              | 84  | kept best (shunting-yard two-stack; mem 6<7 but runtime+loc worse: 1/3) |

**Stopped after run 7 (3 runs unused).** best = run 4. Memory is pinned at ~6-7 KB and
runtime is near its floor (~0.047 s); beating best on 2/3 metrics would require a >10%
runtime drop that only luck/noise could produce — which the rules explicitly say not to
chase. Four distinct algorithmic idioms were explored; best.py == solution.py is the final answer.
