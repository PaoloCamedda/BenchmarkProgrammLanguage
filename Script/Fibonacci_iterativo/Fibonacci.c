#include <stdio.h>
#include <stdlib.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    int a = 0, b = 1, c;
    for (int i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }
    return b;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Uso: %s <numero>\n", argv[0]);
        return 1;
    }
    int n = atoi(argv[1]);
    printf("Fibonacci(%d) = %d\n", n, fibonacci(n));
    return 0;
}
