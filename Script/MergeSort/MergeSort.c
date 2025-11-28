#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <unistd.h>   // chdir, readlink
#include <libgen.h>   // dirname
#include <string.h>
#include <errno.h>

// Funzione per la fusione (Merge) di due sotto-array
void merge(int arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    int L[n1], R[n2];

    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    i = 0; j = 0; k = l;

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }

    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}

void printArray(int A[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", A[i]);
    printf("\n");
}

int main(void) {
    // Porta il working directory nella cartella dell’eseguibile
    char exe_path[PATH_MAX];
    ssize_t len = readlink("/proc/self/exe", exe_path, sizeof(exe_path) - 1);
    if (len == -1) {
        fprintf(stderr, "Errore: readlink fallita: %s\n", strerror(errno));
        return 1;
    }
    exe_path[len] = '\0';
    char *dir = dirname(exe_path);
    if (chdir(dir) != 0) {
        fprintf(stderr, "Errore: chdir(%s) fallito: %s\n", dir, strerror(errno));
        return 1;
    }

    FILE *file = fopen("input.txt", "r");
    if (!file) {
        fprintf(stderr, "Errore: impossibile aprire 'input.txt' in %s: %s\n", dir, strerror(errno));
        return 1;
    }

    int *arr = NULL;
    int count = 0;
    int number;

    while (fscanf(file, "%d", &number) == 1) {
        int *tmp = realloc(arr, (count + 1) * sizeof(int));
        if (!tmp) {
            fprintf(stderr, "Errore di allocazione memoria\n");
            free(arr);
            fclose(file);
            return 1;
        }
        arr = tmp;
        arr[count++] = number;
    }
    fclose(file);

    if (count == 0) {
        fprintf(stderr, "Il file 'input.txt' è vuoto o non contiene numeri validi.\n");
        free(arr);
        return 0;
    }

    printf("Array non ordinato: ");
    printArray(arr, count);

    mergeSort(arr, 0, count - 1);

    printf("Array ordinato: ");
    printArray(arr, count);

    free(arr);
    return 0;
}
