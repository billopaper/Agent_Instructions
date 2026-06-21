"""Arithmetic expression evaluator — functional, recursive-descent.

Pure functions throughout: each parser takes (tokens, position) and returns
(value, next_position). No shared mutable state; the token list is read-only.

Grammar (standard precedence, left-associative):
    expr   -> term   (('+' | '-') term)*
    term   -> factor (('*' | '/') factor)*
    factor -> '-' factor | '(' expr ')' | number
"""

import re

_TOKEN = re.compile(r"\s*(?:(\d+\.?\d*|\.\d+)|(.))")


def _tokenize(expr):
    """expr string -> immutable tuple of tokens (numbers as float/int, ops as str)."""
    tokens = []
    pos = 0
    n = len(expr)
    while pos < n:
        m = _TOKEN.match(expr, pos)
        if not m or m.end() == pos:
            break
        num, sym = m.group(1), m.group(2)
        if num is not None:
            tokens.append(int(num) if num.isdigit() else float(num))
        elif sym is not None:
            if sym not in "+-*/()":
                raise ValueError(f"unexpected character: {sym!r}")
            tokens.append(sym)
        pos = m.end()
    return tuple(tokens)


def _parse_factor(tokens, i):
    if i >= len(tokens):
        raise ValueError("unexpected end of input")
    tok = tokens[i]
    if tok == "-":
        value, j = _parse_factor(tokens, i + 1)
        return -value, j
    if tok == "(":
        value, j = _parse_expr(tokens, i + 1)
        if j >= len(tokens) or tokens[j] != ")":
            raise ValueError("unbalanced parentheses")
        return value, j + 1
    if isinstance(tok, (int, float)):
        return tok, i + 1
    raise ValueError(f"unexpected token: {tok!r}")


def _parse_term(tokens, i):
    value, i = _parse_factor(tokens, i)
    while i < len(tokens) and tokens[i] in ("*", "/"):
        op = tokens[i]
        rhs, i = _parse_factor(tokens, i + 1)
        if op == "*":
            value = value * rhs
        else:
            if rhs == 0:
                raise ValueError("division by zero")
            value = value / rhs
    return value, i


def _parse_expr(tokens, i):
    value, i = _parse_term(tokens, i)
    while i < len(tokens) and tokens[i] in ("+", "-"):
        op = tokens[i]
        rhs, i = _parse_term(tokens, i + 1)
        value = value + rhs if op == "+" else value - rhs
    return value, i


def evaluate(expr):
    tokens = _tokenize(expr)
    if not tokens:
        raise ValueError("empty expression")
    value, i = _parse_expr(tokens, 0)
    if i != len(tokens):
        raise ValueError("unexpected trailing input")
    return value
