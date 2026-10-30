"""Mean-field analysis of the k-of-n multisourcing model with correlated regional shocks.

Model (extends Elliott, Golub & Leduc 2022, eq. (1)):
  * each firm needs m essential inputs;
  * each input has n potential suppliers, split into c regional clusters of b = n / c;
  * a relationship is operational with probability x;
  * an input is sourced iff at least k of its n suppliers are functional AND operational;
  * each region is hit independently with probability phi; firms in hit regions are dead.

With r = P(firm functional | its own region not hit), the deep-network recursion is

  F(r) = [ sum_{C=0}^{c} Binom(C; c, 1-phi) * S_k(C*b, x*r) ]^m,    S_k(N,p) = P[Bin(N,p) >= k]

and aggregate reliability is rho = (1 - phi) * r*, where r* is the largest fixed point of F.
"""
from functools import lru_cache

import numpy as np
from scipy.stats import binom

GRID = np.linspace(1e-6, 1.0, 200_001)


def S(k, N, p):
    """P[Bin(N, p) >= k], vectorized over p. Zero when N < k."""
    if N < k:
        return np.zeros_like(np.asarray(p, dtype=float))
    return binom.sf(k - 1, N, p)


def F(r, x, m, n, k, c=None, phi=0.0):
    """One step of the recursion (eq. 3). c defaults to n (fully spread suppliers)."""
    c = n if c is None else c
    assert n % c == 0, "n must be divisible by c"
    b = n // c
    r = np.asarray(r, dtype=float)
    tot = np.zeros_like(r)
    for C in range(c + 1):
        w = binom.pmf(C, c, 1.0 - phi)
        if w > 0:
            tot = tot + w * S(k, C * b, x * r)
    return tot ** m


def largest_fixed_point(x, m, n, k, c=None, phi=0.0):
    """Largest root of F(r) = r on (0, 1]; returns 0 if none (collapsed network)."""
    g = F(GRID, x, m, n, k, c, phi) - GRID
    pos = np.flatnonzero(g >= 0)
    if len(pos) == 0:
        return 0.0
    i = pos[-1]
    if i == len(GRID) - 1:
        return 1.0
    lo, hi = GRID[i], GRID[i + 1]          # g(lo) >= 0 > g(hi): refine by bisection
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if F(mid, x, m, n, k, c, phi) - mid >= 0:
            lo = mid
        else:
            hi = mid
    r = 0.5 * (lo + hi)
    return r if r > 1e-4 else 0.0


def finite_depth(x, m, n, k, c=None, phi=0.0, depth=20):
    """Reliability (conditional on own region surviving) of a depth-D firm: F^D(1)."""
    r = 1.0
    for _ in range(depth):
        r = float(F(r, x, m, n, k, c, phi))
    return r


def rho(x, m, n, k, c=None, phi=0.0, phi_own=None):
    """Aggregate deep-network reliability rho = (1 - phi_own) r*.

    phi is the probability that a supplier cluster's region is hit (the supply-weighted
    shock); phi_own is the share of firms whose own region is hit. They coincide when
    supply is spread evenly across regions (the default)."""
    phi_own = phi if phi_own is None else phi_own
    return (1.0 - phi_own) * largest_fixed_point(x, m, n, k, c, phi)


def x_crit(m, n, k, tol=1e-6):
    """Smallest relationship strength with a positive fixed point (phi = 0)."""
    lo, hi = 0.0, 1.0
    if largest_fixed_point(hi, m, n, k) == 0:
        return float("nan")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if largest_fixed_point(mid, m, n, k) > 0:
            hi = mid
        else:
            lo = mid
    return hi


def phi_star(x, m, n, k, c=None, tol=1e-6):
    """Largest regional shock probability the deep network survives (r* > 0)."""
    lo, hi = 0.0, 1.0
    if largest_fixed_point(x, m, n, k, c, 0.0) == 0:
        return 0.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if largest_fixed_point(x, m, n, k, c, mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def jump_at_threshold(m, n, k):
    """r* just above x_crit (size of the discontinuity; ~0 for a continuous transition)."""
    xc = x_crit(m, n, k)
    return largest_fixed_point(xc + 1e-5, m, n, k)


# ------------------------------------------------------------------ geography theorems
def phi_star_closed_form(x, m, n, k):
    """Theorem 2 (paper numbering): collapse thresholds of the two geographic extremes in closed form.

    spread (c = n):     phi* = 1 - x_crit / x
    co-located (c = 1): phi* = 1 - (x_crit / x) ** (1 / m) = 1 - (1 - phi*_spread) ** (1 / m)
    Both are 0 when the network is already dead without a shock (x < x_crit)."""
    xc = x_crit(m, n, k)
    if not np.isfinite(xc) or x < xc:
        return {"spread": 0.0, "colocated": 0.0}
    return {"spread": max(0.0, 1.0 - xc / x), "colocated": max(0.0, 1.0 - (xc / x) ** (1.0 / m))}


def refinement_violations(x, m, n, k, tol=1e-4):
    """Proposition 4 (paper numbering) scan: pairs (c, c2) with c | c2 | n where splitting clusters LOWERS phi*.

    Returns a list of (c, c2, phi*_c, phi*_c2) with phi*_c > phi*_c2 + tol (empty for k = 1 by Theorem 3)."""
    cs = [c for c in range(1, n + 1) if n % c == 0]
    ps = {c: phi_star(x, m, n, k, c) for c in cs}
    return [(c, c2, ps[c], ps[c2]) for c in cs for c2 in cs
            if c < c2 and c2 % c == 0 and ps[c] > ps[c2] + tol]


# ------------------------------------------------------------------ DGM (2006), Erdos-Renyi graphs
def dgm_er_core_size(k, p, z):
    """Size of the giant k-core (share of all vertices) of an ER graph with mean degree z after
    keeping each vertex with probability p (Dorogovtsev, Goltsev & Mendes 2006, eqs. 1 and 4)."""
    from scipy.special import gammaincc
    if k <= 1:
        return p
    R = 0.0
    for _ in range(200_000):                 # lowest root of R = 1 - p + p Q(k-1, z(1-R)), from R = 0
        Rn = 1.0 - p + p * gammaincc(k - 1, z * (1.0 - R))
        if abs(Rn - R) < 1e-14:
            R = Rn
            break
        R = Rn
    if R > 1.0 - 1e-9:
        return 0.0
    return p * (1.0 - gammaincc(k, z * (1.0 - R)))


def dgm_er_Qc(k, z):
    """Largest share Q of randomly removed vertices at which the giant k-core still exists."""
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if dgm_er_core_size(k, 1.0 - mid, z) > 1e-6:
            lo = mid
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    print("Table 1: x_crit and jump (phi = 0)")
    for (m, n, k) in [(1, 4, 1), (1, 4, 2), (2, 4, 1), (2, 4, 2), (2, 4, 3),
                      (3, 4, 1), (3, 4, 2), (2, 6, 2), (2, 8, 2)]:
        print(f"  m={m} n={n} k={k}: x_crit={x_crit(m, n, k):.3f}  jump={jump_at_threshold(m, n, k):.3f}")
    print("Table 2: phi* and rho (x = 0.9, m = 2, n = 4)")
    for k in (1, 2):
        for c in (4, 2, 1):
            vals = [rho(0.9, 2, 4, k, c, p) for p in (0.0, 0.02, 0.05, 0.10)]
            print(f"  k={k} c={c}: phi*={phi_star(0.9, 2, 4, k, c):.3f}  rho(0,.02,.05,.10)="
                  + " ".join(f"{v:.3f}" for v in vals))
    # check P3 closed form: phi* = 1 - x_crit / x when c = n
    for k in (1, 2):
        print(f"  THM2a check k={k}: 1 - xcrit/x = {1 - x_crit(2, 4, k) / 0.9:.3f}")
    # Theorem 2 check and Proposition 4 scan
    for k in (1, 2):
        cf = phi_star_closed_form(0.9, 2, 4, k)
        print(f"  THM2b k={k}: closed form spread={cf['spread']:.4f} colocated={cf['colocated']:.4f}  "
              f"numeric {phi_star(0.9, 2, 4, k, 4):.4f} {phi_star(0.9, 2, 4, k, 1):.4f}")
    cases = viol = viol_k1 = 0
    for n in (2, 4, 6, 8):
        for k in range(1, n + 1):
            for m in (1, 2, 3):
                for x in (0.6, 0.7, 0.8, 0.9, 0.95, 1.0):
                    cases += 1
                    if refinement_violations(x, m, n, k):
                        viol += 1
                        viol_k1 += (k == 1)
    print(f"  TRAP scan: cases={cases} violations={viol} (k=1: {viol_k1})")
