# AUTO_REVIEW.md — auto-review-loop log

Project: Transient Chaos and Topological Bounds in Prime Dynamics
Target venue: JNS or DCDS-A (1区Top pure-math)
Mode: review-only

## Round 1 (2026-05-29)

**Reviewer**: Opus 4.7 (self-review fallback; Codex MCP sandbox refused
file access, no `LLM_API_KEY` for `auto-review-loop-llm` → external
reviewer paths exhausted, used in-process review per skill's fallback
guidance)

### Assessment summary

- **Score**: 6.5 / 10
- **Verdict**: ALMOST READY (with non-trivial revisions)
- **Key criticisms**:
  1. Lemma 5 (geometric convergence of α_n) has a gap: spectral gap
     of the transfer operator gives geometric *correlation* decay, but
     the conversion to convergence of `q_n / Q_{n-1}` isn't airtight.
  2. Lemma 3 invokes "hyperbolic along the critical orbit" with a
     vague de Melo–van Strien §V citation; needs a specific theorem.
  3. Theorem 3 proof's last step ("divergence of Σ 1/(log n_i)^2 follows
     from Lemma 7") elides a positive-density argument.
  4. Conjecture 2 (arithmetic shadowing) is not made precise enough
     for a reviewer to judge whether it's plausible or vacuous.
  5. Section 1.1 (AI-for-math) feels grafted on; doesn't cohere with
     the rest of the paper.
  6. Several arXiv IDs in refs.bib are unverified due to API rate-limit
     during compilation (Task #39).

### Reviewer raw response

<details>
<summary>Click to expand full reviewer response</summary>

# Referee report — JNS / DCDS-A submission

## 1. Summary

The paper revisits the unimodal-symbolic model of the prime
distribution proposed by Wang (2026), establishes that its central
"topological admissibility" hypothesis is false at finite stages
(Q_3, Q_5), and rebuilds the model on three pillars:

- **Theorem A (Parity-Gap Lemma)**: a defective shift in W_k forces a
  prime gap of length ≥ p_{k+1}-1 starting at a prime m+1. This
  reduces topological admissibility to an extremal prime-gap problem.
- **Theorem B (Even-gap rigidity)**: at u_c, all odd gaps carry zero
  invariant measure, via a clean parity-twisted lex argument on the
  kneading sequence RLR^∞.
- **Theorem C (Asymptotic geometric decay)**: μ_{2m+2}/μ_{2m} → p_∞
  with exponential remainder, via three spectral bridging lemmas
  (induced first-return uniformly expanding, BV spectral gap,
  geometric convergence of α_n).

The paper closes with a clearly conditional reduction (Section 8) of
"infinite L-R-L recurrence" to an arithmetic shadowing conjecture.

## 2. Strengths

- The Parity-Gap Lemma is genuinely new and the proof is clean. The
  case analysis on positions 0, 1, j ∈ [2, p_{k+1}-1] is correct,
  and the conclusion that defective shifts force prime gaps ≥
  p_{k+1}-1 is sharp (matched by the only two known defects at k=3, 5).
- The choice to *demote* twin-prime infinitude to a clearly
  conditional Corollary 3 — and explicitly say so in Remark 5 —
  reads as mature, not over-claiming.
- The numerical evidence is impressive in scope (k ≤ 5000, horizons
  up to 2.36 × 10^9), and the paper correctly does not rely on it
  for any theorem statement.
- The "phenomenological calibration" reframing of Wang's C_2
  recovery (Section 5.5) is sharp and fair.
- Related Work section is genuinely informative: positioning vs
  Cramér / Hardy-Littlewood / Granville-Soundararajan / Cellarosi-Sinai
  is something a JNS referee will appreciate.

## 3. Critical weaknesses (ranked by severity)

### 3.1 Lemma 5 (Geometric convergence of α_n) — GAP IN PROOF

[spectral_lemmas.tex:134-169]

The proof states:
> "Lemma 4 applied to the indicator function 1_{A_n} yields
> q_n − μ_A(A_n)·1 = O(θ^n)"

This is the heart of the argument and it's not quite right as stated.
The spectral gap on BV (Lemma 4) gives, for any φ ∈ BV with mean zero,

  ||L^N φ||_{BV} ≤ C θ^N ||φ||_{BV}.

This is a statement about the iterates L_F^N applied to a *fixed*
φ. To conclude convergence of `q_n` (which is the mass of the *cylinder*
A_n, not the iterate of a fixed function), you need an additional
step: either (a) interpret q_n as ∫ 1_{A_n} h_A dm and bound it
directly via the spectral data of L_F (which gives only the rate at
which iterates of an INITIAL density approach the equilibrium density,
not the rate at which different cylinder masses concentrate), or (b)
identify q_n with a Markov-renewal-type quantity and apply a
geometric-tail argument *separately*.

The two are not the same and conflating them is the most common
mistake in this kind of proof. **At minimum, the proof needs a
Markov-renewal lemma stating that for piecewise expanding F,
P(τ_A = 2n) = q_n decays geometrically in n; this is a *separate*
fact from the BV spectral gap.** The standard reference is
Sarig 2002 (Bull. LMS) or Aaronson's book on infinite ergodic theory.

**Minimum fix**: insert a half-page step deriving
`q_n = O(θ^n)` from the Markov structure and the L^∞ bound on h_A,
*using* Lemma 4 but not pretending Lemma 4 directly gives it.
Alternatively: state Lemma 5 as a hypothesis explicitly drawn from
Sarig/Aaronson and weaken Theorem C accordingly.

### 3.2 Lemma 3 (Induced first-return uniformly expanding) — VAGUE CITATION

[spectral_lemmas.tex:42-58]

The proof claims:
> "the Misiurewicz parameter u_c is hyperbolic along the critical
> orbit in the sense of [demelo1993one, §V]"

§V of de Melo–van Strien is 60+ pages. A precise theorem reference
(probably §V.5 or Theorem V.6.1 there) is needed. Moreover the
implication actually used is stronger than mere "hyperbolic along
critical orbit"; it's "the iterate f_{u_c}^N has expanding derivative
on the union of cylinders that miss a fixed neighborhood of the
critical point." This is a *consequence* of Misiurewicz hyperbolicity
combined with the stratification of the chaotic band, not a single
theorem.

**Minimum fix**: cite a specific theorem (perhaps Misiurewicz 1981
Theorem 1 or a specific result from Mañé's "Hyperbolicity, sinks
and measure in one-dimensional dynamics" CMP 1985), and state the
implication being used as a sub-lemma.

### 3.3 Theorem 3 (Twin cylinder recurrence) — POSITIVE-DENSITY GAP

[main.tex:929-949]

The proof says:
> "the visit set N(x_0) has positive lower density, hence is
> infinite, and divergence of Σ_{n ∈ N} 1/(log n)^2 follows from
> Lemma 7."

This is too quick. Lemma 7 says ∫ μ(I_LRL)/(log t)^2 dt diverges.
That's an integral over t, not a sum over the visit times n_i ∈ N.
The implication `positive density of n_i + integral diverges →
sum over visit times diverges` requires an Abel-summation or
upper-density step. Specifically, if N has positive lower density
δ > 0, then Σ_{n ∈ N, n ≤ T} 1/(log n)^2 ≥ δ T / (log T)^2 (asymptotically),
which → ∞ since T/(log T)^2 → ∞. Fine, but **this two-line argument
should be in the proof.** A referee will pause at this jump.

**Minimum fix**: insert the explicit lower-bound calculation:
"By Birkhoff, |N ∩ [0, T]| ≥ (μ(I_LRL) - ε)T for T large, and
Σ_{n ∈ N ∩ [0,T]} (log n)^{-2} ≥ (μ(I_LRL) - ε) · T (log T)^{-2},
which → ∞."

### 3.4 Conjecture 2 (Arithmetic shadowing for twin primes) — UNDER-SPECIFIED

[main.tex:968-975]

Conjecture 2 asserts:
> "There exists a positive density of horizons N such that, for any
> orbit of f_{u_c} that visits I_{LRL} at symbolic time n ≤ N, the
> arithmetic position of the visit corresponds (under the
> non-autonomous embedding n ↦ p_n) to a true twin-prime pair (p, p+2)
> with p ≤ N log N."

The phrase "positive density of horizons N" is unclear. Density in
what variable? Lower vs upper density? Density with respect to which
measure? Also, **the conjecture as stated has no quantitative content
that distinguishes it from "twin primes are infinite"**: the
embedding n ↦ p_n is not specified; the orbit dependence is unclear;
and "positive density of horizons N" combined with "any orbit visiting
I_LRL at time n ≤ N" is logically strange (the visiting set already
has positive density, so the conjecture appears to say "for some N,
the embedding maps such visits to twin primes," which is either trivial
or a restatement of the twin-prime conjecture).

**Minimum fix**: rewrite Conjecture 2 as a precise statement with
no ambiguity. For example:
"There exists an arithmetic embedding π: N → primes (e.g.
n ↦ p_n) such that for any μ-typical orbit x_0 of f_{u_c}, the
density of n ∈ N(x_0) for which (π(n), π(n)+2) is a twin-prime pair
is positive."
This at least has a clear formal content; whether it's still
*plausible* under arithmetic shadowing is a separate matter that
should be justified with a one-paragraph heuristic.

A JNS referee skeptical of "twin prime adjacent" claims will read
Conjecture 2 carefully. The current statement does not survive
careful reading.

### 3.5 Section 1.1 (AI-for-math) — TONALLY UNCLEAR

[main.tex:63-119]

The new Section 1.1 introduces "AI-assisted numerical-heuristic
discovery" as a methodological frame, citing FunSearch, Davies et al.,
AlphaGeometry, Tao's Lean lectures, etc. For JNS / DCDS-A, this
framing has two issues:

1. The paper's actual content does *not* involve any LLM, FunSearch-
   style program search, or Lean formalization. The numerical
   experiments are standard Python/numba code. A pure-math reviewer
   will find the framing distracting at best, possibly aggrandizing.
2. The list of references is name-dropping rather than substantive:
   FunSearch is for cap-sets, AlphaGeometry for olympiad geometry,
   Tao+Lean for formalization — none of these methodologies is used
   in this paper. The honest connection is just: "we used computers
   to find the bug (Q_3, Q_5) before proving the theorem." That's
   not new and doesn't need a survey paragraph.

**Minimum fix**: either (a) drop Section 1.1 entirely and let
"large-scale numerical experiments" appear as a tool in the
contributions list, or (b) demote it to one short paragraph at the
end of §1.2 acknowledging the methodological lineage without
claiming participation in it.

### 3.6 Theorem 1 (Eventual admissibility, conditional)

[main.tex:493-511]

The theorem is correct but the conditioning is subtle:
**any β > 0 with G(N) ≤ C(log N)^β suffices**. This is implicitly
stronger than "Cramér's conjecture O((log N)^2)" and the proof
doesn't use the full strength of β = 2. The remark elsewhere
(Remark 1, [main.tex:472-491]) correctly notes that BHP / RH /
Andrica / Legendre are insufficient. The combination is logically
fine but a referee might ask: is there *any* unconditional bound
(by Erdős, Maier, Pintz, Granville–Soundararajan, etc.) that gives
G(N) ≤ (log N)^{O(1)}? The answer is no, but the paper should say
so explicitly so the conditioning isn't seen as a sleight of hand.

**Minimum fix**: one sentence after Remark 1:
"To our knowledge no unconditional bound of the form
G(N) ≤ (log N)^{O(1)} is known; the strongest unconditional result
remains G(N) = O(N^{0.525}) (Baker–Harman–Pintz)."

### 3.7 Section 8 conclusion

[main.tex:1010-1024]

Remark 6 is good ("should not be read as resolving any classical
conjecture"). But the framing of Section 8 still calls Conjecture 2
"arithmetic shadowing for twin primes" in its label. After the
stealth-rename of the section title, this internal label still
broadcasts the agenda. Consider renaming the conjecture too, e.g.
"Conjecture (Arithmetic shadowing for L-R-L cylinder)".

**Minimum fix**: rename `\label{conj:arith-shadow-twin}` → e.g.
`\label{conj:arith-shadow-LRL}` and adjust the conjecture's title
to match Section 8's framing.

### 3.8 Numerical-experimental claims in main text

[main.tex:725-783, Section 5.6]

Section 5.6 is a "Numerical evidence" subsection sandwiched between
the Markov decay theorem and Related Work. Its three paragraphs
(even-gap rigidity, twin density, joint constellations) reference
appendix data. For a pure-math journal, having a "Numerical evidence"
*subsection* in the middle of the body is unusual; reviewers may
prefer all numerics in the appendix and only a one-paragraph forward
reference in the body.

**Minimum fix**: move Section 5.6 to the start of Appendix A, leaving
a single sentence in §5.5 saying "All numerical claims are verified
in Appendix A; we summarise them there."

### 3.9 Citations

`refs.bib` contains 8 AI-for-math citations added in the latest
revision (FunSearch, Davies, AlphaGeometry, He review, etc.) that
were not arXiv-API-verified during the writing process. A few
journal/page numbers may be off. Specifically:
- `aidriven2024review`: He, Yang-Hui, NRP 6, 546-553. The pages
  field is filed as "546-553" but I have lower confidence in the
  exact page numbers without DOI verification.
- `mathmachsurvey2024`: filed as arXiv:2412.16543 with placeholder
  authors. The first author is correct; the rest are unverified.

**Minimum fix**: verify arXiv IDs, DOIs, and author lists before
submission via DBLP/CrossRef. Already tracked as Task #39.

### 3.10 Title and abstract

[main.tex:20-21, abstract:28-58]

Title: "Transient Chaos and Topological Bounds in Prime Dynamics:
Revisiting the One-Dimensional Sieve Mapping"

For JNS / DCDS-A, the title is fine but slightly informal
("Revisiting"). The abstract opens with "A recent line of work models
the prime distribution..." — this signals immediately that the paper
is responding to Wang 2026. After the latest reframing (paper as
independent contribution to AI-numerical-heuristic methodology),
this opening is in tension with §1.1.

**Minimum fix**: either change the abstract opening to
"We study the unimodal-symbolic model of the prime distribution
proposed in [Wang 2026]..." or accept that the paper IS a careful
analysis of Wang 2026 and tone down §1.1 (see 3.5).

## 4. Verdict

**ALMOST** ready for JNS / DCDS-A. The mathematical core (Theorem A,
Theorem B, Theorem C with spectral lemmas) is sound, but Lemma 5 has
a real gap (3.1) that a careful referee will catch, and Section 8's
Conjecture 2 (3.4) needs a precise restatement.

If 3.1 (Lemma 5 gap), 3.3 (Theorem 3 step), 3.4 (Conjecture 2
restatement), and 3.5 (Section 1.1 framing) are addressed, the
paper would deserve careful refereeing rather than desk rejection,
and has a fair chance of acceptance after one round of revisions.

A score of 6.5 reflects: the paper has multiple genuinely original
results (Parity-Gap Lemma, parity rigidity, Markov decay) supported
by serious numerics, but the rigor in the spectral chain (Lemmas 3-5)
and in Section 8 is not yet airtight enough for the top-tier pure-
math venues you're targeting.

</details>

### Action items (ranked by severity)

1. **Fix Lemma 5 proof gap** (3.1): insert Markov-renewal step
   deriving q_n = O(θ^n) separately from the BV spectral gap.
   Cite Sarig 2002 or Aaronson.
2. **Tighten Lemma 3 citation** (3.2): replace `[demelo1993one, §V]`
   with a specific Misiurewicz/Mañé theorem.
3. **Fill Theorem 3 last step** (3.3): explicit lower-bound
   Σ_{n ≤ T} 1/(log n)^2 ≥ δ T/(log T)^2 → ∞.
4. **Restate Conjecture 2 precisely** (3.4): specify the
   embedding π and density notion.
5. **Demote / rewrite Section 1.1** (3.5): remove name-dropping;
   keep only the honest "computers found the bug, then we proved
   the theorem" framing.
6. **Add unconditional-bound disclaimer to Remark 1** (3.6).
7. **Rename conj:arith-shadow-twin → conj:arith-shadow-LRL** (3.7).
8. **Move §5.6 to Appendix A intro** (3.8).
9. **Verify arXiv IDs** (3.9, Task #39).
10. **Reconcile abstract opening with §1.1 framing** (3.10).

### Status

Round 1 complete. Review-only mode: no fixes implemented. Stopping
loop after round 1 per user request (1-2 rounds maximum).

## Final Method Description

The paper's mathematical pipeline:

1. **Microscopic counter-examples** to Hypothesis 3.3 of Wang (2026):
   parity-twisted lex comparison shows Q_3, Q_5 are not MSS-admissible
   inside their physical horizon (sections 2.2, 2.3).

2. **Theorem A (Parity-Gap Lemma)**: any defective shift forces a
   prime gap ≥ p_{k+1} - 1 at a prime m+1 (section 3). Combined
   with Cramér-strength gap bounds, yields conditional eventual
   admissibility (Theorem 1).

3. **Theorem B (Even-gap rigidity)**: at the band-merging u_c, all
   odd gaps have zero invariant measure (markov_proof.tex Lemma 2 +
   Proposition 1).

4. **Theorem C (Asymptotic geometric decay)**: via the parity-split
   chain {A, B_o, B_e} and a spectral analysis of the first-return
   transfer operator (spectral_lemmas.tex Lemmas 3-5), the gap
   measure obeys μ_{2m+2}/μ_{2m} → p_∞ ≈ 0.596 with exponential
   remainder.

5. **Section 8 conditional pathway**: Birkhoff applied to the
   positive-mass cylinder I_LRL gives infinite recurrence; under an
   "arithmetic shadowing" conjecture (Conjecture 2), this lifts to
   infinite recurrence of integer L-R-L constellations.

6. **Appendix A**: numerical verification at k ≤ 5000, 5e8 logistic
   iterations, 8 separate experiment scripts.
