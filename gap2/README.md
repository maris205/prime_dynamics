# Sequential Birkhoff Theorem for Slow Logarithmic Drift

Companion repository for the manuscript

> **A Sequential Birkhoff Theorem for Slow Logarithmic Drift in Non-Uniformly Expanding Unimodal Maps**
> Liang Wang

This is a standalone follow-up to the prime-dynamics paper
([../paper/](../paper/), submitted to *Nonlinearity*). It rigorizes the
non-autonomous ergodic foundation that the prime paper leaves as an
informal remark: that a slowly drifting parameter schedule
$u_n \to u_c$ does not change the long-run Cesàro statistics of the
symbolic orbit.

## Main result

Let $f_u(x) = 1 - u x^2$ and let $u_c$ be a Misiurewicz (band-merging)
parameter. For the sequential composition
$\Phi_N = f_{u_N} \circ \cdots \circ f_{u_1}$ with $u_n \to u_c$:

- **Theorem A (conditional, unconditional in the drift rate).** Under a
  *uniform inducing scheme* (uniform Young tower + uniform
  Lasota–Yorke + Keller–Liverani stability), for every BV observable
  the time average converges *in mean / in L² / in probability* to the
  autonomous spatial average $\int \varphi \, d\mu_{u_c}$, whenever the
  drift tail $\Delta_m = \sup_{k\ge m}|u_k - u_c| \to 0$.

- **Corollary 1 (a.e., β > 1).** For the logarithmic schedule
  $|u_n - u_c| \le c(\log n)^{-\beta}$ with $\beta > 1$, the convergence
  holds Lebesgue-almost-everywhere. The threshold $\beta > 1$ is the
  point at which the second-moment estimate becomes summable along a
  ratio-one subsequence.

The proof passes to the induced first-return map (uniformly expanding),
uses a uniform spectral gap, and controls the accumulated drift error
by a Cesàro estimate.

### What it does and does not give

The theorem proves that the **symbolic cylinder frequencies** of the
drifting orbit inherit the band-merging statistics $\mu_{u_c}$. It does
**not** by itself produce the $1/\log n$ **density envelope** of an
arithmetic sequence — that is a non-stationary quantity requiring a
weighted / shrinking-target estimator, outside the scope here. See
Section 6 of the paper.

## Layout

```
gap2/
├── PROJECT.md            scope and three-module plan
├── paper/
│   ├── main.tex          8-page manuscript
│   ├── main.pdf
│   ├── refs.bib
│   └── TITLE_ABSTRACT.md title + abstract for submission forms
└── experiments/
    ├── exp1_drift_bv.py  acim density stability: ||h_u - h_uc|| ~ |u-u_c|^0.51
    ├── exp2_birkhoff.py  sequential time-average convergence (beta sweep)
    └── fig1_gap2.py      two-panel verification figure
```

## Numerical verification

| Script | What it checks | Result |
|---|---|---|
| `exp1_drift_bv.py` | acim density depends Hölder-continuously on $u$ | $\|h_u - h_{u_c}\|_{L^1} \sim \|u-u_c\|^{0.51}$ (Hölder-½) |
| `exp2_birkhoff.py` | sequential time-average → autonomous target | converges; rate increases with $\beta$ |
| `fig1_gap2.py` | both, as a two-panel figure | `paper/figures/fig1_gap2_verification.png` |

These are sanity checks on the **mean** convergence; they do not verify
the almost-everywhere statement (which concerns a full-measure set of
initial conditions).

## Quick start

```bash
pip install numpy matplotlib
python experiments/exp2_birkhoff.py     # sequential Birkhoff convergence
python experiments/exp1_drift_bv.py     # density stability
python experiments/fig1_gap2.py         # regenerate Figure 1
```

## LaTeX build

```bash
cd paper
pdflatex main && bibtex main && pdflatex main && pdflatex main
```

## Citation

```bibtex
@misc{wang2026sequential,
  title     = {A Sequential Birkhoff Theorem for Slow Logarithmic Drift
               in Non-Uniformly Expanding Unimodal Maps},
  author    = {Wang, Liang},
  year      = {2026},
  version   = {v1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20711935},
  url       = {https://doi.org/10.5281/zenodo.20711935}
}
```

> Wang, Liang. (2026). *A Sequential Birkhoff Theorem for Slow
> Logarithmic Drift in Non-Uniformly Expanding Unimodal Maps* (v1.0).
> Zenodo. https://doi.org/10.5281/zenodo.20711935

## Related work

The motivating prime-dynamics paper is in [`../paper/`](../paper/);
its published predecessor is Wang, L. (2026), *The Emergence of Prime
Distribution from Low-Dimensional Deterministic Chaos*, Research in
Mathematics 13(1), [doi:10.1080/27684830.2026.2684334](https://doi.org/10.1080/27684830.2026.2684334).
