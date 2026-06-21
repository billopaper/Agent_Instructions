def fizzbuzz(n):
    base = ["", "", "Fizz", "", "Buzz", "Fizz", "", "", "Fizz", "Buzz", "", "Fizz", "", "", "FizzBuzz"]
    out = (base * (n // 15 + 1))[:n]
    for i, v in enumerate(out):
        if not v:
            out[i] = str(i + 1)
    return out
