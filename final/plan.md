# CS/INFO 6850 Final Project — Proposal & Handoff

**Authors:** Arjun Saini, Aryavardhan Singh
**Working title:** *When Does Geographic Diversification Backfire? Intermediate Supplier Clustering in k-of-n Supply Networks*
**Status as of Nov 12, 2026:** direction chosen; exploratory paper done; roadmap due Nov 16.

This document hands work off to a Claude Code session that has the full exploratory paper, its code, and its experiment outputs. It explains **what we're doing for the final and why**, and **what to build next**. Where it cites a number from the exploratory paper, check it against the repo. Anything marked **[VERIFY]** has not been checked.

> **Repo note (added Nov 12):** paths here refer to the pre-reorganization layout. The exploratory paper and its code now live in `exploratory/`, and final-project material in `final/`. §4's single-firm check is not yet in the repo or in either paper; it was an informal check, so don't cite it as established until it is reproduced in code. Some course details in §1 (talk length, final due date) are superseded by the course's project description: talks are 4–6 minutes, the roadmap is about a page with a discussion of background work, and the final due date will be announced.

---

## 1. Course requirements and deadlines

| Item | Due | Notes |
|---|---|---|
| Roadmap document | **Mon Nov 16, 6pm** | About half a page. Doesn't need to repeat the exploratory paper; just how we turn it into the project. Draft in §9. |
| Lightning-talk slides | **Mon Nov 23, 6pm** | At most **2 PDF slides**, **3 minutes**. Must cover (a) the question, situated in prior work, and (b) a preview of **one** finding so far. |
| In-class lightning talks | Nov 30, Dec 2, or Dec 7 | Schedule announced later. |
| One-on-one check-in | Week of Nov 30 | **10 min**. Check-in on progress since the exploratory paper. |
| **Final write-up** | **Tue Dec 15, 2:30pm** | **About 10–15 pages**, any reasonable format (we use LaTeX). Must include **some mathematical analysis and some computation on real or synthetic data**. Genres: experimental evaluation, theoretical project, or critical survey. **Ours is a theoretical project with simulation validation.** |

## 2. Feedback and what it implies

Instructor feedback on the exploratory paper: **we were doing too many things; for the final, narrow to one result or aspect and go deep.** The overall impression was positive: the exploratory paper was ambitious and went well beyond what was expected.

What this means for the final:
- The exploratory paper already has three proved claims, a counterexample with a grid search, about 3,360 simulation runs matching theory, and the hub-region analysis. That already meets the "math + computation" bar. **The final doesn't need more breadth.**
- The final should answer **one question completely**: a sharp general statement, a proof or a clear characterization, an explanation of the mechanism, and simulations designed to break it.
- Existing results become **setup and supporting material**, not parallel headline results.
- **Drop or move to a short future-work paragraph:**
  - endogenous supplier choice / equilibrium (old §8)
  - the OECD / Thailand-floods empirical test (old §8). The country-industry aggregation would smooth out the jump we'd be testing for, and 2011 is confounded by the Japan earthquake.
  - hub regions / Q3
  - protecting firms on a budget (reverse influence maximization)
- Q1 (k ≥ 2 ⇒ abrupt collapse, Claim 1) stays as a short setup result.

## 3. The chosen question

**Exploratory finding (Example 1, Fig. 2c, Table 1).** With k = 1, splitting suppliers into more regional clusters never hurts (Claim 3, proved by Jensen's inequality). With k ≥ 2 this fails. For n = 4, k = 2, m = 1, x = 0.9, tolerable shock φ*:

| Geography | φ* (infinite depth) | φ* (20 layers) | Sim median [95% CI] |
|---|---|---|---|
| spread (c = 4) | 0.1946 | 0.2162 | 0.2162 [0.2157, 0.2170] |
| pairs (c = 2) | **0.1705** | **0.1946** | **0.1948** [0.1940, 0.1950] |
| co-located (c = 1) | 0.1946 | 0.2174 | 0.2167 [0.2162, 0.2175] |

The grid search over even n ≤ 8, m ≤ 3 and six x values found reversals in 72 of 109 k ≥ 2 settings with positive φ*, and in none with k = 1. Fig. 2c shows a similar reversal for (n, k) = (6, 3).

**Final-project question (reframed):** *When does geographic diversification of suppliers backfire, and why?* The final should lead with the mechanism and the conditions under which it holds, **not** with "pairs are worst."

**Practical hook:** the "pairs" geography is essentially **China+1 / dual-region sourcing**, a very common response to regional risk. If firms need capacity from more than one supplier (k ≥ 2), splitting across two regions can be worse than not splitting at all. Use this as motivation without overclaiming a direct mapping.

## 4. Is it an artifact? What we checked (Nov 11)

The concern was that the reversal might come from the tree or fixed-point setup rather than reflect anything real. We tested a **single firm with no cascade**: n suppliers in c equal clusters of size b = n/c, each region surviving independently with probability s = 1 − φ, each surviving supplier usable independently with probability p, and the input covered if at least k suppliers are usable:

```
C_c(s, p) = Σ_{j=0}^{c} Binom(j; c, s) · S_k(j·b, p)        where S_k(N, p) = Pr[Bin(N, p) ≥ k]
```

This matches the paper's coverage formulas with p = x·r (spread: S_k(n, s·p); co-located: s·S_k(n, p); pairs: s²S_k(4, p) + 2sφ·S_k(2, p)).

Results (grid: s ∈ [0.5, 0.99], p ∈ [0.3, 0.99]):
- n = 4, k = 2: pairs strictly below **both** extremes in **754 / 3500** grid points.
- Interior c is worst in a sizeable fraction of the grid for (n, k) = (6, 2), (6, 3), (8, 2), (8, 4), (12, 3) and (12, 6). Counts out of 1600: 283, 606, 83, 543, 222, 616.
- k = 1: **never**, as Claim 3 predicts.
- Where it happens for n = 4, k = 2:

  | s | p-window where pairs are worst |
  |---|---|
  | 0.6 | none |
  | 0.8 | ≈ (0.448, 0.666) |
  | 0.9 | ≈ (0.382, 0.666) |
  | 0.95 | ≈ (0.356, 0.666) |

  The upper edge, **2/3**, is exactly the root of the bracket 2p² − S₂(4, p) from Example 1. Check: S₂(4, 2/3) = 72/81 = 2·(2/3)².

**Takeaways:**
1. The reversal is a **single-firm phenomenon**. The cascade isn't creating it.
2. The network's role: **at the tipping point, the cascade drives effective supplier reliability p = x·r\* into the reversal window.** In the base case p ≈ 0.6 at threshold. The cascade turns a niche single-firm effect into the one that decides φ\*.
3. Mechanism: with k ≥ 2, coverage is S-shaped in the number of surviving suppliers. In the convex region, concentrated all-or-nothing risk beats diversified risk. Intermediate splits make the knife-edge "exactly k left, all must work" state likely. Co-location almost never reaches it, and full spreading rarely loses that many at once.

Script used (reproduce in the repo and extend):

```python
import numpy as np
from scipy.stats import binom
def S(k, N, p): return binom.sf(k-1, N, p)
def cov(c, s, p, k=2, n=4):
    b = n // c
    return sum(binom.pmf(j, c, s) * S(k, j*b, p) for j in range(c+1))
# pairs strictly worst iff cov(2,s,p) < min(cov(4,s,p), cov(1,s,p))
```

## 5. Planned results

### 5.1 Setup (short; reuse from exploratory paper)
- Model: EGL layered tree, m inputs, n suppliers per input, relationship strength x, **k-of-n coverage**, regional shocks φ, c clusters. Equation (2) and the definitions of r\*, ρ and φ\*.
- Claim 1 (km ≥ 2 ⇒ abrupt collapse): keep as a short proposition.
- Claim 2 (spread = shock acts like weakening x; m = 1 extremes tie; m inputs ⇒ co-location worse): keep, and **don't headline the exact tie**. It's a property of the recursion.
- Claim 3 (k = 1 ⇒ finer splits never hurt): keep. **Extend it to any refinement**, not just splits where c divides c′, if possible. If not, say so.

### 5.2 Lemma A — single-firm reversal window (the core new math)
Characterize when C_c(s, p) < min(C_1(s, p), C_n(s, p)) for intermediate c.
- Closed form for n = 4, k = 2 (pairs): both boundaries of the window in (s, p). The upper edge p = 2/3 against co-location comes from the bracket. Derive the lower edge, which comes from the pairs-vs-spread comparison.
- General (n, k, c): find the cutoff p̂(n, k, c) that generalizes 2/3. Conjecture: a sign condition on Σ_j [Binom(j; c, s) − (co-located weights)]·S_k(jb, p). Prove what's tractable and characterize the rest numerically. **[VERIFY: whether a clean general closed form exists]**
- Interpretation: it's a convexity argument, the k ≥ 2 counterpart of Claim 3's Jensen step. With k = 1 the per-cluster failure term is convex, so finer splits help. With k ≥ 2 the S-shape flips convexity for small p.

### 5.3 Theorem B — single-firm reversal ⇒ network reversal (proposed proof route) **[VERIFY]**
Comparing **largest fixed points** may reduce to a single-point comparison:
- Let F_A and F_B be continuous and increasing on [0, 1] with F(1) ≤ 1. Let r_A\* be the largest fixed point of F_A. If F_B(r_A\*) ≥ r_A\*, then F_B has a fixed point in [r_A\*, 1] by the intermediate value theorem on F_B(r) − r, so r_B\* ≥ r_A\*.
- So to show φ\*_pairs < φ\*_X, it may suffice to show that **at φ = φ\*_pairs, F_X(r_P) > F_P(r_P) = r_P**, where r_P is the pairs network's tangency point. Then show X stays positive slightly past φ\*_pairs, using continuity in φ and the strict inequality.
- With m inputs, F = (coverage)^m, so the ordering of coverage carries over.
- So the **network reversal holds whenever the single-firm reversal holds at p = x·r_P and s = 1 − φ\*_pairs**. Theorem B then reduces to "the pairs tipping point lands inside Lemma A's window." Check this numerically across the 109-setting grid and prove it for the base case.
- **Base-case check (Nov 12; n = 4, k = 2, m = 1, x = 0.9):** a direct fixed-point solve reproduces φ\* = 0.1946 / 0.1705 / 0.1946 (spread / pairs / co-located). At the pairs tipping point, r_P = 0.678, so p = x·r_P = 0.610, which is inside the s ≈ 0.83 window. There F_pairs(r_P) = 0.678, F_spread(r_P) = 0.696 and F_coloc(r_P) = 0.690, so both extremes are strictly above r_P, as the reduction requires. The proof route works for the base case; the general case still needs proof.
- Also explain the 72/109 split: settings without a reversal should be those where (s, x·r_P) at the tipping point falls outside the window.

### 5.4 Large-n limit (optional; include if it comes out cleanly)
With many suppliers per cluster (b → ∞, k/b fixed), the number of usable suppliers in a surviving cluster concentrates at b·p. Coverage then becomes **Pr[Bin(c, s) ≥ ⌈k/(b·p)⌉]**, a purely combinatorial "how many clusters must survive" problem. This should give closed-form tipping points and make the non-monotonicity in c obvious. It also answers whether the effect disappears or persists as redundancy grows.

### 5.5 Robustness simulations (designed to kill the effect)
Each check either confirms the result is robust or identifies what it depends on. Both outcomes are worth reporting. Reuse the existing simulator (20,000 firms/layer, 20 layers, bisection on tipping point, bootstrap CIs).

| # | Relaxation | What it tests |
|---|---|---|
| R1 | **Capacity-weighted coverage**: suppliers have random capacities, input covered if surviving capacity ≥ θ | Whether the hard k threshold is doing the work |
| R2 | **Partial regional damage**: a hit region knocks out each firm with probability δ < 1 | Whether the all-or-nothing shock is doing the work |
| R3 | **Unequal cluster sizes** (e.g. 3+1 vs 2+2) | Whether "balanced intermediate" is special |
| R4 | **Mixed geographies across firms**: fraction of firms using each c | Whether it survives firm heterogeneity |
| R5 | **Graphs with cycles**: directed configuration-model network, heavy-tailed supplier popularity | Whether the tree assumption is doing the work |
| R6 | **Spatially correlated shocks**: adjacent regions hit together | Whether region independence is doing the work |

Priority: R1, R2, R5 first. R3 and R4 are cheap. R6 only if time allows.

## 6. Prior work to position against

Already in the exploratory paper: EGL 2022 (base model), CNST 2021 (empirics), DGM 2006 (k-core), Ang–Iancu–Swinney 2017, Bimpikis–Fearing–Tahbaz-Salehi 2018 (S-shaped production makes multisourcing hurt; the closest mechanism), Papachristou–Rahimian–Azadegan (percolation, recommends geographic diversification with k = 1), Centola–Macy, Granovetter, Easley–Kleinberg, KKT 2003, Kleinberg 2007.

**To add. Non-monotone or harmful diversification in other networks. [VERIFY all citations before use]**
- Acemoglu, Ozdaglar, Tahbaz-Salehi (2015), "Systemic Risk and Stability in Financial Networks," *AER*. Dense connectivity helps against small shocks and hurts against large ones.
- Battiston, Delli Gatti, Gallegati, Greenwald, Stiglitz (2012), "Liaisons dangereuses: Increasing connectivity, risk sharing, and systemic risk," *JEDC*.
- Wagner (2010), "Diversification at financial institutions and systemic crises," *J. Financial Intermediation*. Diversification makes failures coincide.
- Reliability engineering: k-out-of-n systems with **common-cause failures** and redundancy allocation. Find one or two standard references.
- Optional: Ibragimov, Jaffee, Walden on "diversification disasters" under heavy tails.

**Positioning:** the principle that diversification can hurt under convex or threshold payoffs is known in these fields. Our contribution is (i) an explicit supply-network geography version, (ii) the single-firm window plus the network reduction (Lemma A + Theorem B), and (iii) showing that the cascade pushes the network into the window right at its tipping point.

## 7. Paper outline (about 12–14 pages)

| § | Section | Pages | Source |
|---|---|---|---|
| 1 | Introduction: China+1 hook, question, contributions | 1.5 | new |
| 2 | Related work: EGL / CNST / DGM condensed, plus diversification-backfire literature | 1.5–2 | condensed from exploratory §2–5 + new |
| 3 | Model + Claims 1–3 (short; Claim 3 extended) | 2 | exploratory §6 |
| 4 | **Lemma A: single-firm reversal window** (+ figure: window in (s, p) plane) | 2–2.5 | new |
| 5 | **Theorem B: network reversal at the tipping point** (+ explanation of 72/109) | 2 | new |
| 6 | Large-n limit (optional) | 1 | new |
| 7 | Simulations: validation + R1–R6 robustness | 2–2.5 | exploratory §7 + new |
| 8 | Discussion: when it applies (near the cliff, link to EGL equilibrium), limitations, future work (endogenous choice, data) | 1 | new |

Main figures:
1. Reversal window in the (s, p) plane, with the tipping-point trajectory overlaid. **This is the key figure.**
2. φ\* vs c (existing Fig. 2c, extended).
3. Robustness panel.

## 8. Timeline

| Dates | Work |
|---|---|
| Nov 12–16 | Submit roadmap (§9). Reproduce the single-firm check in the repo. Compute the window boundaries for n = 4, k = 2. |
| Nov 16–23 | Lemma A for n = 4, k = 2 in closed form. Verify Theorem B's reduction numerically on the 109-setting grid. **Make the 2 slides** (key figure + one-sentence finding). |
| Nov 23–Dec 4 | General (n, k, c) for Lemma A. Write up Theorem B. Robustness R1, R2, R5. Prepare for the 10-min check-in. |
| Dec 4–11 | R3, R4 (R6 if time). Optional large-n section. Full draft. |
| Dec 11–15 | Revise, check every number against code output, submit by **Dec 15, 2:30pm**. |

## 9. Draft roadmap text (for Nov 16; about half a page)

> **Roadmap: When Does Geographic Diversification Backfire?**
> *Arjun Saini, Aryavardhan Singh*
>
> Our exploratory paper extended the Elliott–Golub–Leduc supply-network model with k-of-n sourcing (an input needs at least k working suppliers) and regional shocks. It studied several questions. For the final project we will focus on one: **when does spreading a firm's suppliers across regions make the network more fragile?** In the exploratory paper we proved that when one supplier suffices (k = 1), finer geographic spreading never hurts. When firms need two (k = 2), we found numerically that splitting suppliers into two regional pairs, a "China+1"-style strategy, can collapse at a smaller regional shock than either keeping all suppliers together or spreading them fully.
>
> Since then we have checked that this reversal is not an artifact of the network recursion: it already appears for a single firm whenever each supplier is usable with probability in a middle window (for 4 suppliers needing 2, up to p = 2/3). The network matters because the cascade pushes supplier reliability into that window right at the tipping point. We plan to (1) characterize the single-firm reversal window in closed form, generalizing the k = 1 convexity argument; (2) prove that a single-firm reversal at the tipping point implies a reversal in the network's tolerable shock, and use this to explain which parameter settings in our grid show reversals; and (3) test robustness in simulation by relaxing our main assumptions: capacity-weighted rather than hard k-of-n coverage, partial regional damage, and networks with cycles and heavy-tailed degrees. We will connect the result to related findings that diversification can increase systemic risk in financial networks and with S-shaped production. Endogenous sourcing choices and an empirical test are left as future work.

## 10. Guardrails for the implementing session

- **Don't headline the m = 1 exact tie** between spread and co-located. It's a property of the recursion.
- **Be honest about scope:** the reversal only matters near the tipping point, and the gap in the base case is modest (about 12% in φ\*). Far from threshold, pairs beat co-location. State that relevance depends on networks operating near the cliff, which EGL's equilibrium result supports.
- Every reported number must come from code output in the repo. Recompute rather than copy from this document.
- Check every citation marked [VERIFY] before it goes into the paper.
- Keep the AI-use acknowledgment, as in the exploratory paper.
- Scope discipline: anything that isn't Lemma A, Theorem B, the large-n limit, or R1–R6 goes in a future-work sentence.

## 11. First tasks for the implementing session

1. Locate the coverage and fixed-point code from the exploratory paper. Add `cov(c, s, p, k, n)` (single-firm) and confirm it matches the paper's coverage formulas at p = x·r.
2. Reproduce the §4 grid counts and the n = 4, k = 2 window table.
3. For each of the 109 grid settings with k ≥ 2: compute the pairs/intermediate tipping point (φ\*, r_P), check whether (1 − φ\*, x·r_P) lies in the single-firm window, and compare with whether the network reversal occurred. This is the empirical test of Theorem B's reduction.
4. Produce the key figure: reversal window in (s, p), with the network's (s, x·r\*) path as φ increases, for each geography.
5. Derive the lower window boundary for n = 4, k = 2 symbolically (sympy).
