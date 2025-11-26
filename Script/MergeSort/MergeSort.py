def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # 1. DIVIDI
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    # 2. RICORRI
    left = merge_sort(left)
    right = merge_sort(right)

    # 3. CONQUISTA (MERGE)
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Aggiungi i rimanenti
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# --- Gestione Input/Output ---
def main():
    try:
        with open('input.txt', 'r') as f:
            # Leggi i numeri, rimuovi spazi bianchi e li converte in interi
            data_str = f.read().split()
            arr = [int(x) for x in data_str if x.isdigit()]
            
            print("Array non ordinato:", arr)
            sorted_arr = merge_sort(arr)
            print("Array ordinato:", sorted_arr)

    except FileNotFoundError:
        print("Errore: il file 'input.txt' non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

if __name__ == "__main__":
    main()