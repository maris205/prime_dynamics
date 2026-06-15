"""Gap2 Figure 1: two-panel verification of the sequential Birkhoff theorem.

Panel (a): acim density stability -- ||h_u - h_uc||_L1 vs |u - u_c| on
           log-log axes, showing the Holder-1/2 modulus (Module 1).
Panel (b): sequential time-average convergence -- |drift avg - target|
           vs N for several beta, showing convergence with beta-dependent
           rate (the main theorem).

Outputs figures/fig1_gap2_verification.png.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pathlib

U_C = 1.5436890126920763
OUT = pathlib.Path(__file__).resolve().parent.parent / "paper" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def acim_hist(u, n_steps, nbins=400, burn=10000):
    x = 0.1
    for _ in range(burn):
        x = 1.0 - u * x * x
    xs = np.empty(n_steps)
    for i in range(n_steps):
        x = 1.0 - u * x * x
        xs[i] = x
    h, e = np.histogram(xs, bins=nbins, range=(-1, 1), density=True)
    return h, e


def l1(h1, h2, e):
    return np.sum(np.abs(h1 - h2)) * (e[1] - e[0])


def drift_L_freq(c, beta, N, x0=0.1):
    x = x0
    cnt = 0
    for n in range(1, N + 1):
        u = U_C - c / (np.log(n + 2.0) ** beta)
        x = 1.0 - u * x * x
        if not np.isfinite(x):
            return np.nan
        if x < 0:
            cnt += 1
    return cnt / N


def main():
    np.seterr(over="ignore", invalid="ignore")
    plt.style.use("seaborn-v0_8-paper")
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.3), dpi=150)

    # --- Panel A: density stability ---
    print("Panel A: acim density convergence...")
    n_dens = 10_000_000
    h_c, edges = acim_hist(U_C, n_dens)
    dus = [0.05, 0.02, 0.01, 0.005, 0.002, 0.001]
    ds = []
    for du in dus:
        h_u, _ = acim_hist(U_C - du, n_dens)
        ds.append(l1(h_u, h_c, edges))
        print(f"  du={du:.4f}  L1={ds[-1]:.4f}")
    dus = np.array(dus); ds = np.array(ds)
    slope, icpt = np.polyfit(np.log(dus), np.log(ds), 1)

    axA.loglog(dus, ds, "o-", color="#1f77b4", markersize=7,
               label=f"data, slope $\\approx {slope:.2f}$")
    axA.loglog(dus, np.exp(icpt) * dus**0.5, "r--", alpha=0.7,
               label="Hölder-$1/2$ ref")
    axA.set_xlabel(r"$|u - u_c|$")
    axA.set_ylabel(r"$\|h_u - h_{u_c}\|_{L^1}$")
    axA.set_title("(a) acim density stability (Module 1)", fontsize=11)
    axA.legend(fontsize=9)
    axA.grid(True, which="both", ls="--", alpha=0.4)

    # --- Panel B: sequential Birkhoff convergence ---
    print("Panel B: sequential Birkhoff convergence...")
    target = 0.220693
    Ns = [10**5, 3*10**5, 10**6, 3*10**6, 10**7]
    colors = {1.0: "#d62728", 2.0: "#2ca02c", 3.0: "#9467bd"}
    for beta in [1.0, 2.0, 3.0]:
        diffs = []
        for N in Ns:
            avg = drift_L_freq(1.0, beta, N)
            diffs.append(abs(avg - target))
            print(f"  beta={beta} N={N} diff={diffs[-1]:.5f}")
        axB.loglog(Ns, diffs, "o-", color=colors[beta], markersize=6,
                   label=fr"$\beta={beta:.0f}$")
    axB.set_xlabel(r"$N$")
    axB.set_ylabel(r"time-average error  $|\bar\varphi_N - \int\varphi\,d\mu_{u_c}|$")
    axB.set_title("(b) sequential Birkhoff convergence ($c=1$)", fontsize=11)
    axB.legend(fontsize=9)
    axB.grid(True, which="both", ls="--", alpha=0.4)

    fig.tight_layout()
    out = OUT / "fig1_gap2_verification.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nWrote {out}")
    print(f"Panel A Holder exponent: {slope:.3f}")


if __name__ == "__main__":
    main()
