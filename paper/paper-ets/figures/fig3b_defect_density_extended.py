"""Figure 2 (extended): rho(N) for k = 1..50.

Reads results/exp1_extended.csv. Same stem-plot style as fig2_defect_density.py
but on the wider k range; demonstrates that beyond Q_3 and Q_5 every Q_k
in the tested range is admissible.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CSV_PATH = ROOT / "results" / "exp1_extended.csv"


def load() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
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
    fig, ax = plt.subplots(figsize=(11, 5.5), dpi=150)

    markerline, stemlines, baseline = ax.stem(
        Ns, rhos, basefmt="k-", linefmt="#d62728", markerfmt="ro"
    )
    plt.setp(stemlines, linewidth=1.5, alpha=0.85)
    plt.setp(markerline, markersize=6, markeredgecolor="black", markeredgewidth=0.4)
    plt.setp(baseline, color="black", lw=0.7)

    ax.plot(Ns, rhos, color="#d62728", alpha=0.18, lw=4, zorder=0)

    spike_anns = {
        3: ("$Q_3$ defect at $n=31$\n(parity flip)", (1500, 0.022)),
        5: ("$Q_5$ defect at gap 113-127", (5000, 0.012)),
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
        r"$\rho(N) \equiv 0$ for all $k \in [6, 50]$",
        xy=(40000, 0), xytext=(20000, 0.006),
        fontsize=11, color="#2ca02c", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#2ca02c", lw=1.3),
    )

    ax.set_title(
        r"Asymptotic Admissibility (extended): $\rho(N)$ for $Q_k$, $k = 1, \ldots, 50$",
        fontsize=13, fontweight="bold", pad=12,
    )
    ax.set_xlabel(r"Physical horizon $N = p_{k+1}^2$", fontsize=12)
    ax.set_ylabel(r"Defect density $\rho(N)$", fontsize=12)
    ax.grid(True, ls="--", alpha=0.5)
    ax.set_ylim(-0.002, 0.026)
    ax.set_xscale("symlog", linthresh=200)

    out = ROOT / "figures" / "fig3b_defect_density_extended.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
