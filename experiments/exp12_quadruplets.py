"""Experiment 12: Prime quadruplets — gap pattern (2, 4, 2).

Prime quadruplets are 4-tuples (p, p+2, p+6, p+8) of primes. Examples:
(5, 7, 11, 13), (11, 13, 17, 19), (101, 103, 107, 109). The gap pattern
between consecutive members is (2, 4, 2). This is the densest possible
prime constellation of length 4: any p, p+2, p+4 contains a multiple of 3.

Hardy-Littlewood predicts the quadruplet density:
    pi_4(N) ~ (27/2) * prod_{p>=5} (p^3 (p-4) / (p-1)^4) * Li_4(N)

with the H-L constant H_4 ~ 4.151. We compare:
  - 1D logistic: P(g_i=2, g_{i+1}=4, g_{i+2}=2) ~ mu_2 * mu_4 * mu_2 (independent)
  - Real primes: empirical density showing strong joint enhancement
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


def joint3_density(gaps: np.ndarray, g1: int, g2: int, g3: int) -> float:
    if gaps.size < 3:
        return 0.0
    a = (gaps[:-2] == g1) & (gaps[1:-1] == g2) & (gaps[2:] == g3)
    return float(a.sum()) / (gaps.size - 2)


def main(n_steps_logistic: int = 5_000_000, N_primes: int = 5_000_000) -> None:
    print("=" * 70)
    print("Prime quadruplet (2, 4, 2) density: 1D logistic vs real primes")
    print("=" * 70)

    print(f"\nIterating logistic at u_c for {n_steps_logistic:,} steps...")
    orbit = iterate(U_C, 0.1, n_steps_logistic, burn_in=10_000)
    sym = symbolize(orbit)
    gaps_log = gap_sequence(sym)
    rho_log = float((sym == 0).mean())

    counts_log = np.bincount(gaps_log, minlength=20)
    mu2_log = counts_log[2] / gaps_log.size
    mu4_log = counts_log[4] / gaps_log.size
    indep3_log = mu2_log * mu4_log * mu2_log

    p242_log = joint3_density(gaps_log, 2, 4, 2)
    p222_log = joint3_density(gaps_log, 2, 2, 2)
    p424_log = joint3_density(gaps_log, 4, 2, 4)

    print(f"  rho = {rho_log:.6f}")
    print(f"  P(2, 4, 2) = {p242_log:.6f}")
    print(f"  P(2, 2, 2) = {p222_log:.6f}  (forbidden in real primes)")
    print(f"  P(4, 2, 4) = {p424_log:.6f}")
    print(f"  Independent mu_2*mu_4*mu_2 = {indep3_log:.6f}")
    print(f"  Joint enhancement P(2,4,2) / indep = {p242_log/indep3_log if indep3_log else 0:.4f}")

    print(f"\nSieving primes up to {N_primes:,}...")
    primes = np.array(list(primerange(2, N_primes)), dtype=np.int64)
    gaps_real = np.diff(primes)
    rho_real = primes.size / N_primes

    counts_real = np.bincount(gaps_real, minlength=20)
    mu2_real = counts_real[2] / gaps_real.size
    mu4_real = counts_real[4] / gaps_real.size
    indep3_real = mu2_real * mu4_real * mu2_real

    p242_real = joint3_density(gaps_real, 2, 4, 2)
    p222_real = joint3_density(gaps_real, 2, 2, 2)
    p424_real = joint3_density(gaps_real, 4, 2, 4)

    print(f"  rho = {rho_real:.6f}")
    print(f"  P(2, 4, 2) = {p242_real:.6f}")
    print(f"  P(2, 2, 2) = {p222_real:.6f}")
    print(f"  P(4, 2, 4) = {p424_real:.6f}")
    print(f"  Independent mu_2*mu_4*mu_2 = {indep3_real:.6f}")
    print(f"  Joint enhancement P(2,4,2) / indep = {p242_real/indep3_real if indep3_real else 0:.4f}")

    print("\n" + "=" * 70)
    print("Quadruplet comparison")
    print("=" * 70)
    print(f"{'metric':<28} {'logistic':>14} {'real primes':>14}")
    print(f"{'P(2, 4, 2)':<28} {p242_log:>14.6e} {p242_real:>14.6e}")
    print(f"{'P(2, 2, 2)':<28} {p222_log:>14.6e} {p222_real:>14.6e}")
    print(f"{'joint enhancement':<28} {p242_log/indep3_log:>14.4f} {p242_real/indep3_real:>14.4f}")

    out = ROOT / "results" / "exp12_quadruplets.json"
    out.write_text(
        json.dumps(
            {
                "logistic": {
                    "rho": rho_log,
                    "P_242": p242_log,
                    "P_222": p222_log,
                    "P_424": p424_log,
                    "indep_product": indep3_log,
                    "joint_enhancement": p242_log / indep3_log if indep3_log else 0.0,
                },
                "real_primes": {
                    "rho": rho_real,
                    "P_242": p242_real,
                    "P_222": p222_real,
                    "P_424": p424_real,
                    "indep_product": indep3_real,
                    "joint_enhancement": p242_real / indep3_real if indep3_real else 0.0,
                },
            },
            indent=2,
        )
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
