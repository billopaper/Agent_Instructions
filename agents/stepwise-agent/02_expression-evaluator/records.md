# Records — 02 Expression Evaluator (Stepwise Agent)

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1   | true    | 0.062136  | 525            | 84  | new best — recursive descent, manual tokenizer |
| 2   | true    | 0.109404  | 525            | 73  | reverted — regex tokenizer: LOC down but runtime ~2x worse (import re cost), mem tie → only 1/3 improved |
| 3   | true    | 0.072334  | 219            | 61  | new best — module-level parse fns (no per-call closures): mem 525→219 + loc 84→61 = 2/3 improved |
| 4   | true    | 0.077911  | 219            | 59  | reverted — precedence-climbing (merged expr/term): loc 61→59 but mem tie, runtime tie → 1/3 only |
| 5   | true    | 0.064255  | 219            | 78  | reverted — iterative two-stack (shunting-yard): runtime ~-11% (no recursion) but loc 61→78 worse, mem tie → 1/3 |
| 6   | true    | 0.086408  | 6              | 56  | new best — SCANNERLESS recursive descent (no token list): mem 219→6 + loc 61→56 = 2/3. Token list was the whole memory cost. |
| 7   | true    | 0.095478  | 6              | 52  | reverted — scannerless precedence-climbing: loc 56→52 but runtime worse (dict lookups + deeper recursion), mem tie → 1/3 |
| 8   | true    | 0.068625  | 6              | 74  | reverted — scannerless iterative two-stack: runtime -20% + mem 6, but loc 56→74 worse → 1/3 (Pareto: fast XOR compact) |
| 9   | true    | 0.067842  | 6              | 66  | reverted — same algo, partial compression: runtime -21% + mem 6, but loc 66 still > 56 → 1/3 |
| 10  | true    | 0.069867  | 6              | 47  | **new best (FINAL)** — scannerless iterative, guard-clause one-liners: runtime 0.086→0.070 (-19%) + loc 56→47 = 2/3. Broke the Pareto wall by compressing the fast version under the recursive one's LOC. |
