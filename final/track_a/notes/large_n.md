# Large-n limit (A7)

Numbers here come from `code/large_n.py` → `results/large_n.json`, and `tests/test_large_n.py` checks them against `exploratory/code/model.py`.

**Result.** Let the number of suppliers n grow, with c clusters and a fixed share α = k/n of suppliers needed. In the formal limit, with m = 1, every intermediate geography (1 < c < ∞) is strictly less shock-tolerant than both co-location and full spread, for every α < x. So the reversal does not fade as redundancy grows; in the limit it holds everywhere. Finite-n values from the model approach the limit slowly, but they keep the same strict ordering, and the gap in φ\* widens with n.

## The limit

Each surviving cluster has b = n/c suppliers, of which about b·p are usable (law of large numbers). The input is covered iff the usable total reaches k = αn, that is, iff at least ⌈cα/p⌉ of the c clusters survive:

    C_c(s, p) → Pr[Bin(c, s) ≥ ⌈cα/p⌉],    co-located: s·1{p ≥ α},    spread (c = n → ∞): 1{sp ≥ α}.

So F(r) = C_c(s, xr)^m is a non-decreasing step function taking the values π_j^m, with π_j(s) = Pr[Bin(c, s) ≥ j].

**Tipping point.** The network keeps r\* > 0 iff

    g_c(s) := max_{1≤j≤c} (j/c)·π_j(s)^m ≥ α/x.

For co-location g₁ = s^m, and for spread g = s.

*Proof.* (⇐) Take r₀ = π_j^m with (j/c)π_j^m ≥ α/x. Then ⌈cα/(x·r₀)⌉ ≤ j, so F(r₀) ≥ π_j^m = r₀. The iterates Fᵗ(r₀) are non-decreasing and take finitely many values, so they settle at a fixed point ≥ r₀ > 0. (⇒) A positive fixed point is some r\* = π_J^m with J = ⌈cα/(x·r\*)⌉ ≤ c. Then J ≥ cα/(x·r\*), which is the condition for j = J. ∎

g_c is increasing in s, so φ\*_c = 1 − min{s : g_c(s) ≥ α/x}. Spread gives φ\* = 1 − α/x, and co-location gives 1 − (α/x)^(1/m): the same forms as Claim 2, with α in place of the finite-n critical x.

**Intermediate c loses to spread, and for m = 1 to co-location too.** Let X ~ Bin(c, s). By Markov's inequality j·Pr[X ≥ j] ≤ E[X] = cs, with equality only if X takes just the values 0 and j. That is impossible for c ≥ 2 and 0 < s < 1. So (j/c)·π_j^m ≤ (j/c)·π_j < s for every j, and g_c(s) < s. An intermediate c therefore needs a larger s, which means φ\*_c < φ\*_spread for every m. When m = 1, φ\*_co-located = φ\*_spread as well. ∎

The mechanism is the same as in the finite case. A spread firm gets the average share s of its suppliers almost surely. An intermediate firm gets a lumpy share j/c and needs enough lumps, and Markov says lumpiness costs.

**c = 2 in closed form (m = 1).** g₂(s) = max(s − s²/2, s²), so φ\*₂ = 1 − min(√(α/x), 1 − √(1 − 2α/x)), where the second term applies when 2α/x ≤ 1. This is checked in the test.

## Limit values (x = 0.9)

φ\* in the limit, from `results/large_n.json`:

| α | m | c = 1 | c = 2 | c = 3 | c = 4 | c = 5 | c = 10 | c = 20 | spread |
|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 1 | 0.778 | 0.745 | 0.693 | 0.646 | 0.658 | 0.649 | 0.655 | 0.778 |
| 0.4 | 1 | 0.556 | 0.333 | 0.387 | 0.333 | 0.365 | 0.363 | 0.391 | 0.556 |
| 0.6 | 1 | 0.333 | 0.184 | 0.126 | 0.151 | 0.151 | 0.148 | 0.176 | 0.333 |
| 0.2 | 2 | 0.529 | 0.577 | 0.568 | 0.514 | 0.549 | 0.582 | 0.607 | 0.778 |
| 0.4 | 2 | 0.333 | 0.239 | 0.274 | 0.261 | 0.281 | 0.313 | 0.354 | 0.556 |

- **m = 1:** every intermediate c is below both extremes, as proved.
- **Shape in c:** φ\*_c is not monotone in c (α = 0.4: c = 2 and c = 4 tie at 0.333, c = 3 is 0.387), because ⌈cα/p⌉ jumps in steps. It climbs back toward the extremes only slowly as c grows (c = 20: 0.391).
- **m ≥ 2:** spread is still best, but an intermediate c can beat co-location (α = 0.2: c = 2 has 0.577 against 0.529). This matches Claim 2: with several inputs, co-location is worse.

## Finite n against the limit (α = 0.4, m = 1, x = 0.9)

φ\* from `model.phi_star`:

| n | k | c = 1 (= spread) | c = 2 | c = 5 |
|---|---|---|---|---|
| 10 | 4 | 0.329 | 0.243 | 0.292 |
| 20 | 8 | 0.361 | 0.218 | 0.280 |
| 40 | 16 | 0.398 | 0.226 | 0.282 |
| 80 | 32 | 0.432 | 0.247 | 0.291 |
| 160 | 64 | 0.461 | 0.266 | 0.304 |
| limit | | 0.556 | 0.333 | 0.365 |

At every n, the ordering is the one the limit predicts. The gap between the extremes and pairs grows from 0.086 at n = 10 to 0.195 at n = 160. Convergence is slow: the finite-n values are still well below the limit at n = 160, plausibly because of the order-√n fluctuations around b·p.

The swap of limits (n → ∞ inside the fixed-point problem) is not proved here. The claims for the paper are the formal limit, plus finite-n numbers that agree with its ordering.
