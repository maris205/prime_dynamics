"""Q_k sieve sequences per the Wang (2026) paper.

Sieve operator S_p = R L^{p-1}: at stage k, every multiple of p_1, ..., p_k
(including the primes themselves) is marked R (1); survivors are L (0).
Index 0 is forced to R by convention.
"""
from __future__ import annotations

import numpy as np
from sympy import primerange


def first_n_primes(n: int) -> list[int]:
    if n <= 0:
        return []
    upper = max(50, int(n * 14))
    primes = list(primerange(2, upper))
    while len(primes) < n + 1:
        upper *= 2
        primes = list(primerange(2, upper))
    return primes[: n + 1]


def Qk_sequence(k: int, horizon: int) -> np.ndarray:
    """Generate Q_k as an int8 array of length `horizon`."""
    if k < 1:
        raise ValueError("k must be >= 1")
    primes = first_n_primes(k)
    used = primes[:k]
    seq = np.zeros(horizon, dtype=np.int8)
    seq[0] = 1
    for p in used:
        seq[0:horizon:p] = 1
    return seq


def Qk_horizon(k: int) -> int:
    """Effective physical horizon p_{k+1}^2 from the paper."""
    primes = first_n_primes(k)
    return primes[k] ** 2
