def fizzbuzz(n):
    labels = ("FizzBuzz", "", "", "Fizz", "", "Buzz", "Fizz", "", "", "Fizz", "Buzz", "", "Fizz", "", "")
    return [labels[i % 15] or str(i) for i in range(1, n + 1)]
