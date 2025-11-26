use std::fs;
use std::path::Path;

// Funzione principale di Quick Sort (lavora in-place su una slice mutabile)
fn quick_sort(arr: &mut [i32]) {
    if arr.len() > 1 {
        // Partiziona e ottieni l'indice del pivot
        let pivot_index = partition(arr);
        
        // Ordina la parte sinistra ricorsivamente
        quick_sort(&mut arr[0..pivot_index]);
        
        // Ordina la parte destra ricorsivamente
        quick_sort(&mut arr[pivot_index + 1..]);
    }
}

// Funzione di Partizione
fn partition(arr: &mut [i32]) -> usize {
    let len = arr.len();
    // Scegli l'elemento più a destra come pivot
    let pivot_value = arr[len - 1]; 
    let mut i = 0; // Puntatore per la sezione minore del pivot

    for j in 0..len - 1 {
        if arr[j] <= pivot_value {
            // Scambia l'elemento corrente con l'elemento in posizione i
            arr.swap(i, j); 
            i += 1;
        }
    }
    // Sposta il pivot nella sua posizione finale
    arr.swap(i, len - 1);
    i // Ritorna l'indice finale del pivot
}

// --- Gestione Input/Output ---
fn main() {
    let path = Path::new("input.txt");
    
    let content = match fs::read_to_string(path) {
        Ok(c) => c,
        Err(_) => {
            println!("Errore: il file 'input.txt' non è stato trovato.");
            return;
        }
    };

    // Parsa i dati
    let mut arr: Vec<i32> = content
        .split_whitespace()
        .filter_map(|s| s.parse::<i32>().ok())
        .collect();

    if arr.is_empty() {
        println!("Il file 'input.txt' è vuoto o non contiene numeri validi.");
        return;
    }

    println!("Array non ordinato: {:?}", arr);
    
    // Esegue il Quick Sort, passando un riferimento mutabile al vettore
    quick_sort(&mut arr);
    
    println!("Array ordinato: {:?}", arr);
}