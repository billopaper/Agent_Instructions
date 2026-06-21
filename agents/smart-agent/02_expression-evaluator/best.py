_PR = {'+': 1, '-': 1, '*': 2, '/': 2, 'u': 3}    # 'u' = unary minus
_OP = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b, '/': lambda a, b: a / b}


def evaluate(expr):                               # shunting-yard, iterative two stacks
    n, i = len(expr), 0
    val, ops = [], []
    want = True                                   # expecting a value/operand?

    def apply():
        o = ops.pop()
        if o == 'u': val.append(-val.pop()); return
        b = val.pop(); a = val.pop()
        if o == '/' and b == 0: raise ValueError("division by zero")
        val.append(_OP[o](a, b))

    while i < n:
        c = expr[i]
        if c.isspace(): i += 1
        elif c.isdigit() or c == '.':
            j = i
            while i < n and (expr[i].isdigit() or expr[i] == '.'): i += 1
            s = expr[j:i]
            val.append(float(s) if '.' in s else int(s)); want = False
        elif c == '(':
            ops.append(c); i += 1; want = True
        elif c == ')':
            while ops and ops[-1] != '(': apply()
            if not ops: raise ValueError("unbalanced")
            ops.pop(); i += 1; want = False
        elif c in _PR:
            if want:
                if c == '+': i += 1; continue
                if c != '-': raise ValueError("dangling operator")
            op = 'u' if want else c
            while ops and ops[-1] != '(' and (_PR[ops[-1]] > _PR[op] or (_PR[ops[-1]] == _PR[op] and op != 'u')): apply()
            ops.append(op); i += 1; want = True
        else: raise ValueError("bad character")

    if want: raise ValueError("dangling operator")
    while ops:
        if ops[-1] == '(': raise ValueError("unbalanced")
        apply()
    if len(val) != 1: raise ValueError("malformed")
    return val[0]
