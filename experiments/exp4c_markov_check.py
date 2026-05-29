"""Experiment 4c: probe Markovianness of the 4-state parity-split chain.

For each m, computes alpha_m = empirical P(return to A at the m-th visit
to B_o since last A). Under the Markov assumption, alpha_m should be
constant in m. If it drifts, the parity-split chain has hidden state and
the geometric law is only asymptotic.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.logistic import U_C, gap_sequence, iterate, symbolize


def main(n_steps: int = 5_000_000) -> None:
    orbit = iterate(U_C, 0.1, n_steps, burn_in=10_000)
    sym = symbolize(orbit)
    gaps = gap_sequence(sym)

    max_m = 12
    counts_close = np.zeros(max_m + 2, dtype=np.int64)
    counts_continue = np.zeros(max_m + 2, dtype=np.int64)
    for g in gaps:
        if g % 2 != 0:
            continue
        m_close = g // 2
        for m in range(1, min(m_close, max_m + 1)):
            counts_continue[m] += 1
        if m_close <= max_m:
            counts_close[m_close] += 1

    print("alpha_m = P(return to A at m-th B_o visit | reached m-th B_o):")
    print("Markov hypothesis: alpha_m is constant in m.\n")
    print(f"  {'m':>4} {'closes':>10} {'continues':>10} {'alpha_m':>10}")
    for m in range(1, max_m + 1):
        denom = counts_close[m] + counts_continue[m]
        alpha_m = counts_close[m] / denom if denom > 0 else float("nan")
        print(f"  {m:>4} {counts_close[m]:>10} {counts_continue[m]:>10} {alpha_m:>10.4f}")


if __name__ == "__main__":
    main()
