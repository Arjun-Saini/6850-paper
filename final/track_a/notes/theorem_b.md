# Theorem B: single-firm reversal at the tipping point ⇒ network reversal (A4)

Numbers here come from `code/theorem_b_base_case.py` → `results/theorem_b_base_case.json`, and `tests/test_theorem_b.py` checks them. The 109-setting test (explaining 72/109) is Track B's B2; this write-up will cite its output once it lands.

**Result.** Let r_P > 0 be the pairs network's reliability at its own tipping point φ\*_P. If another geography X gives a single firm strictly more coverage than pairs at (s, p) = (1 − φ\*_P, x·r_P), then φ\*_X > φ\*_P, for any number of inputs m. For n = 4, k = 2 this means the network reversal holds whenever the pairs tipping point lands in Lemma A's window. It does in the base case: p = 0.611 lies in (0.426, 2/3) at s = 0.829.

## Setting

For a geography c, the recursion is F_c(r; φ) = C_c(1 − φ, x·r)^m on [0, 1], where C_c(s, p) is the single-firm coverage. C_c is a polynomial in (s, p), so F_c is continuous in (r, φ), and 0 ≤ F_c ≤ 1. Coverage is non-decreasing in p and in s: couple the draws, and a surviving region or usable supplier stays one when s or p rises. Let r\*_c(φ) be the largest fixed point of F_c(·; φ), and φ\*_c = sup{φ : r\*_c(φ) > 0}.

## Steps

**Lemma 1 (comparison).** Let G be continuous on [0, 1] with G ≤ 1. If G(a) ≥ a for some a in [0, 1], then G has a fixed point in [a, 1], so its largest fixed point is ≥ a.

*Proof.* h(r) = G(r) − r is continuous with h(a) ≥ 0 and h(1) ≤ 0. The intermediate value theorem gives a root in [a, 1]. ∎

**Lemma 2 (the tangency point is a fixed point).** r\*_c(φ) is non-increasing in φ. Let L = lim_{φ↑φ\*_c} r\*_c(φ). Then L is a fixed point of F_c(·; φ\*_c), and r\*_c(φ\*_c) = L.

*Proof.* If φ₁ < φ₂, then F_c(·; φ₂) ≤ F_c(·; φ₁) pointwise, since coverage is monotone in s. Apply Lemma 1 to G = F_c(·; φ₁) at a = r\*_c(φ₂): this gives r\*_c(φ₁) ≥ r\*_c(φ₂). So the limit L exists. By joint continuity, F_c(L; φ\*_c) = L. Then r\*_c(φ\*_c) ≥ L, because L is a fixed point, and r\*_c(φ\*_c) ≤ L, by monotonicity. ∎

So when the collapse in φ is abrupt (L > 0), the tipping point is attained, and r_P := r\*_P(φ\*_P) > 0 is a fixed point there. For km ≥ 2 the exploratory paper's Claim 1 gives an abrupt collapse in x. Here L > 0 is a hypothesis, checked numerically: r_P = 0.6787 in the base case.

**Theorem B.** Let r_P = r\*_P(φ\*_P) > 0 and s_P = 1 − φ\*_P. If C_X(s_P, x·r_P) > C_P(s_P, x·r_P), then φ\*_X > φ\*_P.

*Proof.* Since y ↦ yᵐ is strictly increasing on [0, 1], F_X(r_P; φ\*_P) > F_P(r_P; φ\*_P) = r_P. By continuity in φ there is a δ > 0 with F_X(r_P; φ) > r_P for all φ in [φ\*_P, φ\*_P + δ]. By Lemma 1, r\*_X(φ) ≥ r_P > 0 on that interval, so φ\*_X ≥ φ\*_P + δ. ∎

**Corollary (n = 4, k = 2).** If p_P = x·r_P lies in the A3 window, p₋(s_P) < p_P < 2/3, then φ\*_pairs < min(φ\*_spread, φ\*_co-located), for any m.

## Base case (n = 4, k = 2, m = 1, x = 0.9), from code

| | spread | pairs | co-located |
|---|---|---|---|
| φ\* | 0.1946 | 0.1705 | 0.1946 |
| F_c(r_P) at φ\*_pairs | 0.6975 | 0.6787 (= r_P) | 0.6910 |

At the pairs tangency, s_P = 0.8295, r_P = 0.6787 and p_P = 0.6109. The A3 window at s_P is (0.4258, 2/3), so p_P is inside it and the corollary applies. plan.md quoted F_spread = 0.696 and F_co-located = 0.690; the code gives 0.6975 and 0.6910, and the paper should use the code's values.

## The condition is sufficient, not necessary

The script also runs n = 4, k = 2 for m ∈ {1, 2, 3} and x ∈ {0.95, 1.0}. In every case where the hypothesis holds, the conclusion holds. There is one case where the conclusion holds without the hypothesis: m = 1, x = 1.0 against co-location. There r_P = 0.6677, so p_P sits just above 2/3, and F_co-located(r_P) = 0.6674 < r_P. Even so, φ\*_co-located = 0.2752 > φ\*_pairs = 0.2500. For m ≥ 2, co-location fails both the hypothesis and the conclusion, as Claim 2 (several inputs) predicts.

For B2 this means a setting can show a network reversal while (s_P, x·r_P) lies outside the window, so the 72/109 count need not match "inside the window" exactly. Whether the mismatches sit near the window's edge, as in this example, is to be checked against B2's output.
