# Records — 02 Expression Evaluator (smart-agent)

| run | correct | passed/total | runtime_s | peak_mem_kb | loc | action |
|-----|---------|--------------|-----------|-------------|-----|--------|
| 1   | true    | 21/21        | 0.168013  | 515         | 71  | new best — precedence-climbing parser (regex tokenizer) |
| 2   | true    | 21/21        | 0.104557  | 510         | 52  | new best — dropped `re`, hand-written scanner, denser (3/3 improved) |
| 3   | true    | 21/21        | 0.11789   | 27          | 39  | new best — streaming recursive descent, no token list (mem 510→27, loc 52→39; runtime +13% but 2/3 improved) |
| 4   | true    | 21/21        | 0.10046   | 26          | 42  | new best — `nonlocal i` int index instead of `[0]` list-cell (rt 0.118→0.100 ~15% faster, mem 27→26; loc +3 but 2/3 improved) |
| 5   | true    | 21/21        | 0.141356  | 6           | 49  | kept best — shunting-yard, iterative two stacks: mem 26→6 (no recursion frames!) but rt +40% & loc 49; only 1/3 improved. Insight: iterative beats recursion on memory. |
| 6   | true    | 21/21        | 0.1378    | 6           | 40  | new best — compressed shunting-yard (lambda op-table, tightened unary block): mem 26→6 & loc 42→40 (2/3); runtime +37% but memory is the #1 metric. |
| 7   | true    | 21/21        | 0.131508  | 6           | 41  | kept best — set/frozenset char classification instead of `.isspace()`/`.isdigit()`: rt only ~5% lower (tie), loc +1. Insight: char-method overhead is NOT the bottleneck. |
| 8   | true    | 21/21        | 0.136539  | 6           | 42  | kept best — inline `apply` arithmetic (no lambda table): rt unchanged (tie), loc +2. Insight: lambda dispatch is NOT the bottleneck; shunting-yard's runtime is structural (operator-stack mgmt). |

**Stopped at run 8 (2 runs unused).** Best = run 6. Re-grading reports the median (chasing a lucky time is pointless), and from the Pareto point (mem 6 / loc 40) no remaining idea clears the 2/3 promotion gate: memory & loc are at their floor, and runtime is structurally bound to ~0.137 for the iterative approach. `solution.py` restored to `best.py`.

## Final best (run 6)
- correct 21/21, **peak_memory 6 kb**, runtime 0.1378 s, **loc 40**
- Algorithm: shunting-yard (iterative, two stacks) with a lambda operator-table and `'u'` pseudo-operator for unary minus.
- Chosen because the config ranks **memory before runtime before loc**: 6 kb (no recursion frames) beats the recursive-descent variants (26 kb) on the top metric, and loc is minimal.
