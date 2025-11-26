import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Percorsi
RESULT_CSV = "Results/csv/benchmark_single.csv"
GRAPH_DIR = "Results/Graphic/Single"

# Crea cartella grafici se non esiste
os.makedirs(GRAPH_DIR, exist_ok=True)

# Carica dati dal CSV
df = pd.read_csv(RESULT_CSV, delimiter=";")

# === Grafico 1: Tempo medio con deviazione standard per algoritmo e linguaggio ==========================
for algo in df["algoritmo"].unique():
    subset = df[df["algoritmo"] == algo]

    pivot = subset.pivot_table(index="linguaggio", columns="tipo", values="tempo_medio", aggfunc="mean")
    errors = subset.pivot_table(index="linguaggio", columns="tipo", values="deviazione_tempo", aggfunc="mean")

    x = np.arange(len(pivot.index))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["green", "red", "blue", "orange"]

    for i, tipo in enumerate(pivot.columns):
        y = pivot[tipo].values
        yerr = errors[tipo].values

        ax.bar(x + i*bar_width, y, bar_width,
               label=tipo, color=colors[i % len(colors)])
        ax.errorbar(x + i*bar_width, y, yerr=yerr,
                    fmt="none", ecolor="black", capsize=4,
                    label="deviazione standard" if i == 0 else None)

    ax.set_xticks(x + bar_width/2)
    ax.set_xticklabels(pivot.index, rotation=0, ha="center")

    plt.title(f"Tempo medio per {algo} (con deviazione standard)")
    plt.ylabel("Tempo medio (s)")
    plt.xlabel("Linguaggio")
    plt.legend(title="Tipo", loc="best")
    plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, f"tempo_{algo}.png"))
    plt.close()
    print(f"⟶ Grafico tempo salvato: tempo_{algo}.png")

    # === Grafico 2: Energia totale per algoritmo e linguaggio ============================================
    subset_energy = subset.dropna(subset=["energia_tot_j", "deviazione_energia_tot_j"])
    pivot_mean = subset_energy.pivot_table(index="linguaggio", columns="tipo", values="energia_tot_j", aggfunc="mean")
    pivot_std = subset_energy.pivot_table(index="linguaggio", columns="tipo", values="deviazione_energia_tot_j", aggfunc="mean")

    x = np.arange(len(pivot_mean.index))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    for i, tipo in enumerate(pivot_mean.columns):
        y = pivot_mean[tipo].values
        yerr = pivot_std[tipo].values
        ax.bar(x + i*bar_width, y, bar_width,
               label=tipo, color=colors[i % len(colors)])
        ax.errorbar(x + i*bar_width, y, yerr=yerr,
                    fmt="none", ecolor="black", capsize=4,
                    label="deviazione standard" if i == 0 else None)

    ax.set_xticks(x + bar_width/2)
    ax.set_xticklabels(pivot_mean.index, rotation=0, ha="center")

    plt.title(f"Energia totale per {algo} (PKG+DRAM)")
    plt.ylabel("Energia totale (J)")
    plt.xlabel("Linguaggio")
    plt.legend(title="Tipo", loc="best")
    plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, f"energia_{algo}.png"))
    plt.close()
    print(f"⟶ Grafico energia salvato: energia_{algo}.png")

    # === Grafico 3: Potenza (tempo × energia) per algoritmo e linguaggio ================================
    subset["potenza"] = subset["tempo_medio"] * subset["energia_tot_j"]
    subset_pot = subset.dropna(subset=["potenza"])
    pivot_mean = subset_pot.pivot_table(index="linguaggio", columns="tipo", values="potenza", aggfunc="mean")

    x = np.arange(len(pivot_mean.index))
    bar_width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    for i, tipo in enumerate(pivot_mean.columns):
        y = pivot_mean[tipo].values
        ax.bar(x + i*bar_width, y, bar_width,
               label=tipo, color=colors[i % len(colors)])

    ax.set_xticks(x + bar_width/2)
    ax.set_xticklabels(pivot_mean.index, rotation=0, ha="center")

    plt.title(f"Potenza (Tempo × Energia) per {algo}")
    plt.ylabel("Potenza (J·s)")
    plt.xlabel("Linguaggio")
    plt.legend(title="Tipo", loc="best")
    plt.grid(axis="y", linestyle="--", linewidth=0.7, alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPH_DIR, f"potenza_{algo}.png"))
    plt.close()
    print(f"⟶ Grafico potenza salvato: potenza_{algo}.png")

print(f"\n⟶ Tutti i grafici salvati in {GRAPH_DIR}")
