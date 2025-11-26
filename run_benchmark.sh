#!/bin/bash

# Uso:
# ./run_benchmark.sh -r 5 -w 2 -n 20 -a fib -t it -l c,java
# ./run_benchmark.sh -r 5 -w 0 -n 1-30:1 -a all -t all -l all
# ./run_benchmark.sh -r 5 -w 0 -n 5-20:5 -a fib -t rc -l py

# === Parametri opzionali ===================================================================
runs=10       # default numero di runs
warps=0       # default numero di warmup
input=10      # default input numerico
algos="all"
tipi="all"
langs="all"

while getopts "r:w:n:a:t:l:dh" opt; do
  case $opt in
    r) runs=$OPTARG ;;
    w) warps=$OPTARG ;;
    n) input=$OPTARG ;;
    a) algos=$OPTARG ;;
    t) tipi=$OPTARG ;;
    l) langs=$OPTARG ;;
    d) clean=true ;;
    h)
      echo "Uso: $0 [opzioni]"
      echo "  -r <runs>        Numero di runs (default 10)"
      echo "  -w <warmup>      Numero di warmup (default 0)"
      echo "  -n <input|range> Input singolo o range (es. 20 oppure 1-30:1) gli array di ordinamento non funzionano con range poiche n diventa la lunghezza dell array"
      echo "  -a <algoritmi>   Algoritmi (es. fib,fat,ms,qs oppure all ma non funziona per ora all)"
      echo "  -t <tipi>        Tipi (es. it,rc oppure all)"
      echo "  -l <linguaggi>   Linguaggi (es. c,java,py oppure all)"
      echo "  -d <delete>      Ripulisce i file in Results/raw e input.txtprima di eseguire"
      hyperfine -h
      exit 0
      ;;
    *)
      echo "Uso: $0 -r <runs> -w <warmup> -n <input|range> -a <algoritmi> -t <tipi> -l <linguaggi> [-d]"
      exit 1
      ;;
  esac
done
shift $((OPTIND-1))


BASE_DIR="$(pwd)/Script"
RESULT_DIR="$(pwd)/Results/raw"
mkdir -p "$RESULT_DIR"

if [ "$clean" = true ]; then
    echo "⥁   Pulizia dei file in $RESULT_DIR..."
    rm -f "$RESULT_DIR"/*_time.json "$RESULT_DIR"/*_energy.txt "$RESULT_DIR"/tmp_*.json
fi


# === Mappa abbreviazioni ===================================================================
declare -A algo_map=( ["fib"]="Fibonacci" ["fat"]="Fattoriale"  ["ms"]="MergeSort" ["qs"]="QuickSort")
declare -A tipo_map=( ["it"]="iterativo" ["rc"]="ricorsivo" )
declare -A lang_map=( ["c"]="c" ["java"]="java" ["py"]="python" ["rs"]="rs" ["js"]="js" )


# === Funzione creazione input per mergesort e quicksort=====================================
generate_input_file() {
    local size=$1
    local file="$(pwd)/input.txt"   # file unico nella root Benchmark

    if [ "$clean" = true ] || [ ! -f "$file" ]; then
        echo "⥁   Genero nuovo input.txt con $size numeri casuali"
        shuf -i 1-1000 -n "$size" > "$file"
    fi
}




# === Funzione per eseguire un singolo test =================================================
run_one() {
    local algo=$1
    local tipo=$2
    local lang=$3

    # Cartella sorgente
    if [[ "$algo" == "MergeSort" || "$algo" == "QuickSort" ]]; then
        dir="$BASE_DIR/$algo"   # cartella unica senza _tipo
        # Genera input.txt nella root Benchmark
        generate_input_file "$input"
        input_arg="$(pwd)/input.txt"   # path assoluto del file
    else
        dir="$BASE_DIR/${algo}_${tipo}"
        input_arg="$input"            # per Fibonacci/Fattoriale resta l'argomento numerico
    fi

    echo "⟶  Profiling $algo $tipo in $lang (runs=$runs, warmup=$warps, input=$input)"

    time_file="$RESULT_DIR/${algo}_${tipo}_${lang}_time.json"
    energy_file="$RESULT_DIR/${algo}_${tipo}_${lang}_energy.txt"

    # --- Compilazione / preparazione ---
    case $lang in
        c)
            gcc "$dir/$algo.c" -o "$dir/$algo.c.out"
            tmp_file="$RESULT_DIR/tmp_${algo}_${tipo}_${lang}_${input}_time.json"
            hyperfine --runs $runs --warmup $warps \
                --export-json "$tmp_file" "$dir/$algo.c.out $input_arg"
            cat "$tmp_file" >> "$time_file"; rm "$tmp_file"
            ;;
        rs)
            rustc "$dir/$algo.rs" -o "$dir/$algo.rs.out"
            tmp_file="$RESULT_DIR/tmp_${algo}_${tipo}_${lang}_${input}_time.json"
            hyperfine --runs $runs --warmup $warps \
                --export-json "$tmp_file" "$dir/$algo.rs.out $input_arg"
            cat "$tmp_file" >> "$time_file"; rm "$tmp_file"
            ;;
        java)
            javac "$dir/$algo.java"
            tmp_file="$RESULT_DIR/tmp_${algo}_${tipo}_${lang}_${input}_time.json"
            hyperfine --runs $runs --warmup $warps \
                --export-json "$tmp_file" "java -cp $dir $algo $input_arg"
            cat "$tmp_file" >> "$time_file"; rm "$tmp_file"
            ;;
        js)
            tmp_file="$RESULT_DIR/tmp_${algo}_${tipo}_${lang}_${input}_time.json"
            hyperfine --runs $runs --warmup $warps \
                --export-json "$tmp_file" "node $dir/$algo.js $input_arg"
            cat "$tmp_file" >> "$time_file"; rm "$tmp_file"
            ;;
        py|python)
            tmp_file="$RESULT_DIR/tmp_${algo}_${tipo}_${lang}_${input}_time.json"
            hyperfine --runs $runs --warmup $warps \
                --export-json "$tmp_file" "python3 $dir/$algo.py $input_arg"
            cat "$tmp_file" >> "$time_file"; rm "$tmp_file"
            ;;
        *)
            echo "⤬ Linguaggio non supportato: $lang"
            return
            ;;
    esac

    # --- Energia ---
    total_pkg=0
    total_dram=0
    dram_available=false
    if [ -f /sys/class/powercap/intel-rapl:0:1/energy_uj ]; then
        dram_available=true
    fi

    for i in $(seq 1 $runs); do
        start_pkg=$(sudo cat /sys/class/powercap/intel-rapl:0/energy_uj 2>/dev/null || echo 0)
        if $dram_available; then
            start_dram=$(sudo cat /sys/class/powercap/intel-rapl:0:1/energy_uj 2>/dev/null || echo 0)
        fi

        # esecuzione programma
        case $lang in
            c) "$dir/$algo.c.out" "$input_arg" > /dev/null ;;
            rs) "$dir/$algo.rs.out" "$input_arg" > /dev/null ;;
            java) java -cp "$dir" "$algo" "$input_arg" > /dev/null ;;
            js) node "$dir/$algo.js" "$input_arg" > /dev/null ;;
            py|python) python3 "$dir/$algo.py" "$input_arg" > /dev/null ;;
        esac

        end_pkg=$(sudo cat /sys/class/powercap/intel-rapl:0/energy_uj 2>/dev/null || echo 0)
        run_energy_pkg=$((end_pkg - start_pkg))
        echo "$algo;$tipo;$lang;$input;$i;PKG;$run_energy_pkg" >> "$energy_file"
        total_pkg=$((total_pkg + run_energy_pkg))

        if $dram_available; then
            end_dram=$(sudo cat /sys/class/powercap/intel-rapl:0:1/energy_uj 2>/dev/null || echo 0)
            run_energy_dram=$((end_dram - start_dram))
            echo "$algo;$tipo;$lang;$input;$i;DRAM;$run_energy_dram" >> "$energy_file"
            total_dram=$((total_dram + run_energy_dram))
        fi
    done

    avg_pkg=$((total_pkg / runs))
    echo "$algo;$tipo;$lang;$input;avg;PKG;$avg_pkg" >> "$energy_file"

    if $dram_available; then
        avg_dram=$((total_dram / runs))
        echo "$algo;$tipo;$lang;$input;avg;DRAM;$avg_dram" >> "$energy_file"
    fi
}




# === Gestione input come range ============================================================
inputs=()
if [[ "$input" =~ ^[0-9]+-[0-9]+:[0-9]+$ ]]; then
    start=$(echo "$input" | cut -d'-' -f1)
    end=$(echo "$input" | cut -d'-' -f2 | cut -d':' -f1)
    step=$(echo "$input" | cut -d':' -f2)
    inputs=($(seq $start $step $end))
else
    inputs=("$input")
fi

# === Costruzione lista test ================================================================
tests=()
IFS=',' read -ra algo_list <<< "$algos"
IFS=',' read -ra tipo_list <<< "$tipi"
IFS=',' read -ra lang_list <<< "$langs"

is_sort_algo() {
    [[ "$1" == "MergeSort" || "$1" == "QuickSort" ]]
}

# Helper: aggiungi test per una cartella algoritmo con estensioni presenti
add_tests_for_dir() {
    local algo_name="$1"
    local tipo_name="$2"   # può essere "ricorsivo" per ms/qs
    local dir="$3"

    if [ "${lang_list[0]}" = "all" ]; then
        # rileva le implementazioni disponibili
        for f in "$dir"/*; do
            ext="${f##*.}"
            case "$ext" in c|java|js|py|rs)
                tests+=("$algo_name;$tipo_name;$ext")
                ;;
            esac
        done
    else
        # lingue specifiche
        for l in "${lang_list[@]}"; do
            lang=${lang_map[$l]:-$l}
            tests+=("$algo_name;$tipo_name;$lang")
        done
    fi
}

for a in "${algo_list[@]}"; do
    algo=${algo_map[$a]:-$a}

    if [ "$algo" = "all" ]; then
        # Scansione directory Script/* (gestisce anche MergeSort/QuickSort)
        for d in "$BASE_DIR"/*; do
            base=$(basename "$d")
            if [[ "$base" == *"_"* ]]; then
                algo_name="${base%%_*}"
                tipo_name="${base##*_}"
                add_tests_for_dir "$algo_name" "$tipo_name" "$d"
            else
                # directory senza tipo (es. MergeSort, QuickSort)
                algo_name="$base"
                tipo_name="ricorsivo"
                add_tests_for_dir "$algo_name" "$tipo_name" "$d"
            fi
        done
    else
        if is_sort_algo "$algo"; then
            # MergeSort/QuickSort: cartella senza _tipo, forziamo "ricorsivo"
            dir="$BASE_DIR/$algo"
            tipo_name="ricorsivo"
            add_tests_for_dir "$algo" "$tipo_name" "$dir"
        else
            # Algoritmi con tipo (Fibonacci/Fattoriale)
            for t in "${tipo_list[@]}"; do
                tipo=${tipo_map[$t]:-$t}
                dir="$BASE_DIR/${algo}_${tipo}"
                add_tests_for_dir "$algo" "$tipo" "$dir"
            done
        fi
    fi
done

total=${#tests[@]}
count=0

# === Loop con progress bar ================================================================
total=${#tests[@]}
count=0

if (( total == 0 )); then
  echo "⤬ Nessun test da eseguire (total=0)."
else
  for t in "${tests[@]}"; do
      count=$((count+1))
      algo=$(echo "$t" | cut -d';' -f1)
      tipo=$(echo "$t" | cut -d';' -f2)
      lang=$(echo "$t" | cut -d';' -f3)

      percent=$((count*100/total))
      bar=$(printf "%-${total}s" | tr ' ' '#')
      bar="${bar:0:$count}"

      # Riga di stato in-place
      echo -ne "[$bar] ${percent}% - $algo $tipo $lang\r"

      for in_val in "${inputs[@]}"; do
          input=$in_val
          # Riga di log persistente
          echo
          echo "➢  Eseguo $algo $tipo $lang con input=$input"
          run_one "$algo" "$tipo" "$lang"
      done
  done
  echo # newline finale per non lasciare la \r sulla stessa riga
fi


echo -e "\n⟶ Tutti i $total test completati"
