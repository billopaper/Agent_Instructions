# Arithmetic Expression Evaluator

## Language
Python

## Goal
Implement `evaluate(expr)` that parses and evaluates an arithmetic expression string and returns the resulting number.

## Rules
- Support `+`, `-`, `*`, `/`, parentheses, and unary minus (e.g. `-3 * (2 + 1)`).
- Honor standard operator precedence and left-associativity; parentheses override precedence.
- `/` is true division (so `10 / 4 == 2.5`). Support integers and decimals; ignore surrounding whitespace.
- Division by zero raises `ValueError`. Malformed input (unbalanced parentheses, a dangling operator) raises `ValueError`.
- The parser must be hand-written — no `eval` / `exec`.

## Example
Input: `"-3 * (2 + 1) + 10 / 4"` → Output: `-6.5`
Input: `"2 + 3 * 4"` → Output: `14`

## Verification
Graded against a hidden test suite; you receive only a verdict (`correct`, `passed`/`total`) and metrics - never the test inputs or expected outputs. It exercises: precedence and left-associativity, nested parentheses, unary minus, decimals, whitespace tolerance, and the error conditions (division by zero, unbalanced parentheses, dangling operators).
