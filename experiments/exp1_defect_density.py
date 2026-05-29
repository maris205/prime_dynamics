"""Experiment 1: Asymptotic admissibility of the Q_k sieve sequences.

Reproduces the rho(N) defect-density table from prime6.ipynb / prime7.ipynb
using the cleaned-up modules in src/. Output: results/exp1_defect_density.csv.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.mss import count_defects
from src.sieve import Qk_horizon, Qk_sequence, first_n_primes


def main(k_max: int = 14) -> None:
    primes = first_n_primes(k_max)
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp1_defect_density.csv"

    rows = []
    print(f"{'k':<4} {'p_k':<6} {'p_{k+1}^2':<10} {'defects':<10} {'rho(N)':<12}")
    print("-" * 50)
    for k in range(1, k_max + 1):
        N = Qk_horizon(k)
        seq = Qk_sequence(k, N)
        defects, density = count_defects(seq)
        rows.append((k, primes[k - 1], N, defects, density))
        print(f"{k:<4} {primes[k - 1]:<6} {N:<10} {defects:<10} {density:<12.6e}")

    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["k", "p_k", "horizon_N", "defects", "rho_N"])
        writer.writerows(rows)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
