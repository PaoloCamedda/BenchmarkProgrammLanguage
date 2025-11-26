import sys

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python fibonacci_rec.py <numero>")
        sys.exit(1)
    n = int(sys.argv[1])
    print(f"Fibonacci({n}) = {fibonacci(n)}")
