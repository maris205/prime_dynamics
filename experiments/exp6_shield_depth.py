"""Experiment 6: average shift-match depth d_k as a function of k.

For each sieve stage Q_k, computes the *average* matched-prefix length
across all shifts m in [1, N-1] before a parity-twisted comparison
finds its first mismatch. Tracks both mean and median; fits log-log to
test the conjectured d_k ~ k^alpha scaling that motivates the
shield-depth open problem in the paper.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np
from numba import njit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.sieve import Qk_horizon, Qk_sequence, first_n_primes


@njit(cache=True)
def _shift_match_depths(seq: np.ndarray) -> np.ndarray:
    """Length of the matched prefix orig[:i] == shifted[:i] before first
    mismatch (or full length if all match), one entry per shift."""
    n = seq.shape[0]
    depths = np.empty(n - 1, dtype=np.int64)
    for shift in range(1, n):
        i = 0
        m = n - shift
        while i < m and seq[i] == seq[i + shift]:
            i += 1
        depths[shift - 1] = i
    return depths


def main(k_max: int = 1000) -> None:
    primes = first_n_primes(k_max)
    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp6_shield_depth.csv"

    # warm up JIT
    _ = _shift_match_depths(Qk_sequence(3, 49))

    rows = []
    print(f"{'k':<4} {'p_k':<5} {'N':<10} {'mean':>10} {'median':>8} {'p95':>8} {'max':>8}")
    print("-" * 58)
    for k in range(1, k_max + 1):
        N = Qk_horizon(k)
        seq = Qk_sequence(k, N)
        depths = _shift_match_depths(seq)
        mean = float(depths.mean())
        median = int(np.median(depths))
        p95 = int(np.percentile(depths, 95))
        mx = int(depths.max())
        rows.append((k, primes[k - 1], N, mean, median, p95, mx))
        if k <= 20 or k % 10 == 0:
            print(f"{k:<4} {primes[k - 1]:<5} {N:<10} {mean:>10.2f} {median:>8} {p95:>8} {mx:>8}")

    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["k", "p_k", "N", "mean_depth", "median_depth", "p95_depth", "max_depth"])
        w.writerows(rows)

    ks = np.array([r[0] for r in rows], dtype=float)
    means = np.array([r[3] for r in rows], dtype=float)

    fit_lo = max(1, k_max // 4)
    log_k = np.log(ks[fit_lo:])
    log_d = np.log(np.maximum(means[fit_lo:], 1e-9))
    alpha, log_C = np.polyfit(log_k, log_d, 1)
    print(f"\nLog-log fit on k >= {fit_lo}:  d_k ~ {np.exp(log_C):.3f} * k^{alpha:.3f}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
