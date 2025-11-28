import json
import csv
import glob
import os
import numpy as np

RESULT_DIR = "Results/raw"
OUTPUT_CSV = "Results/csv/benchmark_range.csv"

rows = []

for json_file in glob.glob(os.path.join(RESULT_DIR, "*_time.json")):
    base = os.path.basename(json_file).replace("_time.json", "")
    try:
        algo, tipo, lang = base.split("_")
    except ValueError:
        print(f"⤬ Nome file non riconosciuto: {base}")
        continue

    # === Leggi JSON Hyperfine (può esserci più input) ===
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

    # === Leggi energia (più blocchi, con dominio) ===
    energy_file = os.path.join(RESULT_DIR, f"{base}_energy.txt")
    if os.path.exists(energy_file):
        energy_data = {}   # dict: (input, dominio) -> valori run
        avg_map = {}       # dict: (input, dominio) -> valore medio

        with open(energy_file, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                # formato: algo;tipo;lang;input;run;dominio;valore
                if len(parts) != 7:
                    continue
                algo_f, tipo_f, lang_f, input_f, run, dominio, val = parts
                val_int = int(val)
                key = (input_f, dominio)

                if run == "avg":
                    avg_map[key] = val_int
                else:
                    energy_data.setdefault(key, []).append(val_int)

        # Calcola statistiche per ogni input
        for input_val in set(k[0] for k in energy_data.keys()):

            if input_val.startswith("input_") and input_val.endswith(".txt"):
                input_val = input_val.replace("input_", "").replace(".txt", "")

            stats_map = {}
            for dominio in ["PKG", "DRAM"]:
                key = (input_val, dominio)
                if key in energy_data and key in avg_map:
                    values_uj = energy_data[key]
                    energia_media_uj = avg_map[key]
                    values_j = [v / 1e6 for v in values_uj]
                    media_j = energia_media_uj / 1e6
                    std_j = float(np.std(values_j, ddof=1))
                    min_j = min(values_j)
                    max_j = max(values_j)
                    stats_map[dominio] = (media_j, std_j, min_j, max_j)

            # prendi tempo dal primo blocco Hyperfine (semplificazione)
            stats = objs[0]["results"][0]
            tempo_medio = stats["mean"]
            deviazione_tempo = stats["stddev"]
            minimo_tempo = stats["min"]
            massimo_tempo = stats["max"]

            # Calcola totale se hai PKG + DRAM
            energia_totale_media = energia_totale_std = energia_totale_min = energia_totale_max = None
            if "PKG" in stats_map and "DRAM" in stats_map:
                pkg = stats_map["PKG"]
                dram = stats_map["DRAM"]
                energia_totale_media = pkg[0] + dram[0]
                energia_totale_std   = np.sqrt(pkg[1]**2 + dram[1]**2)
                energia_totale_min   = pkg[2] + dram[2]
                energia_totale_max   = pkg[3] + dram[3]

            # Scrivi una sola riga con tutte le colonne
            rows.append([
                algo, tipo, lang, input_val,
                tempo_medio, deviazione_tempo, minimo_tempo, massimo_tempo,
                stats_map["PKG"][0] if "PKG" in stats_map else None,
                stats_map["PKG"][1] if "PKG" in stats_map else None,
                stats_map["PKG"][2] if "PKG" in stats_map else None,
                stats_map["PKG"][3] if "PKG" in stats_map else None,
                stats_map["DRAM"][0] if "DRAM" in stats_map else None,
                stats_map["DRAM"][1] if "DRAM" in stats_map else None,
                stats_map["DRAM"][2] if "DRAM" in stats_map else None,
                stats_map["DRAM"][3] if "DRAM" in stats_map else None,
                energia_totale_media, energia_totale_std, energia_totale_min, energia_totale_max
            ])

# === Scrivi CSV ===
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
