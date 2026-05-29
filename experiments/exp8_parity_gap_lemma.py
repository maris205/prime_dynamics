"""Experiment 8: Verify the Parity-Gap Lemma numerically.

Lemma (Parity-Gap): For any defective shift m of Q_k inside its horizon,
  - m+1 must be prime,
  - the next prime > m+1 is at least m + p_{k+1}.
Equivalently, a prime gap of length >= p_{k+1} - 1 must occur starting
at m+1.

This experiment locates every defect in Q_k for k where defects exist
(empirically only k=3 and k=5), and explicitly checks the lemma's
two predictions for each defective shift.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from sympy import isprime, nextprime

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.sieve import Qk_horizon, Qk_sequence, first_n_primes


def find_defective_shifts(seq: np.ndarray) -> list[int]:
    n = len(seq)
    cum_R = np.cumsum(seq)
    bad = []
    for shift in range(1, n):
        orig = seq[: n - shift]
        shifted = seq[shift:]
        diffs = orig != shifted
        if not diffs.any():
            continue
        first = int(np.argmax(diffs))
        r_count = int(cum_R[first - 1]) if first > 0 else 0
        base = -1 if orig[first] < shifted[first] else 1
        cmp_val = -base if (r_count & 1) else base
        if cmp_val == -1:
            bad.append(shift)
    return bad


def verify_lemma(k: int) -> None:
    primes = first_n_primes(k)
    p_next = primes[k]
    N = Qk_horizon(k)
    seq = Qk_sequence(k, N)
    bad = find_defective_shifts(seq)

    print(f"\nk = {k}, p_{{k+1}} = {p_next}, horizon N = {N}")
    print(f"  Lemma demands: prime gap of length >= {p_next - 1} starting at m+1.")
    if not bad:
        print("  No defective shifts (lemma vacuously holds).")
        return
    for m in bad:
        is_prime_m1 = isprime(m + 1)
        gap = nextprime(m + 1) - (m + 1)
        bound = p_next - 1
        ok = is_prime_m1 and gap >= bound
        marker = "OK" if ok else "FAIL"
        print(
            f"  shift m = {m:>4}, m+1 = {m + 1:>4} prime? {is_prime_m1}, "
            f"next prime gap = {gap:>3}, lemma demands >= {bound}: {marker}"
        )


def main() -> None:
    print("Verifying the Parity-Gap Lemma on every defective shift of Q_k:")
    for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 50, 100]:
        verify_lemma(k)


if __name__ == "__main__":
    main()
