"""Figure 3: Geometric (1D) vs Hardy-Littlewood (real primes) gap spectrum.

Side-by-side bar charts:
  Left  : 1D logistic gap mass mu_g, with fitted geometric envelope p^m * mu_2.
  Right : real-prime gap mass with mod-6 resonance peaks at g = 6, 12, 18.
The visual contrast is the Section 4 punchline: 1D model is an abelian /
mod-2 projection, lacks internal mod-3 phase memory.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def load(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"{path} missing -- run the corresponding experiment first.")
    return json.loads(path.read_text())


def hist_dict(d: dict) -> dict[int, float]:
    return {int(g): float(m) for g, m in d.items()}


def main() -> None:
    log_data = load(ROOT / "results" / "exp2_large.json")
    real_data = load(ROOT / "results" / "exp3_real_prime_gaps.json")

    log_hist = hist_dict(log_data["histogram"])
    real_hist = hist_dict(real_data["histogram"])
    p_hat = log_data["geometric_p_hat"]

    max_g = 24
    gaps = np.arange(2, max_g + 1, 2)
    log_mu = np.array([log_hist.get(g, 0.0) for g in gaps])
    real_mu = np.array([real_hist.get(g, 0.0) for g in gaps])

    plt.style.use("seaborn-v0_8-paper")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=150, sharey=False)

    ax = axes[0]
    bars = ax.bar(gaps, log_mu, width=1.4, color="#1f77b4", ec="black", lw=0.5, alpha=0.85)
    geom = log_mu[0] * (p_hat ** np.arange(len(gaps)))
    ax.plot(
        gaps, geom, "r--", lw=2.0,
        label=fr"geometric fit: $p \approx {p_hat:.3f}$, $\mu_{{2m}} = p^{{m-1}}\mu_2$",
    )
    ax.set_title("(a) 1D logistic map at $u_c$: geometric decay", fontsize=12, fontweight="bold")
    ax.set_xlabel("gap $g$", fontsize=11)
    ax.set_ylabel(r"normalized mass $\mu_g$", fontsize=11)
    ax.set_xticks(gaps)
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, ls="--", alpha=0.5)
    for g, m in zip(gaps, log_mu):
        if g % 6 == 0:
            ax.text(g, m + 0.005, "no spike", ha="center", fontsize=8, color="#2ca02c")

    ax = axes[1]
    colors = ["#ff7f0e" if g % 6 == 0 else "#1f77b4" for g in gaps]
    ax.bar(gaps, real_mu, width=1.4, color=colors, ec="black", lw=0.5, alpha=0.85)
    ax.set_title(
        "(b) real primes: Hardy-Littlewood mod-6 resonance",
        fontsize=12, fontweight="bold",
    )
    ax.set_xlabel("gap $g$", fontsize=11)
    ax.set_ylabel(r"normalized mass $\mu_g$", fontsize=11)
    ax.set_xticks(gaps)
    ax.grid(True, ls="--", alpha=0.5)
    for g, m in zip(gaps, real_mu):
        if g % 6 == 0:
            ax.annotate(
                f"g={g}", xy=(g, m), xytext=(g, m + 0.015),
                ha="center", fontsize=9, color="#ff7f0e", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#ff7f0e", lw=1.0),
            )
    handles = [
        plt.Rectangle((0, 0), 1, 1, fc="#ff7f0e", ec="black"),
        plt.Rectangle((0, 0), 1, 1, fc="#1f77b4", ec="black"),
    ]
    ax.legend(
        handles, ["multiples of 6 (mod-3 spike)", "other even gaps"],
        loc="upper right", fontsize=10,
    )

    fig.suptitle(
        "Topological Horizon: 1D Markov Decay vs Real Hardy-Littlewood Spectrum",
        fontsize=14, fontweight="bold", y=1.02,
    )
    out = ROOT / "figures" / "fig2_geometric_vs_HL.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
