# Claim 3 for any refinement (A6)

Numbers here come from `code/claim3_refinement.py` → `results/claim3_refinement.json`; `code/partition_coverage.py` handles clusters of arbitrary sizes and is tested against `exploratory/code/model.py` in `tests/test_partition_coverage.py`.

**Result.** The exploratory paper's Claim 3 covers going from c to c′ equal clusters with c | c′, and its proof does halving explicitly ("other splits work the same way"). It extends to any refinement, unequal clusters included:

> **Claim 3′.** Let k = 1. If geography B is obtained from geography A by splitting clusters into smaller ones, of any sizes, then for every φ the coverage, F, r\* and ρ under B are at least those under A, and φ\*_B ≥ φ\*_A.

Refinement is needed: with more clusters that are not a refinement, coverage can be lower (below).

## Proof

Let q = 1 − p with p = x·r, and s = 1 − φ. With k = 1 an input fails iff no cluster supplies a usable supplier. A cluster of size b supplies none with probability φ + s·qᵇ (hit, or not hit and all b unusable), independently across clusters, so

    coverage(b₁, …, b_c) = 1 − ∏ᵢ (φ + s·q^{bᵢ}).

**One split.** Replace a cluster of size b = b₁ + b₂ by two clusters of sizes b₁ and b₂. With u = q^{b₁} and v = q^{b₂}, using φ + s = 1,

    (φ + s·uv) − (φ + s·u)(φ + s·v) = φs(1 − u)(1 − v) ≥ 0.

So that cluster's failure factor goes down, and the other factors are unchanged and non-negative. Coverage goes up weakly, and strictly when 0 < φ < 1, p > 0 and every other factor is positive. Sympy checks the identity in `split_identity()`.

**Any refinement.** A refinement is a finite sequence of single splits, so coverage is weakly larger for every (s, p).

**Network.** Then F_B(r) = coverage_B(s, xr)^m ≥ F_A(r) for every r in [0, 1]. Let r_A\* be the largest fixed point of F_A. Then F_B(r_A\*) − r_A\* ≥ 0 and F_B(1) − 1 ≤ 0, and F_B is continuous. So F_B has a fixed point in [r_A\*, 1], which gives r_B\* ≥ r_A\* (the same comparison step planned for Theorem B). This holds at every φ, so ρ_B ≥ ρ_A and φ\*_B = sup{φ : r_B\* > 0} ≥ φ\*_A. ∎

## Numerical checks

- **Coverage:** all 330 refinement pairs of partitions of n ≤ 8 were checked on a 50 × 99 grid of (s, p) in [0.01, 0.99]². There were 0 violations. The smallest gap is 6·10⁻¹³ (≥ 0, at (1,…,1) vs (2,1,…,1)).
- **Network φ\*:** every refinement pair for n ∈ {4, 6}, m ∈ {1, 2, 3} and x ∈ {0.6, 0.9, 1.0} was checked, 477 comparisons in all. There were 0 violations (tolerance 10⁻⁴).

## Without refinement it fails

The check also covered pairs of partitions of n ≤ 8 where one has more clusters but does not refine the other. In 21 of these 43 pairs, the one with more clusters has lower coverage somewhere on the grid. Examples:

| more clusters | fewer clusters | min coverage gap |
|---|---|---|
| (4, 1, 1) | (3, 3) | −0.0022 |
| (3, 1, 1, 1) | (2, 2, 2) | −0.0011 |
| (5, 1, 1) | (4, 3) | −0.0083 |

So "more regions" is not the right monotonicity even when one supplier is enough. "Finer split of the same regions" is. A balanced split into fewer regions can beat a lopsided split into more.
