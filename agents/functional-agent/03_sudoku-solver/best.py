"""Functional Sudoku: pure recursion over immutable bitmask tuples, with naked-single propagation per frame and MRV branching at choice points."""
ALL = 0x1FF
RCB = tuple((i // 9, i % 9, (i // 9 // 3) * 3 + (i % 9) // 3) for i in range(81))


def _search(empties, rows, cols, boxes):
    placed, pend, changed = {}, empties, True
    while changed:
        changed, rem = False, []
        for idx in pend:
            r, c, b = RCB[idx]
            cand = ~(rows[r] | cols[c] | boxes[b]) & ALL
            if not cand:
                return None
            if cand & (cand - 1):
                rem.append(idx)
            else:  # forced cell -> assign and re-scan
                placed[idx] = cand.bit_length()
                rows = rows[:r] + (rows[r] | cand,) + rows[r + 1:]
                cols = cols[:c] + (cols[c] | cand,) + cols[c + 1:]
                boxes = boxes[:b] + (boxes[b] | cand,) + boxes[b + 1:]
                changed = True
        pend = rem
    if not pend:
        return placed
    pos, idx, cand = min(
        ((p, j, ~(rows[RCB[j][0]] | cols[RCB[j][1]] | boxes[RCB[j][2]]) & ALL)
         for p, j in enumerate(pend)), key=lambda t: t[2].bit_count())
    r, c, b = RCB[idx]
    rest = pend[:pos] + pend[pos + 1:]
    while cand:
        bit = cand & -cand; cand ^= bit
        res = _search(rest, rows[:r] + (rows[r] | bit,) + rows[r + 1:],
                      cols[:c] + (cols[c] | bit,) + cols[c + 1:],
                      boxes[:b] + (boxes[b] | bit,) + boxes[b + 1:])
        if res is not None:
            res[idx] = bit.bit_length()
            res.update(placed)
            return res
    return None


def solve(board):
    rows, cols, boxes, empties = [0] * 9, [0] * 9, [0] * 9, []
    for i in range(81):
        v = board[i // 9][i % 9]
        if not v:
            empties.append(i)
            continue
        bit = 1 << (v - 1)
        r, c, b = RCB[i]
        if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
            return False
        rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
    placed = _search(empties, tuple(rows), tuple(cols), tuple(boxes))
    if placed is None:
        return False
    for i, v in placed.items():
        board[i // 9][i % 9] = v
    return True
