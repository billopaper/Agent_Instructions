"""HIDDEN suite for train/02_expression-evaluator. Never expose to agents.

A case is a tuple `(expr, kind)` where `kind` is:
  - "ok"     -> the candidate's evaluate(expr) must return the numeric value
  - "raises" -> the candidate's evaluate(expr) must raise ValueError

To handle both shapes uniformly, both reference() and run() return either a number
(for "ok") or the sentinel `("RAISES", "ValueError")` (for "raises"); the grader's
equality check then validates correctness AND the exception type in one comparison.

The reference uses Python's eval (with builtins stripped, defence-in-depth). The
no-eval restriction in the task spec applies to the AGENT's solution, not the
hidden oracle.
"""

import random

_NO_BUILTINS = {"__builtins__": {}}


def _big(nterms, seed):
    """A long +/-/* expression for runtime/memory scaling. Products are kept isolated
    (at most d*d) so values stay small ints - no bignum blow-up to mask the parsing cost -
    and division is omitted so the result is exact. Parens are shallow (no deep recursion)."""
    rng = random.Random(seed)

    def term():
        a = str(rng.randint(1, 9))
        if rng.random() < 0.4:
            a += "*" + str(rng.randint(1, 9))                     # isolated product (<= 81)
        if rng.random() < 0.15:
            op = "+" if rng.random() < 0.5 else "-"
            a = "(" + a + op + str(rng.randint(1, 9)) + ")"       # shallow paren group
        return a

    parts = [term()]
    for _ in range(nterms - 1):
        parts.append("+" if rng.random() < 0.5 else "-")
        parts.append(term())
    return "".join(parts)


def _oracle(expr: str):
    # Restricted-scope eval so the oracle can't accidentally do anything beyond
    # arithmetic. Our cases only use +, -, *, /, parens, and numeric literals.
    return eval(expr, _NO_BUILTINS, {})


def reference(case):
    expr, kind = case
    if kind == "raises":
        return ("RAISES", "ValueError")
    return _oracle(expr)


def run(candidate, case):
    expr, kind = case
    try:
        value = candidate.evaluate(expr)
    except ValueError:
        return ("RAISES", "ValueError")
    except Exception as exc:  # noqa: BLE001 - wrong exception type is a fail
        return ("RAISES", type(exc).__name__)
    return value


# Cases pair an expression with whether it should evaluate or raise.
CASES = [
    # ---- valid: precedence, associativity, parens, decimals, whitespace, unary - ----
    ("0", "ok"),
    ("2 + 3 * 4", "ok"),                       # precedence -> 14
    ("-3 * (2 + 1) + 10 / 4", "ok"),           # spec example -> -6.5
    ("10 / 4", "ok"),                          # true division -> 2.5
    ("1.5 + 2.5", "ok"),                       # decimals -> 4.0
    ("  1   +   2  ", "ok"),                   # whitespace tolerance
    ("-(-5)", "ok"),                           # double unary minus -> 5
    ("((1 + 2)) * ((3 + 4))", "ok"),           # nested parens -> 21
    ("2 - 3 - 4", "ok"),                       # left-associativity -> -5
    ("100 / 10 / 2", "ok"),                    # left-assoc division -> 5.0
    ("0 * 1234567", "ok"),                     # multiplication by zero
    ("2 + 3 * 4 - 5 / 5", "ok"),               # mixed precedence -> 13.0
    ("(1 + 2) * 3", "ok"),                     # parens override -> 9
    # ---- invalid: must raise ValueError ------------------------------------------
    ("1 / 0", "raises"),                       # division by zero
    ("(1 + 2", "raises"),                      # unbalanced parentheses
    ("3 +", "raises"),                         # dangling operator
    ("", "raises"),                            # empty input
    ("( 1 + 2 ) )", "raises"),                 # extra close paren
    # ---- large: runtime + memory become real (candidate parses ~10-40k chars in Python) ----
    (_big(4000, 1), "ok"),
    (_big(6000, 2), "ok"),
    (_big(8000, 3), "ok"),
]
