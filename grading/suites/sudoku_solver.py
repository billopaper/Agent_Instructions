"""HIDDEN suite for train/03_sudoku-solver. Never expose to agents.

Standard 9x9 Sudoku. The runtime/memory signal comes from a set of genuinely HARD
puzzles (well-known backtracking stress tests): a naive backtracker churns for ~1s+ on
these while a constraint-propagation / bitmask solver finishes in milliseconds, and
propagation's candidate-set state vs lean backtracking spans a wide memory range. So all
three metrics discriminate, stably, with no large-board difficulty cliff.

A case is `(board, kind)`:
  - "solvable"   -> candidate returns True AND leaves a valid solution preserving givens
  - "unsolvable" -> candidate returns False AND leaves the board unchanged

Puzzles can have multiple valid solutions, so we never compare to a fixed board: run()
fully verifies (return value + valid 9x9 sudoku + givens preserved + no mutation on
failure) and reports a label; reference() returns the expected label.
"""
import copy


# --- validators ----------------------------------------------------------------
def _is_valid_solution(b):
    t = set(range(1, 10))
    for i in range(9):
        if set(b[i]) != t:                                          # row
            return False
        if {b[r][i] for r in range(9)} != t:                        # column
            return False
    for br in range(3):
        for bc in range(3):
            if {b[br * 3 + r][bc * 3 + c] for r in range(3) for c in range(3)} != t:
                return False                                        # 3x3 box
    return True


def _preserves_givens(given, work):
    return all(given[i][j] == 0 or given[i][j] == work[i][j]
               for i in range(9) for j in range(9))


# --- reference + run -----------------------------------------------------------
def reference(case):
    _, kind = case
    return "SOLVED_OK" if kind == "solvable" else "REJECTED_OK"


def run(candidate, case):
    board, kind = case
    given = copy.deepcopy(board)
    work = copy.deepcopy(board)
    try:
        result = candidate.solve(work)
    except Exception as exc:  # noqa: BLE001 — surface category, not text
        return f"EXCEPTION:{type(exc).__name__}"

    if kind == "solvable":
        if result is not True:
            return f"WRONG_RETURN:{result!r}"
        if any(0 in row for row in work):
            return "BOARD_NOT_FILLED"
        if not _is_valid_solution(work):
            return "INVALID_SOLUTION"
        if not _preserves_givens(given, work):
            return "MUTATED_GIVENS"
        return "SOLVED_OK"
    else:  # unsolvable
        if result is not False:
            return f"WRONG_RETURN:{result!r}"
        if work != given:
            return "MUTATED_ON_FAILURE"
        return "REJECTED_OK"


# --- hidden inputs -------------------------------------------------------------
def _parse(s):
    return [[int(s[r * 9 + c]) for c in range(9)] for r in range(9)]


# Genuinely hard 9x9 puzzles (well-known backtracking stress tests). Each is valid and
# has a solution; a propagation solver clears them in ms, a naive one takes ~1s+.
_HARDS = [
    "800000000003600000070090200050007000000045700000100030001000068008500010090000400",  # Inkala 2012
    "000000012000000003002300400001800005060070800000009000008500000900040500470006000",  # Platinum Blonde
    "000000039000001005003050800008090006070002000100400000009080050020000600400700000",  # Golden Nugget
    "100000002090400050006000700050903000000070000000850040700000600030009080002000001",  # Easter Monster
    "100007090030020008009600500005300900010080002600004000300000010040000007007000300",  # AI Escargot
]

# A complete valid board (already solved -> True, unchanged) and a classic easy puzzle.
_SOLVED = _parse("534678912672195348198342567859761423426853791713924856961537284287419635345286179")
_EASY = _parse("530070000600195000098000060800060003400803001700020006060000280000419005000080079")


def _conflict_row():
    b = [[0] * 9 for _ in range(9)]; b[0][0] = 5; b[0][1] = 5; return b   # two 5s in a row


def _conflict_col():
    b = [[0] * 9 for _ in range(9)]; b[0][0] = 5; b[1][0] = 5; return b   # two 5s in a column


def _conflict_box():
    b = [[0] * 9 for _ in range(9)]; b[0][0] = 5; b[1][1] = 5; return b   # two 5s in a box


CASES = (
    (_SOLVED, "solvable"),                       # already complete + valid
    (_EASY, "solvable"),                         # easy newspaper puzzle
    *[(_parse(s), "solvable") for s in _HARDS],  # hard puzzles -> runtime/memory stress
    (_conflict_row(), "unsolvable"),
    (_conflict_col(), "unsolvable"),
    (_conflict_box(), "unsolvable"),
)
