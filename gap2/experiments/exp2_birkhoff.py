"""Gap2 exp2: numerical verification of the sequential Birkhoff theorem.

Theorem (as first stated): for u_n -> u_c with |u_n - u_c| <= c (log n)^{-beta},
the time-average (1/N) sum phi(Phi_n(x0)) converges to the autonomous
spatial average int phi dmu_{u_c}.

phi = indicator of the left branch {x<0} (the L-symbol frequency).

The first run revealed: convergence holds for large beta (e.g. 2) but
FAILS for small beta (0.5) because the early schedule values u_n are
far below the admissible window and the orbit escapes to infinity
(overflow). This script pins down:

  (A) the critical beta (fixed c=1, sweep beta),
  (B) whether a CLAMPED schedule u_n = max(u_c - c/(log n)^beta, u_min)
      restores convergence for ALL beta -- testing the "keep u_n in the
      admissible window" hypothesis.
"""
import numpy as np

U_C = 1.5436890126920763   # band-merging (Misiurewicz) parameter
U_MIN = 1.40               # lower edge of a safe admissible window near u_c


def autonomous_L_freq(u, n_steps, x0=0.1, burn=10000):
    x = x0
    for _ in range(burn):
        x = 1.0 - u * x * x
    c = 0
    for _ in range(n_steps):
        x = 1.0 - u * x * x
        if x < 0:
            c += 1
    return c / n_steps


def drifting_L_freq(u_c, c_drift, beta, n_steps, x0=0.1, clamp=False):
    """Sequential cocycle time average with u_n = u_c - c/(log n)^beta.

    If clamp=True, u_n is floored at U_MIN to keep it in the admissible
    window (tests whether early-transient escape is the failure cause).
    Returns (avg, escaped) where escaped flags overflow / divergence.
    """
    x = x0
    cnt = 0
    escaped = False
    for n in range(1, n_steps + 1):
        u_n = u_c - c_drift / (np.log(n + 2.0) ** beta)
        if clamp and u_n < U_MIN:
            u_n = U_MIN
        x = 1.0 - u_n * x * x
        if not np.isfinite(x) or abs(x) > 1.0 + 1e-9:
            escaped = True
            break
        if x < 0:
            cnt += 1
    return (cnt / n_steps, escaped)


def main():
    np.seterr(over="ignore", invalid="ignore")
    print(f"u_c = {U_C}")
    target = autonomous_L_freq(U_C, 5_000_000)
    print(f"Autonomous L-frequency at u_c (Birkhoff target): {target:.6f}")

    N = 2_000_000

    print("\n=== (A) Critical beta sweep (c=1, unclamped) ===")
    print(f"{'beta':>6} {'drift avg':>12} {'|diff|':>10} {'escaped':>9}")
    print("-" * 42)
    for beta in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]:
        avg, esc = drifting_L_freq(U_C, 1.0, beta, N)
        print(f"{beta:>6} {avg:>12.6f} {abs(avg-target):>10.6f} {str(esc):>9}")

    print("\n=== (B) Clamped schedule (floor u_n at U_MIN=1.40) ===")
    print(f"{'beta':>6} {'c':>5} {'drift avg':>12} {'|diff|':>10} {'escaped':>9}")
    print("-" * 48)
    for beta in [0.5, 1.0, 2.0]:
        for c_drift in [1.0, 5.0]:
            avg, esc = drifting_L_freq(U_C, c_drift, beta, N, clamp=True)
            print(f"{beta:>6} {c_drift:>5} {avg:>12.6f} "
                  f"{abs(avg-target):>10.6f} {str(esc):>9}")

    print("\n=== (C) Convergence of clamped, c=1, beta=1 across N ===")
    print(f"{'N':>10} {'drift avg':>12} {'|diff|':>10}")
    print("-" * 34)
    for Nx in [10**5, 10**6, 5*10**6, 2*10**7]:
        avg, esc = drifting_L_freq(U_C, 1.0, 1.0, Nx, clamp=True)
        print(f"{Nx:>10} {avg:>12.6f} {abs(avg-target):>10.6f}")

    print("\nReading:")
    print("- (A) tells us the unclamped critical beta (escape vs converge).")
    print("- (B) tests whether clamping into the admissible window rescues")
    print("      ALL beta -- if yes, the right hypothesis is 'u_n in U', not")
    print("      a beta threshold.")
    print("- (C) confirms genuine convergence (|diff| -> 0) for the clamped")
    print("      schedule as N grows.")


if __name__ == "__main__":
    main()
