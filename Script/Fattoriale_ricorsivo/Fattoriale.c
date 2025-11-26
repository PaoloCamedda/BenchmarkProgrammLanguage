#include <stdio.h>
#include <stdlib.h>

long fattoriale_rec(int n) {
    if (n == 0 || n == 1) return 1;
    return n * fattoriale_rec(n - 1);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <numero>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    printf("Fattoriale ricorsivo(%d) = %ld\n", n, fattoriale_rec(n));
    return 0;
}
