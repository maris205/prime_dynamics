"""Experiment 2: 1D logistic-map gap spectrum at u_c.

Tests the geometric-decay claim mu_{2m+2} = p * mu_{2m} predicted by the
3-state Markov partition (A -> C, B -> C, C -> A | B). Expected ratios
from readme.md: mu_4/mu_2 ~ 0.54, mu_6/mu_2 ~ 0.29 (~ 0.54^2).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.gap_spectrum import even_gap_ratios, gap_histogram, geometric_fit_ratio
from src.logistic import U_C, gap_sequence, iterate, symbolize


def main(n_steps: int = 5_000_000, x0: float = 0.1, max_gap: int = 30) -> None:
    print(f"Iterating logistic map at u = {U_C} for {n_steps:,} steps...")
    orbit = iterate(U_C, x0, n_steps, burn_in=10_000)
    sym = symbolize(orbit)
    gaps = gap_sequence(sym)
    print(f"Collected {gaps.size:,} gaps; L-frequency = {(sym == 0).mean():.4f}")

    hist = gap_histogram(gaps, max_gap=max_gap)
    ratios = even_gap_ratios(hist)
    p_hat = geometric_fit_ratio(hist)

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp2_logistic_gaps.json"
    out_path.write_text(
        json.dumps(
            {
                "u": U_C,
                "n_steps": n_steps,
                "histogram": hist,
                "even_ratios_to_mu2": ratios,
                "geometric_p_hat": p_hat,
            },
            indent=2,
        )
    )

    print("\nGap mass:")
    for g in sorted(hist):
        print(f"  g = {g:>3}  mu = {hist[g]:.6f}")
    print("\nEven-gap ratios mu_{2m}/mu_2 (geometric decay test):")
    for g, r in sorted(ratios.items()):
        print(f"  mu_{g}/mu_2 = {r:.4f}")
    print(f"\nFitted common ratio p ~ {p_hat:.4f}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
