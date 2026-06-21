class FizzBuzz:
    _P = {0: "FizzBuzz", 3: "Fizz", 6: "Fizz", 9: "Fizz", 12: "Fizz", 5: "Buzz", 10: "Buzz"}

    def sequence(self, n):
        return [self._P.get(i % 15) or str(i) for i in range(1, n + 1)]


def fizzbuzz(n):
    return FizzBuzz().sequence(n)
