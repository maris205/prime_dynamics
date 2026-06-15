"""Figure 2: Asymptotic admissibility -- defect density rho(N) decay.

Reads results/exp1_defect_density.csv and renders the stem plot from
prime7.ipynb in publication style: spikes at Q_3 (n=31) and Q_5 (113-127),
crushed to zero for k >= 6 by the topological shield.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CSV_PATH = ROOT / "results" / "exp1_defect_density.csv"


def load() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"{CSV_PATH} not found. Run experiments/exp1_defect_density.py first."
        )
    ks, Ns, rhos = [], [], []
    with CSV_PATH.open() as f:
        for row in csv.DictReader(f):
            ks.append(int(row["k"]))
            Ns.append(int(row["horizon_N"]))
            rhos.append(float(row["rho_N"]))
    return np.array(ks), np.array(Ns), np.array(rhos)


def main() -> None:
    ks, Ns, rhos = load()

    plt.style.use("seaborn-v0_8-paper")
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)

    markerline, stemlines, baseline = ax.stem(
        Ns, rhos, basefmt="k-", linefmt="#d62728", markerfmt="ro"
    )
    plt.setp(stemlines, linewidth=2, alpha=0.85)
    plt.setp(markerline, markersize=8, markeredgecolor="black", markeredgewidth=0.5)
    plt.setp(baseline, color="black", lw=0.7)

    ax.plot(Ns, rhos, color="#d62728", alpha=0.18, lw=4, zorder=0)

    for k, N, rho in zip(ks, Ns, rhos):
        ax.text(N, rho + 0.0008, f"$Q_{{{k}}}$", ha="center", fontsize=9, color="dimgray")

    spike_anns = {
        3: ("Topological breakdown $Q_3$\ndriver: gap (23-29) + parity flip", (200, 0.022)),
        5: ("Topological breakdown $Q_5$\ndriver: large gap (113-127)", (550, 0.012)),
    }
    for k, N, rho in zip(ks, Ns, rhos):
        if k in spike_anns and rho > 0:
            text, xytext = spike_anns[k]
            ax.annotate(
                text, xy=(N, rho), xytext=xytext,
                fontsize=10, color="#8c564b", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#8c564b", lw=1.3),
            )

    ax.annotate(
        r"asymptotic admissibility: $\rho(N) \equiv 0$",
        xy=(1500, 0), xytext=(1100, 0.006),
        fontsize=11, color="#2ca02c", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.3),
    )

    ax.set_title(
        r"Asymptotic Admissibility: Defect Density $\rho(N)$ of the Sieve Sequence $Q_k$",
        fontsize=13, fontweight="bold", pad=12,
    )
    ax.set_xlabel(r"Physical horizon $N = p_{k+1}^2$", fontsize=12)
    ax.set_ylabel(r"Defect density $\rho(N)$", fontsize=12)
    ax.grid(True, ls="--", alpha=0.5)
    ax.set_ylim(-0.002, 0.026)

    out = ROOT / "figures" / "fig3_defect_density.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
