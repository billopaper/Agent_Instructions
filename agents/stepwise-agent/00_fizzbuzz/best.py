def fizzbuzz(n, _P=("FizzBuzz", "", "", "Fizz", "", "Buzz", "Fizz", "", "", "Fizz", "Buzz", "", "Fizz", "", "")):
    return [_P[i % 15] or str(i) for i in range(1, n + 1)]
