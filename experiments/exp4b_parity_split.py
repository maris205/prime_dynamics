"""Experiment 4b: 4-state parity-split Markov chain.

States:
  A    : current symbol L
  B_o  : current symbol R, odd # of R's since last L
  B_e  : current symbol R, even # of R's since last L

Predicted transitions (from the parity rigidity of unimodal flow at u_c):
  A    -> B_o   with probability 1
  B_o  -> A     with probability alpha
        -> B_e  with probability 1 - alpha
  B_e  -> B_o   with probability 1

If correct, gap masses obey  mu_{2m} = alpha * (1 - alpha)^{m-1},  exact
geometric law with ratio p = 1 - alpha. Verifies against the empirical
ratio mu_4/mu_2 from exp2 and against the empirical chain itself.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.logistic import U_C, iterate, symbolize


def parity_split_states(symbols: np.ndarray) -> np.ndarray:
    """0 = A, 1 = B_o (odd R-count), 2 = B_e (even R-count)."""
    states = np.zeros(len(symbols), dtype=np.int8)
    parity = 0  # # R's since last L, mod 2
    for i, s in enumerate(symbols):
        if s == 0:
            states[i] = 0
            parity = 0
        else:
            parity ^= 1
            states[i] = 1 if parity == 1 else 2
    return states


def main(n_steps: int = 5_000_000, x0: float = 0.1) -> None:
    print(f"Iterating logistic map at u = {U_C} for {n_steps:,} steps...")
    orbit = iterate(U_C, x0, n_steps, burn_in=10_000)
    sym = symbolize(orbit)
    states = parity_split_states(sym)

    counts = np.bincount(states, minlength=3)
    pi = counts / counts.sum()

    T = np.zeros((3, 3), dtype=np.int64)
    for s, t in zip(states[:-1], states[1:]):
        T[s, t] += 1

    P = np.zeros((3, 3), dtype=np.float64)
    for i in range(3):
        s = T[i].sum()
        if s > 0:
            P[i] = T[i] / s

    labels = ["A", "B_o", "B_e"]
    print("\nStationary distribution:")
    for lab, p in zip(labels, pi):
        print(f"  pi_{lab} = {p:.6f}")

    print("\nRow-stochastic transition matrix:")
    print("            ->A        ->B_o      ->B_e")
    for i, lab in enumerate(labels):
        print(f"  from {lab:>4}: {P[i, 0]:>10.6f} {P[i, 1]:>10.6f} {P[i, 2]:>10.6f}")

    alpha = P[1, 0]
    p_geom = 1.0 - alpha
    print("\nKey transitions (skeleton check):")
    print(f"  P(A   -> B_o) = {P[0, 1]:.6f}   (predicted 1.0)")
    print(f"  P(B_o -> A)   = {P[1, 0]:.6f}   (predicted alpha)")
    print(f"  P(B_o -> B_e) = {P[1, 2]:.6f}   (predicted 1 - alpha)")
    print(f"  P(B_e -> B_o) = {P[2, 1]:.6f}   (predicted 1.0)")
    print(f"  P(A   -> A)   = {P[0, 0]:.6f}   (predicted 0)")
    print(f"  P(A   -> B_e) = {P[0, 2]:.6f}   (predicted 0)")
    print(f"  P(B_e -> A)   = {P[2, 0]:.6f}   (predicted 0)")
    print(f"  P(B_e -> B_e) = {P[2, 2]:.6f}   (predicted 0)")

    print(f"\nalpha = {alpha:.6f}")
    print(f"Geometric ratio  p = 1 - alpha = {p_geom:.6f}")
    print(f"Cross-check:     p_hat from exp2 ~ 0.582")

    print("\nPredicted gap mass mu_{2m} = alpha * (1-alpha)^{m-1}:")
    for m in range(1, 8):
        pred = alpha * p_geom ** (m - 1)
        print(f"  m = {m}, g = {2 * m},  mu_pred = {pred:.6f}")

    out = ROOT / "results" / "exp4b_parity_split.json"
    out.write_text(
        json.dumps(
            {
                "u": U_C,
                "n_steps": n_steps,
                "pi": pi.tolist(),
                "transition_matrix": P.tolist(),
                "alpha": float(alpha),
                "p_geometric": float(p_geom),
            },
            indent=2,
        )
    )
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
