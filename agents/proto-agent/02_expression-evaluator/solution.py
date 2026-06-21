def evaluate(expr):
    s, n = expr, len(expr)
    vals, ops = [], []
    P = {'u': 3, '*': 2, '/': 2, '+': 1, '-': 1}
    def apply():
        op = ops.pop()
        if op == 'u': vals.append(-vals.pop()); return
        b, a = vals.pop(), vals.pop()
        if op == '/' and b == 0: raise ValueError("div by zero")
        vals.append(a + b if op == '+' else a - b if op == '-' else a * b if op == '*' else a / b)
    i, expect = 0, True
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isdigit() or c == '.':
            j = i
            while j < n and (s[j].isdigit() or s[j] == '.'): j += 1
            t = s[i:j]
            if t.count('.') > 1: raise ValueError("malformed")
            vals.append(float(t) if '.' in t else int(t)); i, expect = j, False
        elif c == '(':
            ops.append(c); i += 1; expect = True
        elif c == ')':
            while ops and ops[-1] != '(': apply()
            if not ops: raise ValueError("unbalanced")
            ops.pop(); i += 1; expect = False
        elif c in '+-*/':
            if expect:
                if c == '-': ops.append('u')
                elif c != '+': raise ValueError("dangling")
            else:
                while ops and ops[-1] != '(' and P[ops[-1]] >= P[c]: apply()
                ops.append(c)
            i += 1; expect = True
        else:
            raise ValueError("bad char")
    if expect: raise ValueError("dangling")
    while ops:
        if ops[-1] == '(': raise ValueError("unbalanced")
        apply()
    return vals.pop()
