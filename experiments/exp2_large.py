"""Experiment 2 (large): logistic-map gap spectrum at u_c, 10^8 iterations.

Higher-precision version of exp2_logistic_gaps.py. Used for clean tail
ratios mu_{2m+2}/mu_{2m} that confirm the asymptotic geometric law of
Theorem (Markov decay) with p ~ 0.59. Output: results/exp2_large.json.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.gap_spectrum import even_gap_ratios, gap_histogram, geometric_fit_ratio
from src.logistic import U_C, gap_sequence, iterate, symbolize


def main(n_steps: int = 500_000_000, x0: float = 0.1, max_gap: int = 100) -> None:
    print(f"Iterating logistic map at u = {U_C} for {n_steps:,} steps...")
    orbit = iterate(U_C, x0, n_steps, burn_in=10_000)
    sym = symbolize(orbit)
    gaps = gap_sequence(sym)
    print(f"Collected {gaps.size:,} gaps; L-frequency = {(sym == 0).mean():.6f}")

    hist = gap_histogram(gaps, max_gap=max_gap)
    ratios_to_mu2 = even_gap_ratios(hist)
    p_hat = geometric_fit_ratio(hist)

    successive = {}
    even_gaps = sorted(g for g in hist if g % 2 == 0 and hist[g] > 0)
    for i in range(1, len(even_gaps)):
        g_prev, g = even_gaps[i - 1], even_gaps[i]
        if hist[g_prev] > 0:
            successive[g] = hist[g] / hist[g_prev]

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp2_large.json"
    out_path.write_text(
        json.dumps(
            {
                "u": U_C,
                "n_steps": n_steps,
                "n_gaps": int(gaps.size),
                "histogram": hist,
                "even_ratios_to_mu2": ratios_to_mu2,
                "successive_even_ratios": successive,
                "geometric_p_hat": p_hat,
            },
            indent=2,
        )
    )

    print("\nGap mass (even gaps only, mass > 1e-7):")
    for g in even_gaps:
        if hist[g] > 1e-7:
            print(f"  g = {g:>3}  mu = {hist[g]:.7f}")

    print("\nSuccessive ratios mu_{2m+2}/mu_{2m} (asymptotic limit ~ 0.595):")
    for g, r in sorted(successive.items()):
        if hist.get(g, 0) > 1e-6:
            print(f"  mu_{g}/mu_{g - 2} = {r:.4f}")

    print(f"\nFitted common ratio p_hat ~ {p_hat:.4f}")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
