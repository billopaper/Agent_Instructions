"""Arithmetic expression evaluator: single-class recursive-descent parser.
Grammar: expr=term(('+'|'-')term)*  term=factor(('*'|'/')factor)*  factor='-'f|'+'f|'('expr')'|number
"""


class Parser:
    def __init__(self, text):
        self.s = text
        self.i = 0
        self.n = len(text)

    def evaluate(self):
        v = self._expr()
        if self._peek():
            raise ValueError("trailing input")
        return v

    def _peek(self):
        s = self.s
        while self.i < self.n and s[self.i] <= " ":
            self.i += 1
        return s[self.i] if self.i < self.n else ""

    def _expr(self):
        v = self._term()
        while (op := self._peek()) in ("+", "-"):
            self.i += 1
            v = v + self._term() if op == "+" else v - self._term()
        return v

    def _term(self):
        v = self._factor()
        while (op := self._peek()) in ("*", "/"):
            self.i += 1
            r = self._factor()
            if op == "*":
                v *= r
            elif r == 0:
                raise ValueError("division by zero")
            else:
                v /= r
        return v

    def _factor(self):
        ch = self._peek()
        if ch == "-":
            self.i += 1
            return -self._factor()
        if ch == "+":
            self.i += 1
            return self._factor()
        if ch == "(":
            self.i += 1
            v = self._expr()
            if self._peek() != ")":
                raise ValueError("unbalanced parentheses")
            self.i += 1
            return v
        return self._number()

    def _number(self):
        s, start, dot = self.s, self.i, False
        while self.i < self.n:
            c = s[self.i]
            if c.isdigit() or (c == "." and not dot):
                dot = dot or c == "."
                self.i += 1
            else:
                break
        raw = s[start:self.i]
        if not raw or raw == ".":
            raise ValueError("expected a number")
        return float(raw)


def evaluate(expr):
    return Parser(expr).evaluate()
