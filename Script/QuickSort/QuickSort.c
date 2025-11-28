#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <unistd.h>   // chdir, readlink
#include <libgen.h>   // dirname
#include <string.h>   // strerror
#include <errno.h>

// Funzione di utilità per lo scambio (swap)
void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

// Funzione di Partizione (Partition)
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// Funzione principale di Quick Sort
void quick_sort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

// Funzione per la stampa dell'array
void printArray(int A[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", A[i]);
    printf("\n");
}

// --- Gestione Input/Output ---
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
            fprintf(stderr, "Errore di allocazione della memoria\n");
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

    quick_sort(arr, 0, count - 1);

    printf("Array ordinato: ");
    printArray(arr, count);

    free(arr);
    return 0;
}
