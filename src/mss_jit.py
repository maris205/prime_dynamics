"""Numba-jit defect counter. ~100-1000x faster than the pure-numpy version.

Bit-exact equivalent to src.mss.count_defects. Used for the large-k
sweep where horizons exceed 10^6.
"""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def _count_defects(seq: np.ndarray) -> int:
    n = seq.shape[0]
    if n < 2:
        return 0
    defects = 0
    for shift in range(1, n):
        r_count = 0
        for i in range(n - shift):
            a = seq[i]
            b = seq[i + shift]
            if a != b:
                if r_count % 2 == 1:
                    if a > b:
                        defects += 1
                else:
                    if a < b:
                        defects += 1
                break
            if a == 1:
                r_count += 1
    return defects


def count_defects_jit(seq: np.ndarray) -> tuple[int, float]:
    seq = np.ascontiguousarray(seq, dtype=np.int8)
    d = int(_count_defects(seq))
    n = len(seq)
    return d, d / (n - 1) if n > 1 else 0.0
