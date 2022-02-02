def fib(n):
    assert n >= 0
    f0, f1 = 0, 1
    first_n = [f0, f1]
    for _ in range(n - 2):
        f0, f1 = f1, f0 + f1
        first_n.append(f1)
    return first_n[:n]
