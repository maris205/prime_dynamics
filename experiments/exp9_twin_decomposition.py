"""Experiment 9: Twin-pair density decomposition (Direction A).

The autonomous twin-pair (gap=2) density at u_c factors as
    twin_density = rho_L * mu_2
where rho_L is the L-frequency and mu_2 is the conditional gap-2
probability. We further decompose mu_2 into three factors:

    mu_2 = baseline * parity_factor * LRL_excess

where:
  - baseline is the bare-Cramer iid expectation rho_L * (1 - rho_L)
  - parity_factor = mu_2 / (rho_L * (1 - rho_L)) is the rigidity multiplier
    forcing all probability mass onto even gaps
  - LRL_excess = mu_2 / mu_2^geometric measures the genuine short-range
    enhancement above the asymptotic geometric law

For real primes, the analogous decomposition is the Hardy-Littlewood
formula: twin density / Cramer baseline = 2 * C_2 = 1.32032.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> None:
    log = json.loads((ROOT / "results" / "exp2_large.json").read_text())
    real = json.loads((ROOT / "results" / "exp3_real_prime_gaps.json").read_text())

    log_hist = {int(g): float(m) for g, m in log["histogram"].items()}
    real_hist = {int(g): float(m) for g, m in real["histogram"].items()}

    rho_log = 1.0 / sum(g * log_hist[g] for g in log_hist)
    mu2_log = log_hist.get(2, 0.0)
    base_log = rho_log * (1 - rho_log)
    parity_log = mu2_log / base_log
    p_inf = 0.5964
    mu2_geom = 1 - p_inf
    excess_log = mu2_log / mu2_geom

    twin_density_log = rho_log * mu2_log

    rho_real = 1.0 / sum(g * real_hist[g] for g in real_hist)
    mu2_real = real_hist.get(2, 0.0)
    base_real = rho_real * (1 - rho_real)
    parity_real = mu2_real / base_real
    twin_density_real = rho_real * mu2_real
    HL_2C2 = 1.3203236316  # Hardy-Littlewood twin constant 2 C_2

    print("=" * 70)
    print("Twin-pair density decomposition")
    print("=" * 70)

    print("\n[1D logistic at u_c]")
    print(f"  rho_L (L-frequency)            = {rho_log:.6f}")
    print(f"  mu_2 (conditional gap-2)       = {mu2_log:.6f}")
    print(f"  twin density rho_L * mu_2      = {twin_density_log:.6f}")
    print(f"  Cramer baseline rho(1-rho)     = {base_log:.6f}")
    print(f"  parity factor mu_2 / baseline  = {parity_log:.4f}")
    print(f"  asymptotic-geom 1 - p_inf      = {mu2_geom:.6f}")
    print(f"  LRL excess mu_2 / (1-p_inf)    = {excess_log:.4f}")

    print("\n[Real primes up to 5e6]")
    print(f"  rho_L = pi(N)/N                = {rho_real:.6f}")
    print(f"  mu_2 (cond. gap-2)             = {mu2_real:.6f}")
    print(f"  twin density rho_L * mu_2      = {twin_density_real:.6f}")
    print(f"  Cramer baseline rho(1-rho)     = {base_real:.6f}")
    print(f"  HL ratio mu_2 / baseline       = {parity_real:.4f}")
    print(f"  Hardy-Littlewood 2 C_2         = {HL_2C2:.4f}")
    print(f"  ratio HL_real / HL_const       = {parity_real / HL_2C2:.4f}")

    print("\n[Decomposition comparison]")
    print(f"  parity factor (logistic)       = {parity_log:.4f}")
    print(f"  parity factor (real primes)    = {parity_real:.4f}  vs  2 C_2 = {HL_2C2:.4f}")
    print(f"  ratio (logistic / real)        = {parity_log / parity_real:.4f}")

    out = ROOT / "results" / "exp9_twin_decomposition.json"
    out.write_text(
        json.dumps(
            {
                "logistic": {
                    "rho_L": rho_log,
                    "mu_2": mu2_log,
                    "twin_density": twin_density_log,
                    "cramer_baseline": base_log,
                    "parity_factor": parity_log,
                    "p_infty": p_inf,
                    "mu_2_geometric": mu2_geom,
                    "LRL_excess": excess_log,
                },
                "real_primes": {
                    "rho_L": rho_real,
                    "mu_2": mu2_real,
                    "twin_density": twin_density_real,
                    "cramer_baseline": base_real,
                    "HL_ratio": parity_real,
                    "twin_constant_2C2": HL_2C2,
                },
            },
            indent=2,
        )
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
