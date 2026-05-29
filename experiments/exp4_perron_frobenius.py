"""Experiment 4: Perron-Frobenius computation of the geometric ratio p.

Builds the empirical 3-state Markov chain on (A, B, C) where
  A: current symbol is L (orbit in (a_1, 0))
  B: current symbol is R AND next symbol is R (intermediate composite step)
  C: current symbol is R AND next symbol is L (terminal composite step)

Topologically A -> C, B -> C, and C -> A | B with probability q | 1-q.
Verifies that the empirical transition matrix matches this skeleton and
extracts q numerically. The geometric ratio p of Theorem 1 is then
p = 1 - q. Cross-checks against the empirical mu_4/mu_2 from exp2.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.logistic import U_C, iterate, symbolize


def empirical_chain(symbols: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict]:
    """Return the 3-state classification and the 3x3 transition counts.

    State 0 = A (current=L), 1 = B (R, next R), 2 = C (R, next L).
    """
    sym = symbols.astype(np.int8)
    states = np.empty(len(sym) - 1, dtype=np.int8)
    L_mask = sym[:-1] == 0
    R_mask = ~L_mask
    next_R = sym[1:] == 1
    states[L_mask] = 0
    states[R_mask & next_R] = 1
    states[R_mask & ~next_R] = 2

    transitions = np.zeros((3, 3), dtype=np.int64)
    for s, t in zip(states[:-1], states[1:]):
        transitions[s, t] += 1
    pi = np.bincount(states, minlength=3) / len(states)

    info = {
        "n_steps": int(len(states)),
        "pi_A": float(pi[0]),
        "pi_B": float(pi[1]),
        "pi_C": float(pi[2]),
    }
    return pi, transitions, info


def normalise_rows(M: np.ndarray) -> np.ndarray:
    out = np.zeros_like(M, dtype=np.float64)
    for i in range(M.shape[0]):
        s = M[i].sum()
        if s > 0:
            out[i] = M[i] / s
    return out


def main(n_steps: int = 5_000_000, x0: float = 0.1) -> None:
    print(f"Iterating logistic map at u = {U_C} for {n_steps:,} steps...")
    orbit = iterate(U_C, x0, n_steps, burn_in=10_000)
    sym = symbolize(orbit)

    pi, T_counts, info = empirical_chain(sym)
    P = normalise_rows(T_counts)

    print("\nStationary distribution:")
    print(f"  pi_A = {pi[0]:.6f}  (L symbols)")
    print(f"  pi_B = {pi[1]:.6f}  (R, next R)")
    print(f"  pi_C = {pi[2]:.6f}  (R, next L)")
    print(f"  pi_A + pi_B - pi_C = {pi[0] + pi[1] - pi[2]: .2e}  (should be 0)")

    print("\nRow-stochastic transition matrix P[i, j] = P(state j | state i):")
    print("           ->A         ->B         ->C")
    for i, lab in enumerate(["A", "B", "C"]):
        print(f"  from {lab}: {P[i, 0]:>10.6f}  {P[i, 1]:>10.6f}  {P[i, 2]:>10.6f}")

    q = P[2, 0]
    p_an = 1.0 - q
    print("\nKey conditional probabilities from C:")
    print(f"  q = P(C -> A)       = {q:.6f}    (predicted from skeleton)")
    print(f"  1 - q = P(C -> B)   = {1 - q:.6f}")
    print(f"\nGeometric ratio p = 1 - q = {p_an:.6f}")
    print(f"Empirical p_hat (from exp2) ~ 0.582")

    eigvals, eigvecs = np.linalg.eig(P.T)
    idx = int(np.argmin(np.abs(eigvals - 1.0)))
    pf = np.real(eigvecs[:, idx])
    pf = pf / pf.sum()
    print(f"\nPerron-Frobenius left-eigenvector at lambda = 1:")
    print(f"  pi_PF = ({pf[0]:.6f}, {pf[1]:.6f}, {pf[2]:.6f})")
    print(f"  empirical pi = ({pi[0]:.6f}, {pi[1]:.6f}, {pi[2]:.6f})")
    print(f"  L1 distance = {np.abs(pf - pi).sum():.2e}")

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "exp4_perron_frobenius.json"
    out_path.write_text(
        json.dumps(
            {
                "u": U_C,
                "n_steps": n_steps,
                "pi": pi.tolist(),
                "transition_matrix": P.tolist(),
                "transition_counts": T_counts.tolist(),
                "q_C_to_A": q,
                "p_analytic": p_an,
                "PF_eigenvector": pf.tolist(),
            },
            indent=2,
        )
    )
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
