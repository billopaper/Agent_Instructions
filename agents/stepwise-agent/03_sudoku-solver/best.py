def solve(board):
    A = 0b1111111110  # bits 1..9
    R = [0] * 9; C = [0] * 9; X = [0] * 9
    bx = lambda r, c: (r // 3) * 3 + c // 3
    units = [[(r, c) for c in range(9)] for r in range(9)] + [[(r, c) for r in range(9)] for c in range(9)] + [[(3 * (u // 3) + i, 3 * (u % 3) + j) for i in range(3) for j in range(3)] for u in range(9)]
    def cand(r, c):
        return A & ~(R[r] | C[c] | X[bx(r, c)])
    def put(r, c, bit):
        board[r][c] = bit.bit_length() - 1; R[r] |= bit; C[c] |= bit; X[bx(r, c)] |= bit
    def take(r, c, bit):
        board[r][c] = 0; R[r] ^= bit; C[c] ^= bit; X[bx(r, c)] ^= bit
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v:
                if not cand(r, c) & (1 << v): return False  # duplicate given
                put(r, c, 1 << v)
    def go():
        done = []
        while True:
            prog = False
            for r in range(9):  # naked singles
                for c in range(9):
                    if board[r][c]: continue
                    m = cand(r, c)
                    if not m:
                        for t in done: take(*t)
                        return False
                    if m & (m - 1) == 0:
                        put(r, c, m); done.append((r, c, m)); prog = True
            if prog: continue
            for unit in units:  # hidden singles via bitmask aggregation
                once = more = 0
                for (r, c) in unit:
                    if not board[r][c]:
                        m = cand(r, c); more |= once & m; once |= m
                h = once & ~more
                if h:
                    bit = h & -h
                    for (r, c) in unit:
                        if not board[r][c] and cand(r, c) & bit:
                            put(r, c, bit); done.append((r, c, bit)); prog = True; break
            if not prog: break
        best = None; bk = 10  # MRV branch cell
        for r in range(9):
            for c in range(9):
                if board[r][c]: continue
                m = cand(r, c); k = bin(m).count("1")
                if k < bk: bk = k; best = (r, c, m)
        if best is None: return True
        r, c, m = best
        while m:
            bit = m & -m; m ^= bit
            put(r, c, bit)
            if go(): return True
            take(r, c, bit)
        for t in done: take(*t)
        return False
    return go()
