#!/bin/bash
set -u

# Uso:
# ./run_benchmark.sh -r 5 -w 2 -n 20 -a fib -t it -l c,java
# ./run_benchmark.sh -r 5 -w 0 -n 100-5000:100 -a ms,qs -l all -N

runs=10
warps=0
input=10
algos="all"
tipi="all"
langs="all"
noshell=false
clean=false

while getopts "r:w:n:a:t:l:dhN" opt; do
  case $opt in
    r) runs=$OPTARG ;;
    w) warps=$OPTARG ;;
    n) input=$OPTARG ;;
    a) algos=$OPTARG ;;
    t) tipi=$OPTARG ;;
    l) langs=$OPTARG ;;
    d) clean=true ;;
    N) noshell=true ;;
    h)
      echo "Uso: $0 [opzioni]"
      echo "  -r <runs>        Numero di runs (default 10)"
      echo "  -w <warmup>      Numero di warmup (default 0)"
      echo "  -n <input|range> Input singolo o range (es. 20 oppure 100-5000:100)"
      echo "  -a <algoritmi>   Algoritmi (fib,fat,ms,qs oppure all)"
      echo "  -t <tipi>        Tipi (it,rc oppure all)"
      echo "  -l <linguaggi>   Linguaggi (c,java,py,js,rs oppure all)"
      echo "  -d               Ripulisce Results/raw e input_*.txt"
      echo "  -N               Usa hyperfine con --shell=none"
      exit 0
      ;;
    *) exit 1 ;;
  esac
done
shift $((OPTIND-1))

PROJECT_ROOT="$(pwd)"
BASE_DIR="$PROJECT_ROOT/Script"
RESULT_DIR="$PROJECT_ROOT/Results/raw"
mkdir -p "$RESULT_DIR"

if [ "$clean" = true ]; then
    echo "⥁   Pulizia dei file in $RESULT_DIR..."
    rm -f "$RESULT_DIR"/* "$PROJECT_ROOT"/input_*.txt
fi

declare -A algo_map=( ["fib"]="Fibonacci" ["fat"]="Fattoriale" ["ms"]="MergeSort" ["qs"]="QuickSort" )
declare -A tipo_map=( ["it"]="iterativo" ["rc"]="ricorsivo" )
declare -A lang_map=( ["c"]="c" ["java"]="java" ["py"]="python" ["rs"]="rs" ["js"]="js" )

is_sort_algo() { [[ "$1" == "MergeSort" || "$1" == "QuickSort" ]]; }

# Genera input unico e symlink
generate_input_file() {
    local size=$1
    local file="$PROJECT_ROOT/input_${size}.txt"
    echo "⥁   Genero nuovo input_${size}.txt con $size numeri casuali"
    shuf -i 1-10000000 -n "$size" > "$file"
    ln -sf "$file" "$BASE_DIR/MergeSort/input.txt"
    ln -sf "$file" "$BASE_DIR/QuickSort/input.txt"
}
# === Funzione =================== 

run_one() {
    local algo=$1 tipo=$2 lang=$3

    # Determina la cartella sorgente e l'argomento da passare
    if is_sort_algo "$algo"; then
        dir="$BASE_DIR/$algo"
        input_arg=""   # nessun argomento: i programmi aprono input.txt da soli
    else
        dir="$BASE_DIR/${algo}_${tipo}"
        input_arg="$input"   # numero da passare come argomento
    fi

    echo "⟶  Profiling $algo $tipo in $lang (runs=$runs, warmup=$warps, input=$input)"

    time_file="$RESULT_DIR/${algo}_${tipo}_${lang}_time.json"
    tmp_file="$RESULT_DIR/tmp_${algo}_${tipo}_${lang}_${input}_time.json"

    hf_opts=(--runs "$runs" --warmup "$warps" --export-json "$tmp_file")
    [ "$noshell" = true ] && hf_opts+=(--shell=none)

    case $lang in
        c)
            gcc "$dir/$algo.c" -O2 -o "$dir/$algo.c.out" || return 1
            if [ -n "$input_arg" ]; then
                hyperfine "${hf_opts[@]}" "$dir/$algo.c.out $input_arg"
            else
                hyperfine "${hf_opts[@]}" "$dir/$algo.c.out"
            fi
            ;;
        rs)
            rustc "$dir/$algo.rs" -o "$dir/$algo.rs.out" || return 1
            if [ -n "$input_arg" ]; then
                hyperfine "${hf_opts[@]}" "$dir/$algo.rs.out $input_arg"
            else
                hyperfine "${hf_opts[@]}" "$dir/$algo.rs.out"
            fi
            ;;
        java)
            javac "$dir/$algo.java" || return 1
            if [ -n "$input_arg" ]; then
                hyperfine "${hf_opts[@]}" "java -cp $dir $algo $input_arg"
            else
                hyperfine "${hf_opts[@]}" "java -cp $dir $algo"
            fi
            ;;
        js)
            if [ -n "$input_arg" ]; then
                hyperfine "${hf_opts[@]}" "node $dir/$algo.js $input_arg"
            else
                hyperfine "${hf_opts[@]}" "node $dir/$algo.js"
            fi
            ;;
        py|python)
            if [ -n "$input_arg" ]; then
                hyperfine "${hf_opts[@]}" "python3 $dir/$algo.py $input_arg"
            else
                hyperfine "${hf_opts[@]}" "python3 $dir/$algo.py"
            fi
            ;;
        *)
            echo "⤬ Linguaggio non supportato: $lang"
            return
            ;;
    esac

    cat "$tmp_file" >> "$time_file"; rm -f "$tmp_file"
}

# === Gestione input come range =========================
inputs=()
if [[ "$input" =~ ^[0-9]+-[0-9]+:[0-9]+$ ]]; then
    start=${input%-*}
    end_step=${input#*-}
    end=${end_step%:*}
    step=${end_step#*:}
    inputs=($(seq "$start" "$step" "$end"))
else
    inputs=("$input")
fi

tests=()
IFS=',' read -ra algo_list <<< "$algos"
IFS=',' read -ra tipo_list <<< "$tipi"
IFS=',' read -ra lang_list <<< "$langs"

add_tests_for_dir() {
    local algo_name="$1" tipo_name="$2" dir="$3"
    if [ "${lang_list[0]}" = "all" ]; then
        for f in "$dir"/*; do
            ext="${f##*.}"
            case "$ext" in c|java|js|py|rs) tests+=("$algo_name;$tipo_name;$ext");; esac
        done
    else
        for l in "${lang_list[@]}"; do
            lang=${lang_map[$l]:-$l}
            tests+=("$algo_name;$tipo_name;$lang")
        done
    fi
}

for a in "${algo_list[@]}"; do
    algo=${algo_map[$a]:-$a}
    if [ "$algo" = "all" ]; then
        for d in "$BASE_DIR"/*; do
            base=$(basename "$d")
            if [[ "$base" == *"_"* ]]; then
                add_tests_for_dir "${base%%_*}" "${base##*_}" "$d"
            else
                add_tests_for_dir "$base" "ricorsivo" "$d"
            fi
        done
    else
        if is_sort_algo "$algo"; then
            add_tests_for_dir "$algo" "ricorsivo" "$BASE_DIR/$algo"
        else
            for t in "${tipo_list[@]}"; do
                tipo=${tipo_map[$t]:-$t}
                add_tests_for_dir "$algo" "$tipo" "$BASE_DIR/${algo}_${tipo}"
            done
        fi
    fi
done

total=$(( ${#tests[@]} * ${#inputs[@]} ))
count=0
[ $total -eq 0 ] && { echo "⤬ Nessun test da eseguire"; exit 1; }

for in_val in "${inputs[@]}"; do
    input=$in_val
    if [[ "$algos" == *"ms"* || "$algos" == *"qs"* || "$algos" == "all" ]]; then
        generate_input_file "$input"
    fi
    for t in "${tests[@]}"; do
        count=$((count+1))
        algo=$(echo "$t" | cut -d';' -f1)
        tipo=$(echo "$t" | cut -d';' -f2)
        lang=$(echo "$t" | cut -d';' -f3)
        percent=$((count*100/total))
        bar=$(printf "%-${percent}s" | tr ' ' '#')
        echo -ne "[${bar}] ${percent}% - $algo $tipo $lang (input=$input)\r"
        echo
        echo "➢  Eseguo $algo $tipo $lang con input=$input"
        run_one "$algo" "$tipo" "$lang" || echo "⤬ Fallito: $algo $tipo $lang (input=$input)"
    done
done

echo -e "\n⟶ Tutti i $total test completati"
