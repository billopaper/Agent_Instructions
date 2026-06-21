from itertools import cycle
def fizzbuzz(n):
    pat = cycle(["", "", "Fizz", "", "Buzz", "Fizz", "", "", "Fizz", "Buzz", "", "Fizz", "", "", "FizzBuzz"])
    return [next(pat) or str(i) for i in range(1, n + 1)]
