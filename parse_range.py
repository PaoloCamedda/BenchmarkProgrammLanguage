import json
import csv
import glob
import os
import sys
import numpy as np

# Directory di input/output
RESULT_DIR = "Results/raw"
OUTPUT_CSV = "Results/csv/benchmark_range.csv"

# Opzionale: consenti passaggio range via CLI (es. 10-50:20 o singolo 30)
def parse_range_arg():
    if len(sys.argv) >= 2:
        s = sys.argv[1]
        if "-" in s and ":" in s:
            start, rest = s.split("-", 1)
            end, step = rest.split(":", 1)
            return [str(v) for v in range(int(start), int(end) + 1, int(step))]
        else:
            try:
                return [str(int(s))]
            except ValueError:
                pass
    return None

rows = []

# Scansiona tutti i file tempo concatenati via cat
for json_file in glob.glob(os.path.join(RESULT_DIR, "*_time.json")):
    base = os.path.basename(json_file).replace("_time.json", "")
    try:
        algo, tipo, lang = base.split("_")
    except ValueError:
        print(f"⤬ Nome file non riconosciuto: {base}")
        continue

    # --- Leggi JSON Hyperfine concatenati (più input) ---
    with open(json_file, "r") as f:
        content = f.read().strip()
        decoder = json.JSONDecoder()
        idx = 0
        objs = []
        while idx < len(content):
            obj, end = decoder.raw_decode(content, idx)
            objs.append(obj)
            idx = end
            while idx < len(content) and content[idx].isspace():
                idx += 1

    # --- Leggi energia associata ---
    energy_file = os.path.join(RESULT_DIR, f"{base}_energy.txt")
    energy_data = {}  # (input_str, dominio) -> lista valori (µJ)
    avg_map = {}      # (input_str, dominio) -> media (µJ) calcolata nello script bash

    if os.path.exists(energy_file):
        with open(energy_file, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) != 7:
                    continue
                algo_f, tipo_f, lang_f, input_f, run, dominio, val = parts
                if algo_f != algo or tipo_f != tipo or lang_f != lang:
                    continue
                try:
                    val_int = int(val)
                except ValueError:
                    continue
                key = (input_f, dominio)
                if run == "avg":
                    avg_map[key] = val_int
                else:
                    energy_data.setdefault(key, []).append(val_int)
    else:
        print(f"⚠️ File energia mancante: {energy_file}")

    inputs_from_energy = sorted({k[0] for k in energy_data.keys()}, key=lambda x: int(x)) if energy_data else []
    inputs_from_cli = parse_range_arg()
    if inputs_from_cli is not None and set(inputs_from_cli) == set(inputs_from_energy) and inputs_from_energy:
        input_values = inputs_from_cli
    elif inputs_from_energy:
        input_values = inputs_from_energy
    else:
        input_values = [str(i) for i in range(1, len(objs) + 1)]

    if len(objs) != len(input_values):
        print(f"⚠️ Mismatch blocchi: {base} json={len(objs)} inputs={len(input_values)}")
    n = min(len(objs), len(input_values))

    for idx in range(n):
        input_val_raw = input_values[idx].strip()
        if input_val_raw.startswith("input_") and input_val_raw.endswith(".txt"):
            input_val_raw = input_val_raw.replace("input_", "").replace(".txt", "")

        stats_block = objs[idx]["results"][0]
        tempo_medio = stats_block.get("mean")
        deviazione_tempo = stats_block.get("stddev")
        minimo_tempo = stats_block.get("min")
        massimo_tempo = stats_block.get("max")

        stats_map = {}

        for dominio in ["PKG", "DRAM"]:
            key = (input_val_raw, dominio)
            if key in energy_data:
                values_uj = energy_data[key]
                values_j = [v / 1e6 for v in values_uj]
                if key in avg_map:
                    media_j = avg_map[key] / 1e6
                else:
                    media_j = float(np.mean(values_j))
                std_j = float(np.std(values_j, ddof=1)) if len(values_j) > 1 else 0.0
                min_j = float(min(values_j))
                max_j = float(max(values_j))
                stats_map[dominio] = {"media": media_j, "std": std_j, "min": min_j, "max": max_j}

        if "DRAM" not in stats_map:
            stats_map["DRAM"] = {"media": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}
        if "PKG" not in stats_map:
            stats_map["PKG"] = {"media": None, "std": None, "min": None, "max": None}

        pkg = stats_map["PKG"]
        dram = stats_map["DRAM"]
        if pkg["media"] is not None:
            energia_totale_media = (pkg["media"] or 0.0) + (dram["media"] or 0.0)
            energia_totale_std = np.sqrt((pkg["std"] or 0.0) ** 2 + (dram["std"] or 0.0) ** 2)
            energia_totale_min = (pkg["min"] or 0.0) + (dram["min"] or 0.0)
            energia_totale_max = (pkg["max"] or 0.0) + (dram["max"] or 0.0)
        else:
            energia_totale_media = energia_totale_std = energia_totale_min = energia_totale_max = None

        try:
            input_val_num = int(input_val_raw)
        except ValueError:
            input_val_num = input_val_raw

        rows.append([
            algo, tipo, lang, input_val_num,
            tempo_medio, deviazione_tempo, minimo_tempo, massimo_tempo,
            stats_map["PKG"]["media"], stats_map["PKG"]["std"], stats_map["PKG"]["min"], stats_map["PKG"]["max"],
            stats_map["DRAM"]["media"], stats_map["DRAM"]["std"], stats_map["DRAM"]["min"], stats_map["DRAM"]["max"],
            energia_totale_media, energia_totale_std, energia_totale_min, energia_totale_max
        ])

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
rows.sort()
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "algoritmo", "tipo", "linguaggio", "input",
        "tempo_medio", "deviazione_tempo", "min_tempo", "max_tempo",
        "energia_media_pkg_j", "deviazione_energia_pkg_j", "min_energia_pkg_j", "max_energia_pkg_j",
        "energia_media_dram_j", "deviazione_energia_dram_j", "min_energia_dram_j", "max_energia_dram_j",
        "energia_tot_j", "deviazione_energia_tot_j", "min_energia_tot_j", "max_energia_tot_j"
    ])
    writer.writerows(rows)

print(f"⟶ CSV generato: {OUTPUT_CSV}")
