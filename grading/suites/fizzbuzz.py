"""HIDDEN suite for train/00_fizzbuzz. Never expose to agents.

The control task: trivial, so it mainly verifies the convergence assumption rather than
discriminating styles. A case is an integer `n`; the expected output is the FizzBuzz list
for 1..n. The candidate must expose `fizzbuzz(n)` returning that list.
"""


def _fizzbuzz(n):
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out


def reference(case):
    return _fizzbuzz(case)


def run(candidate, case):
    return candidate.fizzbuzz(case)


# Hidden inputs: boundaries + a couple of larger n for a measurable (if floor-bound) run.
CASES = [0, 1, 2, 3, 5, 15, 16, 30, 100, 10000]
