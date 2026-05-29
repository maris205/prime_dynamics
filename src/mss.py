"""MSS (Metropolis-Stein-Stein) parity-lexicographic comparison utilities.

Implements the admissibility test for kneading sequences of unimodal maps:
a sequence Q is *admissible* iff for every shift m >= 0,  sigma^m(Q) <= Q
under the parity-twisted lex order, where the comparison rule flips whenever
the common prefix contains an odd number of R symbols.
"""
from __future__ import annotations

import numpy as np


def parity_lex_compare(a: np.ndarray, b: np.ndarray) -> int:
    """Return -1, 0, +1 for a vs b under the MSS parity-lex order.

    Inputs are int8 arrays with 0 = L, 1 = R. Equal-length compared
    element-wise; tie on the shorter common prefix returns 0.
    """
    n = min(len(a), len(b))
    if n == 0:
        return 0
    diffs = a[:n] != b[:n]
    if not np.any(diffs):
        return 0

    first = int(np.argmax(diffs))
    r_count = int(np.sum(a[:first])) if first > 0 else 0

    base = -1 if a[first] < b[first] else 1
    return -base if (r_count & 1) else base


def count_defects(seq: np.ndarray, max_shift: int | None = None) -> tuple[int, float]:
    """Count shifts m where sigma^m(seq) strictly exceeds seq under MSS order.

    Vectorized: builds the parity-flip mask once via cumulative R-count, then
    handles each shift in O(n) numpy ops. Returns (defect_count, density).
    """
    n = len(seq)
    if n < 2:
        return 0, 0.0
    if max_shift is None:
        max_shift = n - 1

    cum_R = np.cumsum(seq)
    defects = 0
    for shift in range(1, max_shift + 1):
        orig = seq[: n - shift]
        shifted = seq[shift:]
        diffs = orig != shifted
        if not diffs.any():
            continue
        first = int(np.argmax(diffs))
        r_count = int(cum_R[first - 1]) if first > 0 else 0
        base = -1 if orig[first] < shifted[first] else 1
        cmp_val = -base if (r_count & 1) else base
        if cmp_val == -1:  # original < shifted -> defect
            defects += 1
    return defects, defects / max_shift
