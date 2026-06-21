# Sudoku Solver

## Language
Python

## Goal
Implement `solve(board)` that fills a 9×9 Sudoku grid in place and returns whether a solution exists.

## Rules
- `board` is a 9×9 list of lists; empty cells are `0`, filled cells are `1`–`9`.
- A solved board has each row, each column, and each 3×3 box containing the digits `1`–`9` exactly once.
- If a solution exists, fill the board and return `True`.
- If the board is unsolvable, return `False` and leave it effectively unchanged.
- The input is always a well-formed 9×9 grid.

## Example
A board with a valid solution returns `True`, after which every row, column, and 3×3 box contains `1`–`9` exactly once. An over-constrained board (e.g. two `5`s already in one row) returns `False`.

## Verification
Graded against a hidden test suite; you receive only a verdict (`correct`, `passed`/`total`) and metrics - never the test inputs or expected outputs. It exercises: easy and hard solvable puzzles (the result is checked against all Sudoku constraints), unsolvable boards (→ `False`), and an already-complete valid board (→ `True`, unchanged).
