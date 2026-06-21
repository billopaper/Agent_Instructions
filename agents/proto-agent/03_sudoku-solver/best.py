def solve(board):
    rows, cols, boxes = ([0] * 9 for _ in range(3))
    empties = []
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == 0:
                empties.append(r * 9 + c)
            else:
                bit = 1 << v; b = (r // 3) * 3 + c // 3
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return False
                rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
    FULL, n = 0x3FE, len(empties)

    def bt(k):
        if k == n:
            return True
        bi, bav, bc = -1, 0, 99
        for i in range(k, n):
            r, c = divmod(empties[i], 9); b = (r // 3) * 3 + c // 3
            av = FULL & ~(rows[r] | cols[c] | boxes[b])
            cnt = av.bit_count()
            if cnt == 0:
                return False
            if cnt < bc:
                bc, bi, bav = cnt, i, av
                if cnt == 1:
                    break
        empties[k], empties[bi] = empties[bi], empties[k]
        r, c = divmod(empties[k], 9); b = (r // 3) * 3 + c // 3
        av = bav
        while av:
            bit = av & -av; av ^= bit
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            board[r][c] = bit.bit_length() - 1
            if bt(k + 1):
                return True
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
            board[r][c] = 0
        empties[k], empties[bi] = empties[bi], empties[k]
        return False

    return bt(0)
