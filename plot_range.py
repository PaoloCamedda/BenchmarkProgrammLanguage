import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
import itertools as it
from matplotlib import ticker


RESULT_CSV = "Results/csv/benchmark_range.csv"
GRAPH_DIR = "Results/Graphic/Range"
os.makedirs(GRAPH_DIR, exist_ok=True)

df = pd.read_csv(RESULT_CSV, delimiter=";")

# Conversione input numerico
df["input_num"] = pd.to_numeric(df["input"], errors="coerce")

# Limiti globali
x_min, x_max = df["input_num"].min(), df["input_num"].max()
tempo_min, tempo_max = df["tempo_medio"].min(), df["tempo_medio"].max()
energia_min, energia_max = df["energia_tot_j"].min(), df["energia_tot_j"].max()

# === Grafico 1: per ogni combinazione algoritmo + linguaggio + tipo ===
for algo in df["algoritmo"].unique():
    for lang in df["linguaggio"].unique():
        for tipo in df["tipo"].unique():
            subset = df[(df["algoritmo"] == algo) &
                        (df["linguaggio"] == lang) &
                        (df["tipo"] == tipo)]
            if subset.empty:
                continue

            s = subset.sort_values("input_num")
            x = s["input_num"].values
            tempo = s["tempo_medio"].values
            tempo_err = s["deviazione_tempo"].values
            energia = s["energia_tot_j"].values
            energia_err = s["deviazione_energia_tot_j"].values
            potenza = energia * tempo

            # 3 subplot: tempo, energia, potenza
            fig, axes = plt.subplots(1, 3, figsize=(18, 5))

            # Tempo
            axes[0].errorbar(x, tempo, yerr=tempo_err, fmt="-o", color="black", label="Tempo medio")
            axes[0].errorbar(x, tempo, yerr=tempo_err, fmt="none", ecolor="red", capsize=4, label="Deviazione")

            axes[0].set_title(f"Tempo medio - {algo} ({lang}, {tipo})")
            axes[0].set_xlabel("Input")
            axes[0].set_ylabel("Tempo medio (s)")
            axes[0].set_xlim(x_min, x_max)

           
            axes[0].set_yscale("log", base=10)
            axes[0].set_ylim(1e-3, 2.0)  # adatta in base ai tuoi dati
            axes[0].set_yticks([1e-3, 1e-2, 1e-1, 1.0, 2.0])
            axes[0].get_yaxis().set_major_formatter(ticker.ScalarFormatter())
            # tick ogni 0.1 secondi

            axes[0].legend(loc="upper left")                 # aggiungi leggenda
            axes[0].grid(True, linestyle="--", alpha=0.7)

            # Energia
            axes[1].set_title(f"Energia media- {algo} ({lang}, {tipo})")
            axes[1].errorbar(x, energia, yerr=energia_err, fmt="-o", color="black", label="Energia totale")
            axes[1].errorbar(x, energia, yerr=energia_err, fmt="none", ecolor="red", capsize=4, label="Deviazione")

            axes[1].set_xlabel("Input")
            axes[1].set_ylabel("Energia (J)")
            axes[1].set_ylim(0.0, 2.0)
            axes[1].set_yticks(np.arange(0.0, 2.5, 0.5))
            axes[1].grid(True, linestyle="--", alpha=0.7)
            axes[1].legend(loc="upper left")

            # Potenza
            axes[2].plot(x, potenza, "-o", color="black")
            axes[2].set_title(f"Potenza (Energia x Tempo) - {algo} ({lang}, {tipo})")
            axes[2].set_xlabel("Input")
            axes[2].axhline(y=5.0, color="red", linestyle="--", label="Potenza fissa 5 W")
            axes[2].set_ylim(0.0, 6.0)  # range leggermente più alto per visibilità
            axes[2].set_yticks(np.arange(0.0, 6.5, 0.5))
            axes[2].legend(loc="upper left")

            axes[2].grid(True, linestyle="--", alpha=0.7)

            plt.tight_layout()
            filename = f"{algo}_{lang}_{tipo}_tempo_energia_potenza.png"
            plt.savefig(os.path.join(GRAPH_DIR, filename))
            plt.close()

# === Grafico 2: confronto cumulativo separato per algoritmo e tipo ===
for algo in df["algoritmo"].unique():
    for tipo in ["iterativo", "ricorsivo"]:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # due subplot affiancati
        color_cycle = it.cycle([
            "blue", "green", "red", "purple", "brown", "teal", "magenta", "olive", "darkorange", "navy"
        ])

        # --- Subplot 1: Tempo medio cumulativo ---
        for lang in df["linguaggio"].unique():
            subset = df[(df["algoritmo"] == algo) &
                        (df["linguaggio"] == lang) &
                        (df["tipo"] == tipo)]
            if subset.empty:
                continue

            s = subset.sort_values("input_num")
            x = s["input_num"].values
            tempo = s["tempo_medio"].values
            tempo_err = s["deviazione_tempo"].values
            energia = s["energia_tot_j"].values
            energia_err = s["deviazione_energia_tot_j"].values
            color = next(color_cycle)

            # Tempo medio
            axes[0].errorbar(x, tempo, yerr=tempo_err, fmt="-o", color=color, capsize=4, label=f"{lang}")
            # Energia totale
            axes[1].errorbar(x, energia, yerr=energia_err, fmt="-o", color=color, capsize=4, label=f"{lang}")

       # --- Configura subplot tempo ---
            axes[0].set_title(f"Andamento cumulativo del tempo medio - {algo} ({tipo})")
            axes[0].set_xlabel("Input")
            axes[0].set_ylabel("Tempo medio (s)")
            axes[0].grid(True, linestyle="--", alpha=0.7)

            # Scala logaritmica
            axes[0].set_yscale("log")
            axes[0].set_ylim(0, 6.0)   # adatta il minimo al tuo dataset
            axes[0].get_yaxis().set_major_formatter(ticker.ScalarFormatter())
            axes[0].get_yaxis().set_minor_formatter(ticker.NullFormatter())

            # tick logaritmici (puoi personalizzare)
            axes[0].set_yticks([1e-3, 1e-2, 1e-1, 1, 6])

            axes[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        # --- Configura subplot energia ---
        axes[1].set_title(f"Consumo cumulativo dell'energia totale - {algo} ({tipo})")
        axes[1].set_xlabel("Input")
        axes[1].set_ylabel("Energia (J)")

        axes[1].set_ylim(0.0, 6.0)
        axes[1].set_yticks(np.arange(0.0, 2.5, 0.5))
        

        axes[1].grid(True, linestyle="--", alpha=0.7)
        axes[1].legend(bbox_to_anchor=(1.05, 1), loc="upper left")

        plt.tight_layout()
        filename = f"cumulativo_tempo_energia_{algo}_{tipo}.png"
        #plt.show()
        plt.savefig(os.path.join(GRAPH_DIR, filename))
        plt.close()

print(f"\n⟶ Saved plots in {GRAPH_DIR}")
