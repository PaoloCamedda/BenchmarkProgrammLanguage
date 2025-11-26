import sys

def fattoriale_iter(n: int) -> int:
    risultato = 1
    for i in range(1, n + 1):
        risultato *= i
    return risultato

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <numero>")
        sys.exit(1)

    n = int(sys.argv[1])
    print(f"Fattoriale iterativo({n}) = {fattoriale_iter(n)}")
