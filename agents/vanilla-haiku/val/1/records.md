# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 0.986099 | 26653 | 25 | new best (Dijkstra, list-of-lists adj) |
| 2 | true | 0.801925 | 10106 | 48 | new best (CSR flat arrays: runtime -19%, mem -62%, loc worse) |
| 3 | true | 0.884220 | 8957 | 49 | reverted (packed-int heap: mem -11% but runtime +10% tie/worse, loc worse; only 1/3) |
| 4 | true | 1.392236 | 6837 | 50 | reverted (array-module CSR: mem -32% but runtime +73%, loc worse; only 1/3) |
| 5 | true | 0.857664 | 8957 | 51 | reverted (bit-shift packed heap: mem -11% but runtime tie +7%, loc worse; only 1/3) |
| 6 | true | 0.832097 | 9871 | 36 | new best (lean CSR: dropped deg array + compressed lines; mem -2%, loc -25%, runtime tie; 2/3) |
| 7 | true | 2.430305 | 18040 | 41 | reverted (single packed adj (v<<wb)|w: bigint promotion -> mem +83%, runtime +192%, loc worse; all worse) |
| 8 | true | 0.889029 | 9901 | 38 | reverted (done-array pruning: mem +0.3%, runtime tie +7%, loc worse; lazy staleness check is better; 0/3) |
| 9 | true | 1.681373 | 7594 | 39 | reverted (SPFA/Bellman-Ford queue: mem -23% (no tuple heap) but runtime +102%, loc worse; Dijkstra wins runtime; 1/3) |

Run 10 left unused: re-grading cannot promote (grader reports median runtime; same code, same metrics). solution.py == best.py (run 6 lean CSR Dijkstra) is the final answer.

## Final answer: run 6 (lean CSR + binary-heap Dijkstra) — runtime 0.832s, peak_memory 9871 KB, loc 36.

