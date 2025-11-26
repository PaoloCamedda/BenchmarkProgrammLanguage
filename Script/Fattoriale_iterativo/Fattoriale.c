#include <stdio.h>
#include <stdlib.h>

long fattoriale_iter(int n) {
    long risultato = 1;
    for (int i = 1; i <= n; i++) {
        risultato *= i;
    }
    return risultato;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <numero>\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    printf("Fattoriale(%d) = %ld\n", n, fattoriale_iter(n));
    return 0;
}


