_PREC = {'u': 3, '*': 2, '/': 2, '+': 1, '-': 1}


def _apply(v, op):
    if op == 'u':
        v.append(-v.pop())
        return
    b, a = v.pop(), v.pop()
    if op == '+': v.append(a + b)
    elif op == '-': v.append(a - b)
    elif op == '*': v.append(a * b)
    elif b == 0: raise ValueError("division by zero")
    else: v.append(a / b)


def evaluate(expr):
    v, ops, want, i, n = [], [], True, 0, len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
        elif c.isdigit() or c == '.':
            if not want: raise ValueError("missing operator")
            j = i
            while j < n and (expr[j].isdigit() or expr[j] == '.'): j += 1
            t = expr[i:j]
            v.append(float(t) if '.' in t else int(t))
            want, i = False, j
        elif c == '(':
            ops.append(c); want, i = True, i + 1
        elif c == ')':
            while ops and ops[-1] != '(': _apply(v, ops.pop())
            if not ops: raise ValueError("unbalanced parentheses")
            ops.pop(); want, i = False, i + 1
        elif c in _PREC:
            op = 'u' if want and c == '-' else c
            if want and op != 'u':
                if c != '+': raise ValueError("dangling operator")
                i += 1; continue
            while ops and ops[-1] != '(' and (_PREC[ops[-1]] > _PREC[op]
                    or (_PREC[ops[-1]] == _PREC[op] and op != 'u')):
                _apply(v, ops.pop())
            ops.append(op); want, i = True, i + 1
        else:
            raise ValueError("bad char")
    if want: raise ValueError("dangling operator")
    while ops:
        op = ops.pop()
        if op == '(': raise ValueError("unbalanced parentheses")
        _apply(v, op)
    return v[0]
