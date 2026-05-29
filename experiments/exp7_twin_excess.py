"""Experiment 7: Twin-pair (gap-2) excess vs Cramer baseline.

Compares the empirical g=2 mass mu_2 of the logistic orbit at u_c against
the Cramer-stochastic baseline mu_2^{rand} = rho * (1 - rho)^1 where rho
is the L-frequency. The ratio mu_2 / mu_2^{rand} measures the discrete
arithmetic 'twin excess' built into the chaotic dynamics, analogous to
the Hardy-Littlewood factor 2 C_2 / e^{-2} for real primes.

Reads from results/exp2_large.json (the 5e8-step run already done).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def main() -> None:
    data = json.loads((ROOT / "results" / "exp2_large.json").read_text())
    hist = {int(g): float(m) for g, m in data["histogram"].items()}
    n_steps = int(data["n_steps"])

    # mu_2 is the empirical gap-2 mass.
    mu_2_logistic = hist.get(2, 0.0)

    # L-frequency: total L count / n_steps. We can recover rho from the
    # mean gap = 1 / rho.
    g_pos = np.array([g for g in sorted(hist) if hist[g] > 0])
    g_mass = np.array([hist[g] for g in g_pos])
    mean_gap = float((g_pos * g_mass).sum())
    rho = 1.0 / mean_gap
    print(f"L-frequency rho = {rho:.6f}")
    print(f"Mean gap        = {mean_gap:.6f}")

    # Cramer stochastic baseline: gaps are geometric with parameter rho,
    # so P(gap = g) = (1 - rho)^{g-1} * rho. For g = 2 this is (1-rho) * rho.
    # But our parity rigidity halves the support to even gaps only, with
    # total mass conserved. The matched 'parity-Cramer' model has P(g=2) =
    # rho_eff * (1 - rho_eff)^0 where rho_eff = 1/E[g] under the constraint
    # that all odd gaps are zero.
    mu_2_cramer_naive = rho * (1.0 - rho)
    mu_2_cramer_parity = rho  # parity-restricted baseline: P(g=2) = rho_eff

    excess_naive = mu_2_logistic / mu_2_cramer_naive if mu_2_cramer_naive > 0 else float("nan")
    excess_parity = mu_2_logistic / mu_2_cramer_parity if mu_2_cramer_parity > 0 else float("nan")

    p_inf = 0.5964
    mu_2_geom = (1 - p_inf)
    excess_geom = mu_2_logistic / mu_2_geom

    print(f"\nGap-2 mass:")
    print(f"  empirical (logistic at u_c)         mu_2 = {mu_2_logistic:.6f}")
    print(f"  naive Cramer baseline           mu_2_C  = {mu_2_cramer_naive:.6f}")
    print(f"  parity-Cramer baseline          mu_2_PC = {mu_2_cramer_parity:.6f}")
    print(f"  geometric (1 - p_inf), p_inf={p_inf}  = {mu_2_geom:.6f}")

    print(f"\nDiscrete-twin excess factors:")
    print(f"  mu_2 / mu_2_naive  = {excess_naive:.4f}")
    print(f"  mu_2 / mu_2_parity = {excess_parity:.4f}")
    print(f"  mu_2 / mu_2_geom   = {excess_geom:.4f}")

    print("\nReal Hardy-Littlewood twin factor: 2 C_2 = 1.32032 ...")
    print("(The 1D model captures parity rigidity; mod-3 resonance is absent)")

    out_path = ROOT / "results" / "exp7_twin_excess.json"
    out_path.write_text(
        json.dumps(
            {
                "rho_logistic": rho,
                "mean_gap": mean_gap,
                "mu_2_logistic": mu_2_logistic,
                "mu_2_cramer_naive": mu_2_cramer_naive,
                "mu_2_cramer_parity": mu_2_cramer_parity,
                "p_infty": p_inf,
                "excess_naive": excess_naive,
                "excess_parity": excess_parity,
                "excess_geometric": excess_geom,
                "twin_const_hardy_littlewood_2C2": 1.3203236316,
            },
            indent=2,
        )
    )
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
