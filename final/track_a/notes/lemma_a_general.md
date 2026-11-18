# Lemma A for general (n, k, c) (A5)

Numbers here come from `code/lemma_a_general.py` → `results/lemma_a_general.json`, and `tests/test_lemma_a_general.py` checks them against `exploratory/code/model.py`. Arjun's B1 grid data, once it lands, is a further cross-check.

**Result.**
- **c = 2:** pairs lose to co-location exactly when p < p̂(n, k), the unique root of 2S_k(n/2, p) = S_k(n, p), for every s. This generalizes 2/3. There is no such p for k = 1 (Claim 3), and pairs always lose for k > n/2.
- **Other c:** the co-location edge depends on s. It lies between two explicit limits and falls as s rises.
- **The spread edge** is characterized numerically only. A general closed form for the full window is not claimed.

## Tool: a monotone ratio

S_k(N, p) = Pr[Bin(N, p) ≥ k] is the CDF at p of the k-th smallest of N uniforms. Its density is f_N(t) = N·C(N−1, k−1)·t^(k−1)(1−t)^(N−k).

**Lemma R.** For k ≤ M < N, the ratio R(p) = S_k(N, p) / S_k(M, p) is strictly decreasing on (0, 1], from C(N, k)/C(M, k) at p → 0 down to 1 at p = 1.

*Proof.* f_N/f_M ∝ (1−t)^(N−M) is strictly decreasing. So S_k(N, p) = ∫₀ᵖ (f_N/f_M)·f_M > (f_N(p)/f_M(p))·S_k(M, p), which makes R′ = (f_N·S_k(M) − S_k(N)·f_M)/S_k(M)² < 0. As p → 0, R tends to the ratio of the leading coefficients, N·C(N−1, k−1) / (M·C(M−1, k−1)) = C(N, k)/C(M, k). ∎

## c = 2, any even n and k

With b = n/2, the only intermediate state is that one cluster survives, so

    C₂ − C₁ = s(1 − s)·[2S_k(b, p) − S_k(n, p)].

The sign does not depend on s, and pairs lose to co-location iff R(p) = S_k(n, p)/S_k(b, p) > 2.

- **k = 1:** R starts at C(2b, 1)/C(b, 1) = 2 and decreases, so R < 2 on (0, 1). Pairs always win, which is Claim 3.
- **2 ≤ k ≤ b:** Vandermonde gives C(2b, k) ≥ 2C(b, k) + b·C(b, k−1) > 2C(b, k), so R falls from above 2 to 1 and crosses 2 exactly once, at p̂(n, k). Pairs lose iff p < p̂(n, k).
- **k > b:** S_k(b, p) = 0, so the bracket is −S_k(n, p) < 0. One surviving cluster can never cover the input, and pairs always lose.

| n \ k | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| 4 | 0.6667 | | | | |
| 6 | 0.4417 | 0.7881 | | | |
| 8 | 0.3281 | 0.5999 | 0.8401 | | |
| 10 | 0.2606 | 0.4816 | 0.6825 | 0.8704 | |
| 12 | 0.2160 | 0.4017 | 0.5726 | 0.7346 | 0.8909 |

p̂ falls as n grows with k fixed: more suppliers per cluster make the lone surviving cluster more useful. It rises as k grows with n fixed.

## General c (1 < c < n, b = n/c)

Now several intermediate states mix, and the sign of C_c − C₁ at a given p depends on s. Two limits are explicit:

- **s → 0:** at most one cluster survives, and (C_c − C₁)/s → c·S_k(b, p) − S_k(n, p).
- **s → 1:** at most one cluster is lost, and (C_c − C₁)/(1 − s) → c·S_k(n−b, p) − (c−1)·S_k(n, p).

By Lemma R, each has at most one root in (0, 1):

- **p̂₀:** exists iff k ≤ b and C(n, k) > c·C(b, k). If k > b, c loses to co-location for every p as s → 0.
- **p̂₁:** exists iff k ≤ n − b and C(n, k)/C(n−b, k) > c/(c−1). If k > n − b, losing any one cluster is fatal, so C_c = s^c·S_k(n) < s·S_k(n) = C₁ for all s < 1 and p > 0.

For c = 2 the two limits coincide with p̂(n, k).

**Numerical characterization.** The cases are n ∈ {6, 8, 10, 12}, every divisor 2 < c < n, every k ≤ n − b, and s ∈ {0.6, 0.8, 0.9, 0.95}.

- C_c = C₁ has at most one root in p.
- The root lies between p̂₁ and p̂₀, with p̂₀ taken as 1 when it does not exist.
- The root is non-increasing in s. It moves from near p̂₀ toward p̂₁ as s → 1.

For example, with n = 12, c = 3, k = 3 the edge is 0.4055, 0.3728, 0.3582 and 0.3514 at those s values, between p̂₁ = 0.3449 and p̂₀ = 0.5102. Proving the monotonicity in s for general c is open; so far it is numerical only.

## How much of the (s, p) square has c strictly worst

The grid is s ∈ [0.5, 0.99] (50 values) × p ∈ [0.01, 0.99] (99 values). Shares for c strictly below both extremes, from `results/lemma_a_general.json`:

- **k = 1:** never strictly worst, by Claim 3′ (A6), since each c refines c = 1. This follows from the proof; the script does not compute it.
- **n = 4, c = 2, k = 2:** 0.152.
- **k ≥ 2 elsewhere:** the n ≤ 12 shares range up to 0.255 (n = 12, c = 2, k = 7).
- **Largest k:** the share drops to 0 at k = n, where every geography needs every supplier.

This grid differs from the one in plan.md §4, so these shares are not comparable with its counts (754/3500 etc.). Matching those counts is B1's job.
