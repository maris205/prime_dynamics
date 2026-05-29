"""Experiment 5: 'Death in 3 Steps' for the natural prime sequence.

In the paper's S_p = R L^{p-1} convention, the prime p itself gets marked
R (composite-like). The readme/Gemini analysis observes that if instead
the prime is kept as L (its natural symbolic identity), the sequence
becomes absolutely admissible at every horizon: no MSS violation occurs
for ANY shift, because the prefix R L L L ... carrying primes 2, 3, 5
forces all shifts to lose within 3 symbols.

This experiment verifies the claim numerically up to N = 10^8.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from sympy import primerange

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.mss_jit import count_defects_jit


def natural_prime_sequence(N: int, one_is_L: bool = True) -> np.ndarray:
    """Symbolic sequence: primes -> L (0), composites -> R (1).

    Index 0 is forced to R by the unimodal-map convention. The treatment
    of index 1 is a convention choice: in classical arithmetic 1 is
    neither prime nor composite. The Gemini-style 'death in 3 steps'
    argument relies on position 1 being L (carrying L-mass alongside the
    primes 2, 3); this is the default. Set `one_is_L=False` to mark 1 as R.
    """
    seq = np.ones(N, dtype=np.int8)  # default R (composite)
    primes = np.array(list(primerange(2, N)), dtype=np.int64)
    seq[primes] = 0  # primes are L
    if one_is_L and N > 1:
        seq[1] = 0  # treat 1 as L
    return seq


def main() -> None:
    horizons = [10**3, 10**4, 10**5, 10**6, 10**7, 10**8]

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp5_natural_primes.csv"

    for one_is_L in [True, False]:
        label = "1 -> L (Gemini convention)" if one_is_L else "1 -> R (paper-style)"
        print(f"\n=== {label} ===")
        print(f"{'horizon N':>12} {'n_primes':>12} {'defects':>10} {'rho(N)':>14}")
        print("-" * 55)
        rows = []
        for N in horizons:
            seq = natural_prime_sequence(N, one_is_L=one_is_L)
            n_primes = int((seq == 0).sum())
            defects, density = count_defects_jit(seq)
            rows.append((N, n_primes, defects, density))
            print(f"{N:>12,} {n_primes:>12,} {defects:>10} {density:>14.6e}")

        n_defective = sum(1 for r in rows if r[2] > 0)
        if n_defective == 0:
            print(f"  ABSOLUTE ADMISSIBILITY: no MSS defects at any horizon.")
        else:
            print(f"  {n_defective}/{len(rows)} horizons have defects.")


if __name__ == "__main__":
    main()
