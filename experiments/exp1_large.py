"""Experiment 1 (large): defect density rho(N) for k = 1..500.

Multiprocessing version using 16 of the 22 vCPUs available on the AutoDL
instance (leaves headroom for IO + system). Each stage k is independent;
the load imbalance from horizons that grow as p_{k+1}^2 is mitigated by
processing in reverse order so the longest jobs start first.
"""
from __future__ import annotations

import csv
import multiprocessing as mp
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.mss_jit import count_defects_jit as count_defects
from src.sieve import Qk_horizon, Qk_sequence, first_n_primes


def stage(args: tuple[int, int]) -> tuple[int, int, int, int, float, float]:
    k, p_k = args
    N = Qk_horizon(k)
    seq = Qk_sequence(k, N)
    t0 = time.time()
    defects, density = count_defects(seq)
    return k, p_k, N, defects, density, time.time() - t0


def main(k_max: int = 5000, n_workers: int = 12) -> None:
    primes = first_n_primes(k_max)
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp1_large.csv"

    args = [(k, primes[k - 1]) for k in range(1, k_max + 1)]
    args.sort(key=lambda x: -Qk_horizon(x[0]))

    print(f"Running k = 1..{k_max} on {n_workers} workers (longest first)...")
    print(f"Largest horizon: N = {Qk_horizon(k_max):,}")
    t0 = time.time()
    with mp.Pool(n_workers) as pool:
        results = pool.map(stage, args, chunksize=1)
    print(f"Total wall time: {time.time() - t0:.1f}s\n")

    results.sort(key=lambda r: r[0])

    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["k", "p_k", "horizon_N", "defects", "rho_N", "wall_time_s"])
        w.writerows(results)

    defective = [r for r in results if r[3] > 0]
    print(f"Summary: {len(defective)} defective stages out of {k_max}.")
    if defective:
        print("Defective k:")
        for k, p_k, N, d, rho, t in defective:
            print(f"  k = {k:>4}  p_k = {p_k:>4}  N = {N:>10,}  defects = {d:>3}  rho = {rho:.3e}")

    print("\nLargest 5 horizons (timing check):")
    for r in sorted(results, key=lambda x: -x[2])[:5]:
        k, p_k, N, d, rho, t = r
        print(f"  k = {k:>4}  N = {N:>10,}  defects = {d:>3}  wall = {t:>7.1f}s")

    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
