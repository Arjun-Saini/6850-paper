# Lemma A, n = 4, k = 2: the reversal window in closed form (A3)

Numbers here come from `code/lemma_a_n4k2.py` → `results/lemma_a_n4k2.json`; `tests/test_lemma_a_n4k2.py` checks them against `exploratory/code/model.py`.

**Result.** For a single firm with 4 suppliers needing 2, pairs (c = 2) are strictly worse than both co-location (c = 1) and full spread (c = 4) exactly when

    p₋(s) < p < 2/3,    where p₋(s) = 2 / (4s + √(2s(5s − 3))),

and this window is nonempty exactly when s > s₀ = (3 − √3)/2 ≈ 0.634. As s → 1, p₋(s) → 1/3, so the window tends to (1/3, 2/3).

## Setup

s = 1 − φ is the probability that a region survives, p is the probability that a surviving supplier is usable, and S₂(N, p) = Pr[Bin(N, p) ≥ 2] = 1 − (1−p)^N − Np(1−p)^(N−1). With S₂(4, p) = 6p² − 8p³ + 3p⁴:

- co-located: C₁ = s·S₂(4, p)
- pairs: C₂ = s²·S₂(4, p) + 2s(1 − s)·p²
- spread: C₄ = S₂(4, sp)

## Upper edge: pairs vs co-located

C₂ − C₁ = s(1 − s)·[2p² − S₂(4, p)] = s(1 − s)·p²(2 − p)(3p − 2).

For 0 < s < 1 the sign is the sign of 3p − 2, so pairs lose to co-location iff p < 2/3, whatever s is.

## Lower edge: pairs vs spread

C₂ − C₄ = s(1 − s)·p²·g(s, p),    with g(s, p) = 3s(1 + s)p² − 8sp + 2.

Pairs lose to spread iff g < 0, that is, iff p lies strictly between the roots of g. The discriminant of g in p is 8s(5s − 3), so there are real roots only for s ≥ 3/5. The roots are

    p₋(s) = 2 / (4s + √(2s(5s − 3))),    p₊(s) = (4s + √(2s(5s − 3))) / (3s(1 + s)).

At s = 3/5 they meet at 5/6. For s in [3/5, 1), p₊(s) > 2/3, so the binding edges of the window are p₋(s) from below and 2/3 from above.

## When the window opens

The window is nonempty iff p₋(s) < 2/3, that is, iff g(s, 2/3) = (2/3)(2s² − 6s + 3) < 0. The root of 2s² − 6s + 3 in (0, 1) is s₀ = (3 − √3)/2 ≈ 0.634. For s between 3/5 and s₀, pairs do beat spread somewhere, but only at p values above 2/3, where co-location beats pairs.

## Check against the plan.md §4 table

| s | p₋(s) | window |
|---|---|---|
| 0.6 | 0.833 | none (p₋ > 2/3) |
| 0.8 | 0.448 | (0.448, 2/3) |
| 0.9 | 0.381 | (0.381, 2/3) |
| 0.95 | 0.356 | (0.356, 2/3) |

These match the grid estimates in plan.md (≈ 0.448, 0.382, 0.356; none at 0.6). The test also checks that brute force on `model.F` (m = 1, x = 1, r = p) gives exactly this window over 36 values of s in [0.64, 0.99] and 981 values of p, and no window for s below s₀.

## Reading

The upper edge is the knife-edge state. When one of the two clusters is hit, pairs keep exactly 2 suppliers and need both, so they are covered with probability p². The bracket 2p² − S₂(4, p) compares that state against all 4 suppliers surviving, and it turns negative below p = 2/3.

For the network (Theorem B), the base case's tipping point is (s, p) ≈ (0.83, 0.61) per plan.md, inside this window (p₋(0.83) ≈ 0.43). Track A will recompute this from code in A4 rather than rely on plan.md's numbers.
