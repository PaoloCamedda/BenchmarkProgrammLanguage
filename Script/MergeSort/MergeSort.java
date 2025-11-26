import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class MergeSort {

    // Funzione principale di Merge Sort
    public static void mergeSort(int[] arr, int n) {
        if (n < 2) {
            return;
        }
        int mid = n / 2;
        int[] left = new int[mid];
        int[] right = new int[n - mid];

        // Copia degli elementi
        System.arraycopy(arr, 0, left, 0, mid);
        System.arraycopy(arr, mid, right, 0, n - mid);

        // Ricorsione
        mergeSort(left, mid);
        mergeSort(right, n - mid);

        // Fusione
        merge(arr, left, right, mid, n - mid);
    }

    // Funzione di Merge (fusione)
    public static void merge(int[] arr, int[] left, int[] right, int leftLen, int rightLen) {
        int i = 0, j = 0, k = 0; // i: puntatore left, j: puntatore right, k: puntatore arr

        while (i < leftLen && j < rightLen) {
            if (left[i] <= right[j]) {
                arr[k++] = left[i++];
            } else {
                arr[k++] = right[j++];
            }
        }
        // Aggiungi i rimanenti
        while (i < leftLen) {
            arr[k++] = left[i++];
        }
        while (j < rightLen) {
            arr[k++] = right[j++];
        }
    }
    
    // --- Gestione Input/Output ---
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>();
        
        try (Scanner scanner = new Scanner(new File("input.txt"))) {
            while (scanner.hasNextInt()) {
                list.add(scanner.nextInt());
            }
        } catch (FileNotFoundException e) {
            System.out.println("Errore: File 'input.txt' non trovato.");
            return;
        }
        
        // Converte la List<Integer> in un array primitivo int[]
        int[] arr = list.stream().mapToInt(i -> i).toArray();

        System.out.println("Array non ordinato: " + Arrays.toString(arr));
        mergeSort(arr, arr.length);
        System.out.println("Array ordinato: " + Arrays.toString(arr));
    }
}