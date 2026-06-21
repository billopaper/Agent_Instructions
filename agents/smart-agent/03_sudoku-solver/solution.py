_POP = bytes(bin(i).count("1") for i in range(512))
_BOX = bytes((r // 3) * 3 + c // 3 for r in range(9) for c in range(9))


def solve(board):
    rows = [0] * 9; cols = [0] * 9; boxes = [0] * 9
    empties = []
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v:
                bit = 1 << (v - 1); b = _BOX[r * 9 + c]
                if (rows[r] | cols[c] | boxes[b]) & bit:
                    return False
                rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            else:
                empties.append(r * 9 + c)

    def bt(empties=empties, rows=rows, cols=cols, boxes=boxes, board=board, POP=_POP, BOX=_BOX, FULL=0x1FF):
        if not empties:
            return True
        best_i = -1; best_cnt = 10; best_cand = 0
        for i, p in enumerate(empties):
            cand = FULL & ~(rows[p // 9] | cols[p % 9] | boxes[BOX[p]])
            cnt = POP[cand]
            if cnt < best_cnt:
                if cnt == 0:
                    return False
                best_cnt = cnt; best_i = i; best_cand = cand
                if cnt == 1:
                    break
        p = empties[best_i]; empties[best_i] = empties[-1]; empties.pop(); r = p // 9; c = p % 9; b = BOX[p]; cand = best_cand
        while cand:
            bit = cand & -cand; cand ^= bit
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            board[r][c] = bit.bit_length()
            if bt():
                return True
            rows[r] ^= bit; cols[c] ^= bit; boxes[b] ^= bit
        board[r][c] = 0; empties.append(p)
        return False

    return bt()
