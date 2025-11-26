import sys
import os

sys.setrecursionlimit(2000)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def parse_ints(text):
    vals = []
    for tok in text.split():
        try:
            vals.append(int(tok))
        except ValueError:
            continue
    return vals

def main():
    # Il file contenitore che elenca i percorsi dei file da leggere
    file_list = "files.txt"

    try:
        with open(file_list, "r") as f:
            paths = [line.strip() for line in f if line.strip()]

        all_numbers = []
        for path in paths:
            if os.path.isfile(path):
                with open(path, "r") as infile:
                    all_numbers.extend(parse_ints(infile.read()))
            else:
                print(f"Attenzione: file non trovato -> {path}")

        if not all_numbers:
            print("Errore: nessun numero valido trovato.")
            return

        print("Array non ordinato:", all_numbers)
        quick_sort(all_numbers, 0, len(all_numbers) - 1)
        print("Array ordinato:", all_numbers)

    except FileNotFoundError:
        print(f"Errore: il file lista '{file_list}' non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")

if __name__ == "__main__":
    main()
