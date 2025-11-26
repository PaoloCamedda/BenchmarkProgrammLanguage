use std::fs;
use std::path::Path;

// Funzione di Merge
fn merge(left: Vec<i32>, right: Vec<i32>) -> Vec<i32> {
    let mut result = Vec::new();
    let mut i = 0;
    let mut j = 0;

    // Confronta e fonde
    while i < left.len() && j < right.len() {
        if left[i] < right[j] {
            result.push(left[i]);
            i += 1;
        } else {
            result.push(right[j]);
            j += 1;
        }
    }

    // Aggiungi i rimanenti
    result.extend_from_slice(&left[i..]);
    result.extend_from_slice(&right[j..]);

    result
}

// Funzione principale di Merge Sort
fn merge_sort(arr: Vec<i32>) -> Vec<i32> {
    if arr.len() <= 1 {
        return arr;
    }

    // 1. DIVIDI
    let mid = arr.len() / 2;
    let (left, right) = arr.split_at(mid);

    // 2. RICORRI e 3. CONQUISTA (MERGE)
    let sorted_left = merge_sort(left.to_vec());
    let sorted_right = merge_sort(right.to_vec());

    merge(sorted_left, sorted_right)
}

// --- Gestione Input/Output ---
fn main() {
    let path = Path::new("input.txt");
    
    // 1. Legge il file
    let content = match fs::read_to_string(path) {
        Ok(c) => c,
        Err(_) => {
            println!("Errore: il file 'input.txt' non è stato trovato.");
            return;
        }
    };

    // 2. Parsa i dati
    let arr: Vec<i32> = content
        .split_whitespace() // Dividi per qualsiasi spazio bianco
        .filter_map(|s| s.parse::<i32>().ok()) // Prova a convertire in i32
        .collect();

    if arr.is_empty() {
        println!("Il file 'input.txt' è vuoto o non contiene numeri validi.");
        return;
    }

    println!("Array non ordinato: {:?}", arr);
    
    // Esegue il Merge Sort
    let sorted_arr = merge_sort(arr);
    
    println!("Array ordinato: {:?}", sorted_arr);
}