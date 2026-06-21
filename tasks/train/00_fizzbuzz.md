# FizzBuzz

## Language
Python

## Goal
Implement `fizzbuzz(n)` returning the FizzBuzz sequence for `1..n` as a list of length `n`.

## Rules
- For each integer `i` from `1` to `n`, the element is:
  - `"FizzBuzz"` if `i` is divisible by both 3 and 5,
  - `"Fizz"` if divisible by 3,
  - `"Buzz"` if divisible by 5,
  - otherwise the number as a string, `str(i)`.
- Return a list of these values, in order, with length `n`.
- For `n <= 0`, return an empty list.

## Example
| n | result |
|---|--------|
| 5 | `["1", "2", "Fizz", "4", "Buzz"]` |
| 15 | `[..., "13", "14", "FizzBuzz"]` |

## Verification
This is the **control task** (numbered `00`): it is trivial, so agents are expected to converge on essentially the same solution - it checks that assumption rather than discriminating styles. Graded against a hidden test suite; you receive only a verdict (`correct`, `passed`/`total`) and metrics. It exercises: multiples of 3, 5, and 15, non-multiples, and the `n = 0` / `n = 1` boundaries. The visible `Example` is not graded.
