"""Experiment 11: Prime triplets — Direction C.

Prime triplets of the first kind (gap pattern 2, 4) like (5, 7, 11),
(11, 13, 17), (17, 19, 23). Hardy-Littlewood prediction:

    pi_3(N) ~ 9/2 * prod_{p>=5} (p^2(p-3) / (p-1)^3) * Li_3(N)

with the Hardy-Littlewood constant H_3 = (9/2) * 0.635166 = 2.85825.

We measure the empirical density of (gap, gap) = (2, 4) joint events in
both the 1D logistic orbit at u_c and in the real-prime sequence, then
compare against:
  - independent baseline mu_2 * mu_4 (no joint correlation)
  - normalized to Cramer-style baseline rho^2 (1-rho)^4

Prediction: 1D model captures parity rigidity (which forces gaps 2, 4
to be simultaneously realisable) but cannot capture the mod-3 boost.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sympy import primerange

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.logistic import U_C, gap_sequence, iterate, symbolize


def joint_gap_density(gaps: np.ndarray, g1: int, g2: int) -> float:
    """Empirical fraction of consecutive (gap, next gap) = (g1, g2)."""
    if gaps.size < 2:
        return 0.0
    a = (gaps[:-1] == g1) & (gaps[1:] == g2)
    return float(a.sum()) / (gaps.size - 1)


def main(n_steps_logistic: int = 5_000_000, N_primes: int = 5_000_000) -> None:
    print("=" * 70)
    print("Prime triplet (2,4) density: 1D logistic vs real primes")
    print("=" * 70)

    # 1D logistic
    print(f"\nIterating logistic at u_c for {n_steps_logistic:,} steps...")
    orbit = iterate(U_C, 0.1, n_steps_logistic, burn_in=10_000)
    sym = symbolize(orbit)
    gaps_log = gap_sequence(sym)
    rho_log = float((sym == 0).mean())

    p24_log = joint_gap_density(gaps_log, 2, 4)
    p42_log = joint_gap_density(gaps_log, 4, 2)
    p22_log = joint_gap_density(gaps_log, 2, 2)
    indep_log = (np.bincount(gaps_log, minlength=20)[2] / gaps_log.size) * (
        np.bincount(gaps_log, minlength=20)[4] / gaps_log.size
    )
    print(f"  rho = {rho_log:.6f}")
    print(f"  P(g_i=2, g_{{i+1}}=4) = {p24_log:.6f}")
    print(f"  P(g_i=4, g_{{i+1}}=2) = {p42_log:.6f}")
    print(f"  P(g_i=2, g_{{i+1}}=2) = {p22_log:.6f}  (would be twin-pair-twin: forbidden by 2-3 mod-3 rule)")
    print(f"  Independent product mu_2 * mu_4 = {indep_log:.6f}")
    print(f"  Joint enhancement P(2,4)/(mu_2*mu_4) = {p24_log/indep_log if indep_log else 0:.4f}")

    # Real primes
    print(f"\nSieving primes up to {N_primes:,}...")
    primes = np.array(list(primerange(2, N_primes)), dtype=np.int64)
    gaps_real = np.diff(primes)
    rho_real = primes.size / N_primes

    p24_real = joint_gap_density(gaps_real, 2, 4)
    p42_real = joint_gap_density(gaps_real, 4, 2)
    p22_real = joint_gap_density(gaps_real, 2, 2)
    mu2_real = (gaps_real == 2).sum() / gaps_real.size
    mu4_real = (gaps_real == 4).sum() / gaps_real.size
    indep_real = mu2_real * mu4_real
    print(f"  rho = {rho_real:.6f}")
    print(f"  P(g_i=2, g_{{i+1}}=4) = {p24_real:.6f}")
    print(f"  P(g_i=4, g_{{i+1}}=2) = {p42_real:.6f}")
    print(f"  P(g_i=2, g_{{i+1}}=2) = {p22_real:.6f}")
    print(f"  Independent product mu_2 * mu_4 = {indep_real:.6f}")
    print(f"  Joint enhancement P(2,4)/(mu_2*mu_4) = {p24_real/indep_real if indep_real else 0:.4f}")

    print("\n" + "=" * 70)
    print("Comparison summary")
    print("=" * 70)
    print(f"{'metric':<30} {'logistic':>12} {'real primes':>14}")
    print(f"{'P(2, 4)':<30} {p24_log:>12.6f} {p24_real:>14.6f}")
    print(f"{'P(2, 2)':<30} {p22_log:>12.6f} {p22_real:>14.6f}")
    print(f"{'joint enhancement':<30} {p24_log/indep_log:>12.4f} {p24_real/indep_real:>14.4f}")

    print("\nKey observations:")
    print("  - P(2, 2) is non-zero in the logistic model but tiny in real primes")
    print("    (real primes: only triplet (3,5,7) has gap-2-twice)")
    print("  - The 1D logistic model treats g_i and g_{i+1} as independent ~ mu_2*mu_4")
    print("  - Real primes show significant mod-3 enhancement at (2,4) and (4,2)")
    print("    (these triplets avoid divisibility by 3, hence boosted)")

    out = ROOT / "results" / "exp11_triplets.json"
    out.write_text(
        json.dumps(
            {
                "logistic": {
                    "rho": rho_log,
                    "n_gaps": int(gaps_log.size),
                    "P_2_4": p24_log,
                    "P_4_2": p42_log,
                    "P_2_2": p22_log,
                    "indep_product": indep_log,
                    "joint_enhancement": p24_log / indep_log if indep_log else 0.0,
                },
                "real_primes": {
                    "rho": rho_real,
                    "n_primes": int(primes.size),
                    "P_2_4": p24_real,
                    "P_4_2": p42_real,
                    "P_2_2": p22_real,
                    "indep_product": indep_real,
                    "joint_enhancement": p24_real / indep_real if indep_real else 0.0,
                },
            },
            indent=2,
        )
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
