"""Figure 1: Microscopic parity-lex breakdown of Q_3 at n = 31.

Visualizes the MSS comparison of Q_3 against its 22-shift, highlighting the
public prefix (7 R's -> odd parity flip) and the position-9 conflict where
Q_3 emits R (composite 9) but sigma^22(Q_3) emits L (prime 31), so under
the flipped rule Q_3 prec sigma^22(Q_3) and admissibility fails.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.sieve import Qk_sequence


def main() -> None:
    horizon = 49
    Q3 = Qk_sequence(3, horizon)

    shift = 22
    prefix_len = 10
    orig = Q3[:prefix_len]
    shifted = Q3[shift : shift + prefix_len]
    diff_pos = int(np.argmax(orig != shifted))
    r_count = int(orig[:diff_pos].sum())
    parity_flip = bool(r_count & 1)

    plt.style.use("seaborn-v0_8-paper")
    fig, ax = plt.subplots(figsize=(11, 4), dpi=150)

    cells = np.arange(prefix_len)
    for row, (label, seq, base_idx) in enumerate(
        [(r"$Q_3$ from $n=0$", orig, 0), (r"$\sigma^{22}(Q_3)$ from $n=22$", shifted, 22)]
    ):
        y = 1 - row
        for i, sym in enumerate(seq):
            color = "#d62728" if i == diff_pos else ("#1f77b4" if sym else "#2ca02c")
            ax.add_patch(
                plt.Rectangle(
                    (i - 0.4, y - 0.4), 0.8, 0.8, fc=color, ec="black", lw=0.6, alpha=0.85
                )
            )
            ax.text(
                i, y, "R" if sym else "L",
                ha="center", va="center", color="white", fontweight="bold", fontsize=12,
            )
            ax.text(
                i, y - 0.65, str(base_idx + i),
                ha="center", va="center", fontsize=8, color="dimgray",
            )
        ax.text(-1.5, y, label, ha="right", va="center", fontsize=12, fontweight="bold")

    ax.add_patch(
        plt.Rectangle(
            (-0.5, -0.5), diff_pos, 2.0,
            fill=False, ec="#8c564b", lw=2.0, ls="--",
        )
    )
    ax.annotate(
        f"common prefix: {r_count} R-symbols (odd) -> rule flips: $L \\succ R$",
        xy=(diff_pos / 2 - 0.5, 1.5), xytext=(diff_pos / 2 - 0.5, 2.0),
        ha="center", fontsize=10, color="#8c564b", fontweight="bold",
    )
    ax.annotate(
        f"position {diff_pos} (n={diff_pos} vs n={shift + diff_pos}):\n"
        r"$Q_3$ = R, $\sigma^{22}(Q_3)$ = L  $\Rightarrow$  $Q_3 \prec \sigma^{22}(Q_3)$",
        xy=(diff_pos, 0.5), xytext=(diff_pos + 0.5, -1.2),
        fontsize=10, color="#d62728", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.5),
    )

    ax.set_xlim(-3.5, prefix_len + 0.5)
    ax.set_ylim(-2.0, 2.6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(
        "Microscopic Breakdown: Parity-Lex Collapse of $Q_3$ at $n=31$",
        fontsize=13, fontweight="bold", pad=10,
    )

    out = ROOT / "figures" / "fig1_microscopic_breakdown.png"
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Wrote {out}  (parity_flip={parity_flip}, r_count={r_count})")


if __name__ == "__main__":
    main()
