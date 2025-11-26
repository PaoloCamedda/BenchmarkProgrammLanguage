#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

// Funzione per la fusione (Merge) di due sotto-array
void merge(int arr[], int l, int m, int r) {
    int i, j, k;
    int n1 = m - l + 1;
    int n2 = r - m;

    // Crea array temporanei
    int L[n1], R[n2];

    // Copia i dati negli array temporanei L[] e R[]
    for (i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    // Fusione degli array temporanei nell'array principale arr[l..r]
    i = 0; // Indice iniziale del primo sotto-array
    j = 0; // Indice iniziale del secondo sotto-array
    k = l; // Indice iniziale dell'array unito

    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            i++;
        } else {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    // Copia gli elementi rimanenti di L[]
    while (i < n1) {
        arr[k] = L[i];
        i++;
        k++;
    }

    // Copia gli elementi rimanenti di R[]
    while (j < n2) {
        arr[k] = R[j];
        j++;
        k++;
    }
}

// Funzione principale di Merge Sort
void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        // 1. DIVIDI
        int m = l + (r - l) / 2;

        // 2. RICORRI
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);

        // 3. CONQUISTA (MERGE)
        merge(arr, l, m, r);
    }
}

// Funzione per la stampa dell'array
void printArray(int A[], int size) {
    int i;
    for (i = 0; i < size; i++)
        printf("%d ", A[i]);
    printf("\n");
}

// --- Gestione Input/Output ---
int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("Errore: impossibile aprire il file 'input.txt'\n");
        return 1;
    }

    int *arr = NULL;
    int count = 0;
    int number;

    // Legge i numeri dal file
    while (fscanf(file, "%d", &number) == 1) {
        // Riapplica dinamicamente la memoria
        arr = (int*)realloc(arr, (count + 1) * sizeof(int));
        if (arr == NULL) {
            printf("Errore di allocazione della memoria\n");
            fclose(file);
            return 1;
        }
        arr[count] = number;
        count++;
    }
    fclose(file);

    if (count == 0) {
        printf("Il file 'input.txt' è vuoto o non contiene numeri validi.\n");
        if (arr != NULL) free(arr);
        return 0;
    }
    
    printf("Array non ordinato: ");
    printArray(arr, count);

    mergeSort(arr, 0, count - 1);
    
    printf("Array ordinato: ");
    printArray(arr, count);

    free(arr); // Libera la memoria allocata dinamicamente
    return 0;
}