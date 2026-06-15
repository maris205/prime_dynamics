"""Gap2 exp1: spectral stability of the acim density under parameter drift.

Module 1 (Keller-Liverani) predicts that the absolutely continuous
invariant measure density h_u depends continuously on u near the
Misiurewicz value u_c. We estimate h_u by a long-orbit histogram for a
range of u approaching u_c, and measure the L1 distance ||h_u - h_{u_c}||.

If KL stability holds, ||h_u - h_{u_c}||_{L1} -> 0 as u -> u_c, ideally
with a Holder modulus |u - u_c|^gamma.
"""
import numpy as np

U_C = 1.5436890126920763


def invariant_density_hist(u, n_steps=20_000_000, nbins=400, burn=10000):
    """Histogram estimate of the acim density h_u on [-1, 1]."""
    x = 0.1
    for _ in range(burn):
        x = 1.0 - u * x * x
    xs = np.empty(n_steps, dtype=np.float64)
    for i in range(n_steps):
        x = 1.0 - u * x * x
        xs[i] = x
    hist, edges = np.histogram(xs, bins=nbins, range=(-1.0, 1.0), density=True)
    return hist, edges


def l1_distance(h1, h2, edges):
    w = edges[1] - edges[0]
    return np.sum(np.abs(h1 - h2)) * w


def main():
    np.seterr(over="ignore", invalid="ignore")
    print(f"u_c = {U_C}")
    print("Estimating acim densities by long-orbit histograms (20M steps each)...\n")

    h_c, edges = invariant_density_hist(U_C)

    print(f"{'u':>12} {'u_c - u':>12} {'||h_u - h_uc||_L1':>18}")
    print("-" * 44)
    results = []
    for du in [0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
        u = U_C - du
        h_u, _ = invariant_density_hist(u)
        d = l1_distance(h_u, h_c, edges)
        results.append((du, d))
        print(f"{u:>12.6f} {du:>12.4f} {d:>18.6f}")

    # crude Holder exponent estimate from log-log slope
    dus = np.array([r[0] for r in results])
    ds = np.array([r[1] for r in results])
    mask = ds > 0
    if mask.sum() >= 2:
        slope, intercept = np.polyfit(np.log(dus[mask]), np.log(ds[mask]), 1)
        print(f"\nLog-log fit: ||h_u - h_uc||_L1 ~ |u-u_c|^{slope:.3f}")
        print("(positive slope => density converges as u -> u_c, "
              "consistent with KL stability)")


if __name__ == "__main__":
    main()
