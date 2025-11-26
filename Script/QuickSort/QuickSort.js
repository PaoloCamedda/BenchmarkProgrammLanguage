const fs = require('fs');

// Funzione di utilità per lo scambio (swap)
function swap(arr, i, j) {
    [arr[i], arr[j]] = [arr[j], arr[i]];
}

// Funzione di Partizione
function partition(arr, low, high) {
    let pivot = arr[high];
    let i = low - 1; // Indice dell'elemento più piccolo

    for (let j = low; j < high; j++) {
        // Se l'elemento corrente è più piccolo o uguale al pivot
        if (arr[j] <= pivot) {
            i++;
            swap(arr, i, j);
        }
    }
    // Scambia il pivot con l'elemento in arr[i + 1]
    swap(arr, i + 1, high);
    return i + 1;
}

// Funzione principale di Quick Sort
function quickSort(arr, low, high) {
    if (low < high) {
        let pi = partition(arr, low, high);

        // Ordina separatamente gli elementi prima e dopo la partizione
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// --- Gestione Input/Output (Node.js) ---
try {
    const data = fs.readFileSync('input.txt', 'utf8');
    
    const arr = data
        .trim() 
        .split(/\s+/) 
        .map(Number)
        .filter(n => !isNaN(n));

    console.log("Array non ordinato:", arr);
    quickSort(arr, 0, arr.length - 1);
    console.log("Array ordinato:", arr);

} catch (err) {
    if (err.code === 'ENOENT') {
        console.error("Errore: il file 'input.txt' non è stato trovato.");
    } else {
        console.error("Si è verificato un errore:", err.message);
    }
}