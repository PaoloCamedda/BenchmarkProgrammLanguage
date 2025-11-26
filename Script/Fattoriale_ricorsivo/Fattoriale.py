import sys

def fattoriale_rec(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return n * fattoriale_rec(n - 1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <numero>")
        sys.exit(1)

    n = int(sys.argv[1])
    print(f"Fattoriale ricorsivo({n}) = {fattoriale_rec(n)}")
