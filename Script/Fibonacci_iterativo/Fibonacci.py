import sys

def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python fibonacci_py.py <numero>")
        sys.exit(1)
    n = int(sys.argv[1])
    print(f"Fibonacci({n}) = {fibonacci(n)}")
