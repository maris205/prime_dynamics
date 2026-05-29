"""1D logistic map x_{n+1} = 1 - u x_n^2 and its symbolic encoding.

Symbolic partition: x > 0 -> R (1), x < 0 -> L (0); the critical point
x_c = 0 is the kneading reference. The band-merging point u_c that hosts
the prime kneading sequence RLR^infty is approximately 1.5436890...
"""
from __future__ import annotations

import numpy as np

U_C = 1.5436890126920763


def iterate(u: float, x0: float, n_steps: int, burn_in: int = 1000) -> np.ndarray:
    x = x0
    for _ in range(burn_in):
        x = 1.0 - u * x * x
    out = np.empty(n_steps, dtype=np.float64)
    for i in range(n_steps):
        x = 1.0 - u * x * x
        out[i] = x
    return out


def symbolize(orbit: np.ndarray) -> np.ndarray:
    """Encode orbit as int8 symbols: 1 if x > 0 (R), 0 otherwise (L)."""
    return (orbit > 0).astype(np.int8)


def gap_sequence(symbols: np.ndarray) -> np.ndarray:
    """Distance between successive L (prime-like) hits.

    Returns gaps g_i = pos_{i+1} - pos_i; empty if fewer than 2 L symbols.
    """
    L_positions = np.flatnonzero(symbols == 0)
    if L_positions.size < 2:
        return np.array([], dtype=np.int64)
    return np.diff(L_positions)
