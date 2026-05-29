"""Experiment 1 (extended): defect density rho(N) for k = 1..50.

Continuation of experiments/exp1_defect_density.py beyond k = 14 (the
range covered in the original Wang 2026 manuscript). Tests whether the
two defective stages Q_3 (n = 31) and Q_5 (113-127 gap) are the only
ones, or whether further defects appear at large k. Output:
results/exp1_extended.csv.
"""
from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.mss import count_defects
from src.sieve import Qk_horizon, Qk_sequence, first_n_primes


def main(k_max: int = 100) -> None:
    primes = first_n_primes(k_max)
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp1_extended.csv"

    rows = []
    print(f"{'k':<4} {'p_k':<6} {'p_{k+1}^2':<10} {'defects':<10} {'rho(N)':<14} {'time':<8}")
    print("-" * 60)
    for k in range(1, k_max + 1):
        N = Qk_horizon(k)
        seq = Qk_sequence(k, N)
        t0 = time.time()
        defects, density = count_defects(seq)
        elapsed = time.time() - t0
        rows.append((k, primes[k - 1], N, defects, density))
        print(
            f"{k:<4} {primes[k - 1]:<6} {N:<10} {defects:<10} "
            f"{density:<14.6e} {elapsed:.2f}s"
        )

    with out_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["k", "p_k", "horizon_N", "defects", "rho_N"])
        writer.writerows(rows)
    print(f"\nWrote {out_path}")

    n_defective = sum(1 for r in rows if r[3] > 0)
    print(f"\nSummary: {n_defective} defective stages out of {k_max}.")
    if n_defective:
        print("Defective k:")
        for k, p_k, N, d, rho in rows:
            if d > 0:
                print(f"  k = {k:>3}  (p = {p_k}, N = {N}):  {d} defects, rho = {rho:.4e}")


if __name__ == "__main__":
    main()
