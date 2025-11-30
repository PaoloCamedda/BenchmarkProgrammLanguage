const fs = require('fs');


function mergeSort(arr) {
    if (arr.length <= 1) {
        return arr;
    }

    // 1. DIVIDI
    const mid = Math.floor(arr.length / 2);
    const left = arr.slice(0, mid);
    const right = arr.slice(mid);

    // 2. RICORRI e 3. CONQUISTA (MERGE)
    return merge(mergeSort(left), mergeSort(right));
}

function merge(left, right) {
    let result = [];
    let i = 0;
    let j = 0;

    while (i < left.length && j < right.length) {
        if (left[i] < right[j]) {
            result.push(left[i]);
            i++;
        } else {
            result.push(right[j]);
            j++;
        }
    }

    // Aggiungi i rimanenti
    return result.concat(left.slice(i)).concat(right.slice(j));
}

// --- Gestione Input/Output (Node.js) ---
try {
    // Legge il contenuto del file come stringa
    const data = fs.readFileSync('Script/MergeSort/input.txt', 'utf8');
    
    // Filtra e converte in numeri interi
    const arr = data
        .trim() // Rimuovi spazi bianchi all'inizio/fine
        .split(/\s+/) // Dividi per qualsiasi spazio bianco (spazi, newline)
        .map(Number)
        .filter(n => !isNaN(n)); // Assicura che sia un numero valido

    console.log("Array non ordinato:", arr);
    const sortedArr = mergeSort(arr);
    console.log("Array ordinato:", sortedArr);

} catch (err) {
    if (err.code === 'ENOENT') {
        console.error("Errore: il file 'input.txt' non è stato trovato.");
    } else {
        console.error("Si è verificato un errore:", err.message);
    }
}