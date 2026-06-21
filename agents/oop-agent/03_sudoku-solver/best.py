"""OO Sudoku solver: bitmask constraints + MRV backtracking (int cells, RCB table)."""

_POP = bytes(bin(i).count("1") for i in range(1024))
_RCB = [(i // 9, i % 9, (i // 27) * 3 + (i % 9) // 3) for i in range(81)]


class SudokuSolver:
    __slots__ = ("board", "rows", "cols", "boxes", "empties")

    def __init__(self, board):
        self.board = board
        self.rows = [0] * 9
        self.cols = [0] * 9
        self.boxes = [0] * 9
        self.empties = []

    def solve(self):
        board, rows, cols, boxes, empties = (
            self.board, self.rows, self.cols, self.boxes, self.empties)
        for r in range(9):
            row = board[r]
            base = (r // 3) * 3
            for c in range(9):
                v = row[c]
                if v:
                    bit = 1 << v
                    b = base + c // 3
                    if (rows[r] | cols[c] | boxes[b]) & bit:
                        return False
                    rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
                else:
                    empties.append(r * 9 + c)
        return self._fill()

    def _fill(self):
        empties = self.empties
        if not empties:
            return True
        board, rows, cols, boxes = self.board, self.rows, self.cols, self.boxes
        bi, bfree, bcnt = -1, 0, 10
        for i, cell in enumerate(empties):
            r, c, b = _RCB[cell]
            free = ~(rows[r] | cols[c] | boxes[b]) & 0x3FE
            cnt = _POP[free]
            if cnt < bcnt:
                if cnt == 0:
                    return False
                bi, bfree, bcnt = i, free, cnt
                if cnt == 1:
                    break
        cell = empties[bi]; r, c, b = _RCB[cell]
        last = empties.pop()
        if bi < len(empties):
            empties[bi] = last
        free = bfree
        while free:
            bit = free & -free
            free -= bit
            board[r][c] = bit.bit_length() - 1
            rows[r] |= bit; cols[c] |= bit; boxes[b] |= bit
            if self._fill():
                return True
            rows[r] &= ~bit; cols[c] &= ~bit; boxes[b] &= ~bit
        board[r][c] = 0
        if bi < len(empties):
            empties.append(empties[bi]); empties[bi] = cell
        else:
            empties.append(cell)
        return False


def solve(board):
    return SudokuSolver(board).solve()
