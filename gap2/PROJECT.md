# Gap 2 — Non-Autonomous Birkhoff for Slow Logarithmic Drift

Standalone follow-up project. Goal: rigorize the non-autonomous Birkhoff
statement that the prime-dynamics paper (ETDS-2026-0159 / Nonlinearity
submission) leaves as Remark 4 ("a non-autonomous Birkhoff theorem for
slowly-varying parameter cocycles is expected to hold").

## The theorem we want

Let $u_c$ be a Misiurewicz parameter of $f_u(x) = 1 - ux^2$, and let
$(u_n)$ be a sequence with $u_n \to u_c$ and slow drift
$|u_n - u_c| \le c\,(\log n)^{-\beta}$, $\beta > 0$. Define the
sequential composition (cocycle)
$$\Phi_N = f_{u_N} \circ f_{u_{N-1}} \circ \cdots \circ f_{u_1}.$$
Then for Lebesgue-a.e. $x_0$ and every $\varphi \in \mathrm{BV}[-1,1]$,
$$\frac{1}{N}\sum_{n=1}^{N} \varphi(\Phi_n(x_0))
   \;\xrightarrow[N\to\infty]{}\; \int \varphi \, d\mu_{u_c},$$
where $\mu_{u_c}$ is the unique acim of the autonomous map $f_{u_c}$.

## Why this is a clean, publishable, standalone paper

- **No prime numbers**: pure ergodic theory / one-dimensional dynamics.
  Scope is unambiguous; minimal desk-reject risk.
- **Self-contained**: does not cite or depend on the prime-dynamics
  paper's results. (The prime paper will cite *this* once it exists.)
- **Tools are mature**: Keller–Liverani perturbation + Lasota–Yorke +
  the induced-map machinery. This is assembly, not invention.
- **Strengthens the main paper**: once proved, the prime paper's
  Remark 4 upgrades from "expected" to "holds by [this paper]".

## Three work modules

### Module 1 — Spectral perturbation (the engine)
Keller–Liverani (1999) stability of the spectral gap under small
perturbations of the transfer operator, applied on the BV space of the
*induced* first-return map $F$ to the L-cylinder (the critical-point
degeneracy at x=0 forbids working on the raw map). As $u_n \to u_c$:
- leading eigenvalue stays at 1,
- spectral gap persists (uniformly for $u$ near $u_c$),
- acim density $h_{u_n} \to h_{u_c}$ in the KL norm.

### Module 2 — Drift-error accumulation
$\sum_n |u_n - u_c| = \sum_n c(\log n)^{-\beta}$ diverges, but under
Cesàro averaging the error is controlled by the exponential decay of
correlations from the spectral gap. Establish that the time-average
error term $\to 0$. Determine the critical $\beta$ (likely any
$\beta > 0$ suffices, to be checked).

### Module 3 — Non-autonomous Birkhoff
Telescope the cocycle orbit against the autonomous orbit; autonomous
part by classical Birkhoff, the drift correction by Module 1+2.

## Key technical risk

The map is **non-uniformly hyperbolic** (derivative 0 at x=0), so
Keller–Liverani must be applied on the induced first-return map
(uniformly expanding, Lemma 3 of the prime paper), then transferred
back via the tower. Getting the perturbation theory to commute with
the inducing is the main technical content.

## Target journals

ETDS / Nonlinearity / JNS / DCDS-A / Discrete Contin. Dyn. Syst.

## Layout

```
gap2/
├── PROJECT.md            this file
├── paper/
│   ├── main.tex          12-18 page paper
│   └── refs.bib
└── experiments/
    ├── exp1_drift_bv.py      numerical: BV-norm convergence h_{u_n} -> h_{u_c}
    └── exp2_birkhoff.py      numerical: time-average convergence under drift
```
