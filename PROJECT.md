# Prime Dynamics Follow-up — Project Layout

Follow-up to *Liang Wang, "The Emergence of Prime Distribution from Low-Dimensional Deterministic Chaos"* (Final_Paper.pdf), targeting **Hypothesis 3.3 (Topological Admissibility Condition)**.

Working thesis (per `readme.md`):

1. **Microscopic falsification.** The paper's sieve sequence $Q_k$ violates the MSS maximal condition at finite $k$ (e.g. $Q_3$ fails at $n=31$, $Q_5$ at the 113–127 gap) — Legendre's conjecture cannot rescue it.
2. **Macroscopic restoration.** Defect density $\rho(N) \to 0$ as $N \to \infty$ via "arithmetic transient chaos" + "topological shield" (long initial composite runs). Asymptotic admissibility replaces absolute admissibility, no number-theoretic conjecture required.
3. **Markov ceiling.** The 1D unimodal map's invariant measure on a 3-interval Markov partition forces $\mu_{2m+2} = p \cdot \mu_{2m}$ — geometric decay only, no mod-3 resonance. This explains why the 1D model captures $C_2$ but cannot produce the Hardy–Littlewood spike at gap 6.
4. **Langlands-style framing.** 1D unimodal map = abelian/mod-2 projection of the prime universe; capturing higher-order resonances requires multi-modal / non-autonomous lifts.

## Layout

```
prime_math/
├── Final_Paper.pdf          # original paper under critique
├── readme.md                # the strategic plan / discussion log
├── PROJECT.md               # this file
├── prime_logistic/          # original author's reproduction code (read-only reference)
├── prime1..7.ipynb          # exploratory notebooks (Gemini discussion)
│
├── src/                     # reusable Python modules
│   ├── mss.py               # MSS parity-lex comparison + defect counting
│   ├── sieve.py             # Q_k sieve sequence per paper definition S_p = R L^{p-1}
│   ├── logistic.py          # 1D logistic-map orbits and symbolic encoding
│   └── gap_spectrum.py      # gap histograms + Markov geometric-decay test
│
├── experiments/             # runnable experiment scripts → results/
│   ├── exp1_defect_density.py     # Section 3: rho(N) decay table
│   ├── exp2_logistic_gaps.py      # Section 4: mu_4/mu_2, mu_6/mu_2 from logistic orbit
│   └── exp3_real_prime_gaps.py    # Section 4: Hardy–Littlewood reference spectrum
│
├── figures/                 # publication-ready plots
│   ├── fig1_microscopic_breakdown.png
│   ├── fig2_defect_density.png
│   └── fig3_geometric_vs_HL.png
│
├── results/                 # raw outputs (.csv, .json) from experiments
└── paper/                   # LaTeX manuscript
    ├── main.tex
    └── refs.bib
```

## Quick start

```bash
pip install numpy matplotlib sympy scipy
python experiments/exp1_defect_density.py
python experiments/exp2_logistic_gaps.py
python experiments/exp3_real_prime_gaps.py
```
