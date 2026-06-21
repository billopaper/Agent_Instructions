# Records — weighted-shortest-path

| run | correct | runtime_s | peak_memory_kb | loc | action |
|-----|---------|-----------|----------------|-----|--------|
| 1 | true | 0.92774 | 26653 | 24 | new best |
| 2 | true | 1.226426 | 6837 | 40 | kept best (CSR arrays: mem -74% but runtime +32%, loc +16; only 1/3) |
| 3 | true | 1.309854 | 6837 | 40 | kept best (CSR zip-slice; no runtime gain) |
| 4 | true | 0.83786 | 8951 | 40 | kept best (flat python-list CSR: mem -66%, runtime -9.7% = tie band, loc +16; only 1/3) |
| 5 | true | 1.550802 | 8950 | 41 | kept best (interleaved flat + zip(it,it): much slower) |
| 6 | true | 0.844731 | 8951 | 42 | kept best (flat CSR + local push/pop; no real gain) |
| 7 | true | 0.85863 | 8980 | 44 | kept best (flat CSR + done[] array; no gain) |
| 8 | true | 0.691831 | 10107 | 21 | **new best** (compact CSR, accumulate offsets, no edge-copy: runtime -25%, mem -62%, loc -12.5% = 3/3) |
