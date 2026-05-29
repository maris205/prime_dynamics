"""Experiment 3: Real-prime gap spectrum (Hardy-Littlewood reference).

The 1D logistic model produces only a geometric decay; real primes show a
mod-3 resonance peak at gap 6, 12, 18 (HL constants). This script computes
the empirical gap mass from primes up to N for direct comparison.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.gap_spectrum import even_gap_ratios, gap_histogram, real_prime_gaps


def main(N: int = 5_000_000, max_gap: int = 30) -> None:
    print(f"Sieving primes up to {N:,}...")
    gaps = real_prime_gaps(N)
    print(f"Found {gaps.size:,} prime gaps; mean gap = {gaps.mean():.3f}")

    hist = gap_histogram(gaps, max_gap=max_gap)
    ratios_to_mu2 = even_gap_ratios(hist)

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp3_real_prime_gaps.json"
    out_path.write_text(
        json.dumps(
            {
                "N": N,
                "n_gaps": int(gaps.size),
                "histogram": hist,
                "even_ratios_to_mu2": ratios_to_mu2,
            },
            indent=2,
        )
    )

    print("\nReal-prime gap mass (resonance at multiples of 6 expected):")
    for g in sorted(hist):
        flag = "  <-- mod-6 spike" if g % 6 == 0 and g <= 18 else ""
        print(f"  g = {g:>3}  mu = {hist[g]:.6f}{flag}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
