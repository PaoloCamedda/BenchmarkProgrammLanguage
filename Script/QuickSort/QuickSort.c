#include <stdio.h>
#include <stdlib.h>

// Funzione di utilità per lo scambio (swap)
void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

// Funzione di Partizione (Partition)
int partition(int arr[], int low, int high) {
    // Pivot scelto come elemento più a destra
    int pivot = arr[high]; 
    int i = (low - 1); // Indice del più piccolo elemento

    for (int j = low; j <= high - 1; j++) {
        // Se l'elemento corrente è più piccolo del pivot
        if (arr[j] < pivot) {
            i++; // Incrementa l'indice del piccolo elemento
            swap(&arr[i], &arr[j]);
        }
    }
    // Scambia il pivot (arr[high]) con l'elemento in arr[i+1]
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// Funzione principale di Quick Sort
void quick_sort(int arr[], int low, int high) {
    if (low < high) {
        // pi è l'indice di partizionamento
        int pi = partition(arr, low, high);

        // Ordina ricorsivamente gli elementi prima e dopo la partizione
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
int main() {
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("Errore: impossibile aprire il file 'input.txt'\n");
        return 1;
    }

    int *arr = NULL;
    int count = 0;
    int number;

    // Legge i numeri dal file (stessa logica del Merge Sort C)
    while (fscanf(file, "%d", &number) == 1) {
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

    quick_sort(arr, 0, count - 1);
    
    printf("Array ordinato: ");
    printArray(arr, count);

    free(arr);
    return 0;
}