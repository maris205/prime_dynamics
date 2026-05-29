"""Figure 4: joint gap distribution heatmap, logistic vs real primes.

Side-by-side log-scale 2D histogram of P(g_i, g_{i+1}). The 1D logistic
shows essentially independent gaps (rank-1 structure mu_g * mu_{g+1});
real primes show diagonal mod-6 stripes corresponding to admissible
prime constellations. P(2,2) is bright in logistic but absolutely dark
in real primes, exposing mod-3 absence visually.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sympy import primerange

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.logistic import U_C, gap_sequence, iterate, symbolize


def joint_hist(gaps: np.ndarray, max_g: int = 14) -> np.ndarray:
    H = np.zeros((max_g + 1, max_g + 1), dtype=np.float64)
    if gaps.size < 2:
        return H
    pairs = np.stack([gaps[:-1], gaps[1:]], axis=1)
    valid = (pairs[:, 0] <= max_g) & (pairs[:, 1] <= max_g)
    pairs = pairs[valid]
    for a, b in pairs:
        H[a, b] += 1
    return H / pairs.shape[0] if pairs.shape[0] > 0 else H


def main() -> None:
    print("Building 1D logistic gap pairs (5e6 steps)...")
    orbit = iterate(U_C, 0.1, 5_000_000, burn_in=10_000)
    gaps_log = gap_sequence(symbolize(orbit))
    print(f"  collected {gaps_log.size:,} gaps")

    print("Sieving primes up to 5e6...")
    primes = np.array(list(primerange(2, 5_000_000)), dtype=np.int64)
    gaps_real = np.diff(primes)
    print(f"  collected {gaps_real.size:,} gaps")

    max_g = 14
    H_log = joint_hist(gaps_log, max_g=max_g)
    H_real = joint_hist(gaps_real, max_g=max_g)

    plt.style.use("seaborn-v0_8-paper")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5), dpi=150)

    eps = 1e-9
    extent = [-0.5, max_g + 0.5, -0.5, max_g + 0.5]
    vmin, vmax = -7, 0

    for ax, H, title in zip(axes, [H_log, H_real],
                            ["(a) 1D logistic at $u_c$",
                             "(b) Real primes (up to $5 \\times 10^6$)"]):
        im = ax.imshow(
            np.log10(H + eps), origin="lower", extent=extent,
            vmin=vmin, vmax=vmax, cmap="magma", aspect="equal",
        )
        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel(r"$g_{i+1}$", fontsize=11)
        ax.set_ylabel(r"$g_i$", fontsize=11)
        ax.set_xticks(range(0, max_g + 1, 2))
        ax.set_yticks(range(0, max_g + 1, 2))
        plt.colorbar(im, ax=ax, label=r"$\log_{10} P(g_i, g_{i+1})$", shrink=0.85)

    axes[0].annotate(
        f"P(2,2) = {H_log[2, 2]:.2e}",
        xy=(2, 2), xytext=(7, 2.5),
        fontsize=10, color="white", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="white", lw=1.2),
    )
    axes[1].annotate(
        f"P(2,2) = {H_real[2, 2]:.2e}\n(forbidden by mod 3)",
        xy=(2, 2), xytext=(6, 2.5),
        fontsize=10, color="white", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="white", lw=1.2),
    )

    fig.suptitle(
        "Joint gap distribution: independence in 1D vs Hardy-Littlewood structure in primes",
        fontsize=13, fontweight="bold", y=1.02,
    )

    out = ROOT / "figures" / "fig4_joint_gap_heatmap.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"\nWrote {out}")
    print(f"Logistic P(2,2) = {H_log[2, 2]:.6e}")
    print(f"Real P(2,2)     = {H_real[2, 2]:.6e}")


if __name__ == "__main__":
    main()
