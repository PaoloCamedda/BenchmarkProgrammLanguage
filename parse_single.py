import json
import csv
import glob
import os
import numpy as np

RESULT_DIR = "Results/raw"
OUTPUT_CSV = "Results/csv/benchmark_single.csv"

rows = []

for json_file in glob.glob(os.path.join(RESULT_DIR, "*_time.json")):
    base = os.path.basename(json_file).replace("_time.json", "")
    try:
        algo, tipo, lang = base.split("_")
    except ValueError:
        print(f"⤬ Nome file non riconosciuto: {base}")
        continue

    # === Tempo da Hyperfine ===
    with open(json_file, "r") as f:
        data = json.load(f)
        stats = data["results"][0]
        tempo_medio = stats["mean"]
        deviazione_tempo = stats["stddev"]
        minimo_tempo = stats["min"]
        massimo_tempo = stats["max"]

        command = stats["command"]
        parts = command.strip().split()
        input_val = parts[-1] if parts else None

    # === Energia da file TXT ===
    energy_file = os.path.join(RESULT_DIR, f"{base}_energy.txt")

    stats_pkg = stats_dram = None
    energia_totale_media = energia_totale_std = energia_totale_min = energia_totale_max = None

    if os.path.exists(energy_file):
        values_by_domain = {}
        media_by_domain = {}

        with open(energy_file, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) < 7:
                    continue
                run = parts[4]
                dominio = parts[5]
                val = int(parts[6])

                if run != "avg":
                    values_by_domain.setdefault(dominio, []).append(val)
                else:
                    media_by_domain[dominio] = val

        domini_stats = {}
        for dominio, values_uj in values_by_domain.items():
            values_j = [v / 1e6 for v in values_uj]
            # Media: se c'è avg usa quello, altrimenti calcola dai run
            if dominio in media_by_domain:
                media_j = media_by_domain[dominio] / 1e6
            else:
                media_j = float(np.mean(values_j)) if values_j else None

            if values_j:
                std_j = float(np.std(values_j, ddof=1)) if len(values_j) > 1 else 0.0
                min_j = float(min(values_j))
                max_j = float(max(values_j))
            else:
                std_j = min_j = max_j = None

            domini_stats[dominio] = (media_j, std_j, min_j, max_j)

        # estrai PKG e DRAM
        stats_pkg = domini_stats.get("PKG")
        stats_dram = domini_stats.get("DRAM")

        # Fallback: se DRAM manca, forzala a 0.0
        if stats_dram is None:
            stats_dram = (0.0, 0.0, 0.0, 0.0)

        # Totale energia
        if stats_pkg is not None:
            energia_totale_media = (stats_pkg[0] or 0.0) + (stats_dram[0] or 0.0)
            energia_totale_std   = np.sqrt((stats_pkg[1] or 0.0)**2 + (stats_dram[1] or 0.0)**2)
            energia_totale_min   = (stats_pkg[2] or 0.0) + (stats_dram[2] or 0.0)
            energia_totale_max   = (stats_pkg[3] or 0.0) + (stats_dram[3] or 0.0)

    # === Scrivi una sola riga con tutte le colonne ===
    rows.append([
        algo, tipo, lang, input_val,
        tempo_medio, deviazione_tempo, minimo_tempo, massimo_tempo,
        stats_pkg[0] if stats_pkg else None,
        stats_pkg[1] if stats_pkg else None,
        stats_pkg[2] if stats_pkg else None,
        stats_pkg[3] if stats_pkg else None,
        stats_dram[0] if stats_dram else None,
        stats_dram[1] if stats_dram else None,
        stats_dram[2] if stats_dram else None,
        stats_dram[3] if stats_dram else None,
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
