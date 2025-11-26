import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class QuickSort {

    // Scambia due elementi nell'array
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    // Funzione di Partizione
    private static int partition(int[] arr, int low, int high) {
        // Scegli l'elemento più a destra come pivot
        int pivot = arr[high];
        
        // Indice dell'elemento più piccolo
        int i = (low - 1); 

        for (int j = low; j < high; j++) {
            // Se l'elemento corrente è più piccolo o uguale al pivot
            if (arr[j] <= pivot) {
                i++;
                // Scambia arr[i] e arr[j]
                swap(arr, i, j);
            }
        }

        // Scambia il pivot con l'elemento in arr[i + 1]
        swap(arr, i + 1, high);
        return (i + 1);
    }

    // Funzione principale di Quick Sort
    public static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // pi è l'indice di partizionamento, arr[pi] è ora al posto giusto
            int pi = partition(arr, low, high);

            // Ricorsione
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
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
        
        int[] arr = list.stream().mapToInt(i -> i).toArray();

        System.out.println("Array non ordinato: " + Arrays.toString(arr));
        quickSort(arr, 0, arr.length - 1);
        System.out.println("Array ordinato: " + Arrays.toString(arr));
    }
}