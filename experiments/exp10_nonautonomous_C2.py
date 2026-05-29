"""Experiment 10: Non-autonomous logistic gap statistics (Direction B).

Implements the original paper's parameter drift
    u_n = u_c - c / (ln n)^2
to test whether the twin-prime constant C_2 = 0.6601618 emerges from
the LRL pattern density without the post-hoc scale factor used in
fig9-twin_prime_constant.ipynb (which fitted scale_factor = 12.7374).

The classical Hardy-Littlewood prediction for the number of twin
primes up to N is
    pi_2(N) ~ 2 C_2 * Li_2(N) ~ 2 C_2 * N / (ln N)^2.
We mimic this with the chaotic LRL events: count visits to the
LRL pattern (gap-2 within a length-3 window), sum 1 / (ln n)^2 weights,
divide by 2 Li_2(N), and check convergence.
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
from numba import njit
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.logistic import U_C


@njit(cache=True)
def run_drift(u_c: float, c: float, n_steps: int, x0: float, burn_in: int):
    """Iterate x_{n+1} = 1 - u_n x_n^2 with u_n = u_c - c / (ln n)^2.

    Returns:
      lrl_weighted: sum of 1/(ln n)^2 over indices where pattern L-R-L
                    occurred and the centre symbol's gap to the next L = 2.
      n_L: number of L symbols (x < 0).
      lrl_count: unweighted count of L-R-L windows.
    """
    x = x0
    for _ in range(burn_in):
        x = 1.0 - u_c * x * x
    s_prev2 = 1
    s_prev1 = 1
    lrl_w = 0.0
    n_L = 0
    lrl_count = 0
    for n in range(2, n_steps):
        u_n = u_c - c / (math.log(n + 2.0) ** 2)
        x = 1.0 - u_n * x * x
        s_curr = 1 if x > 0 else 0
        if s_curr == 0:
            n_L += 1
        if s_prev2 == 0 and s_prev1 == 1 and s_curr == 0:
            ln_n = math.log(n + 2.0)
            w = 1.0 / (ln_n * ln_n)
            lrl_w += w
            lrl_count += 1
        s_prev2 = s_prev1
        s_prev1 = s_curr
    return lrl_w, n_L, lrl_count


def Li_2(N: float) -> float:
    val, _ = quad(lambda t: 1.0 / math.log(t) ** 2, 2.0, N)
    return val


def main(n_steps: int = 10_000_000, c: float = 1.0, x0: float = 0.1) -> None:
    burn_in = 10_000
    print(f"Running non-autonomous logistic with u_n = u_c - {c} / (ln n)^2")
    print(f"  u_c = {U_C}")
    print(f"  n_steps = {n_steps:,}")
    t0 = time.time()
    lrl_w, n_L, lrl_count = run_drift(U_C, c, n_steps, x0, burn_in)
    print(f"  wall = {time.time() - t0:.1f}s")
    print(f"  L symbols   = {n_L:,}  (rho = {n_L / n_steps:.6f})")
    print(f"  LRL windows = {lrl_count:,}")
    print(f"  weighted LRL = {lrl_w:.6f}")

    li2 = Li_2(n_steps)
    HL_C2 = 0.6601618158
    HL_2C2 = 2 * HL_C2

    C_estimate = lrl_w / (HL_2C2 * li2)
    print(f"\nLi_2(N)            = {li2:.4f}")
    print(f"2 C_2 * Li_2(N)    = {HL_2C2 * li2:.4f}")
    print(f"\n[Headline]  weighted_LRL / (2 C_2 * Li_2)  =  {C_estimate:.6f}")
    print("           (this is the post-hoc scale factor needed to recover C_2;")
    print("            a value of 1.0 would mean C_2 emerges naturally)")

    out = ROOT / "results" / "exp10_nonautonomous_C2.json"
    out.write_text(
        json.dumps(
            {
                "u_c": U_C,
                "c": c,
                "n_steps": n_steps,
                "n_L": n_L,
                "lrl_count": lrl_count,
                "lrl_weighted": lrl_w,
                "Li_2_N": li2,
                "twin_constant_C_2": HL_C2,
                "scale_to_match_C2": C_estimate,
            },
            indent=2,
        )
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
