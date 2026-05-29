"""Gap-spectrum analysis: histograms and Markov geometric-decay diagnostics.

Two reference distributions are compared:
- 1D unimodal map at u_c -> geometric decay mu_{2m+2} = p * mu_{2m}
- Real primes -> Hardy-Littlewood with mod-3 resonance peak at gap 6
"""
from __future__ import annotations

import numpy as np
from sympy import primerange


def gap_histogram(gaps: np.ndarray, max_gap: int = 30) -> dict[int, float]:
    """Normalized histogram of integer gaps in [1, max_gap]."""
    if gaps.size == 0:
        return {}
    counts = np.bincount(gaps, minlength=max_gap + 1)[: max_gap + 1]
    total = counts.sum()
    if total == 0:
        return {}
    return {g: counts[g] / total for g in range(1, max_gap + 1)}


def even_gap_ratios(hist: dict[int, float]) -> dict[int, float]:
    """Ratios mu_{2m}/mu_2 used to test geometric decay."""
    base = hist.get(2, 0.0)
    if base == 0.0:
        return {}
    return {2 * m: hist.get(2 * m, 0.0) / base for m in range(1, 11) if 2 * m in hist}


def geometric_fit_ratio(hist: dict[int, float]) -> float:
    """Estimate the common ratio p from successive even-gap masses."""
    even = [(g, hist[g]) for g in sorted(hist) if g % 2 == 0 and hist[g] > 0]
    if len(even) < 2:
        return float("nan")
    ratios = [even[i + 1][1] / even[i][1] for i in range(len(even) - 1)]
    return float(np.mean(ratios))


def real_prime_gaps(N: int) -> np.ndarray:
    """Gaps between consecutive primes up to N."""
    primes = np.array(list(primerange(2, N)), dtype=np.int64)
    if primes.size < 2:
        return np.array([], dtype=np.int64)
    return np.diff(primes)
