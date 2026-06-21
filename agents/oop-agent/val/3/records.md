# Records — Weighted Shortest Path (OOP agent)

Grade command: `python ../../../../grading/validate.py validation/weighted-shortest-path solution.py`
(folder is `val/3`, one level deeper than the template, hence the extra `../`.)

| run | correct | runtime_s | peak_mem_kb | loc | action |
|-----|---------|-----------|-------------|-----|--------|
| 1   | yes     | 1.069319  | 30012       | 45  | new best — first correct (Graph + DijkstraSolver classes, lazy heap Dijkstra) |
| 2   | yes     | 1.068326  | 30012       | 34  | kept best — only LOC improved (runtime tie within 10%, mem tie); single class, hot-loop locals |
| 3   | yes     | 0.922902  | 26653       | 37  | NEW BEST — all 3 improved (rt -13.6%, mem -3359kb, loc -8); tentative-distance Dijkstra (push only on strict improvement) |
| 4   | yes     | 0.821572  | 8886        | 52  | NEW BEST — rt -11% & mem -17767kb improved (loc +15 regressed); CSR via array('i')/('q'), index-based inner loop |
| 5   | yes     | 0.840359  | 7641        | 44  | NEW BEST — mem -1245kb & loc -8 improved (rt +2.3% tie); weights as array('i') (int32 fits), trimmed docstring/assignments |
| 6   | yes     | 0.846924  | 5355        | 46  | kept best — only mem improved (-2286kb); rt tie, loc +2 regressed; packed-int heap (key = d*n + node) removes tuple objects |
| 7   | yes     | 0.841237  | 5355        | 43  | NEW BEST — mem -2286kb & loc -1 improved (rt tie); packed-int heap + divmod() + inlined relax check |
| 8   | yes     | 0.712122  | 5355        | 42  | NEW BEST — rt -15.3% & loc -1 improved (mem tie); flat array('q') dist (-1 sentinel) + itertools.accumulate CSR build |
| 9   | yes     | 0.716580  | 7642        | 42  | kept best — tuple heap + array dist: rt tie, mem +2287kb regressed, loc tie. Confirms packed-int heap is "free" memory savings (no runtime cost). solution.py restored to best (run 8). |
