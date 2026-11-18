"""Lemma A for general (n, k, c) (task A5).

c = 2, any even n and k (proved in notes/lemma_a_general.md):
  C_2 - C_1 = s(1 - s) [2 S_k(n/2, p) - S_k(n, p)], so pairs lose to co-location iff p < p_hat(n, k),
  the unique root of 2 S_k(n/2, p) = S_k(n, p) (2 <= k <= n/2); never for k = 1; always for k > n/2.

Any c | n with 1 < c < n, b = n / c: the co-location edge depends on s. Its limits are
  s -> 0:  c S_k(b, p) = S_k(n, p)            s -> 1:  c S_k(n - b, p) = (c - 1) S_k(n, p)
and are computed here with the numerical edge at several s, plus where c is strictly worst.

Coverage comes from exploratory/code/model.py: C_c(s, p) = F(p, x=1, m=1, n, k, c, phi=1-s).

Usage:  python3 lemma_a_general.py      (writes ../results/lemma_a_general.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "exploratory", "code"))

import numpy as np  # noqa: E402
from scipy.optimize import brentq  # noqa: E402

from model import F, S  # noqa: E402

OUT = os.path.join(HERE, "..", "results", "lemma_a_general.json")
N_VALUES = (4, 6, 8, 10, 12)
S_EDGE = (0.6, 0.8, 0.9, 0.95)
S_GRID = np.linspace(0.5, 0.99, 50)
P_GRID = np.linspace(0.01, 0.99, 99)
P_FINE = np.linspace(1e-4, 1 - 1e-4, 20_001)


def cov(c, n, k, s, p):
    return F(p, 1.0, 1, n, k, c, 1.0 - s)


def roots(f):
    """All roots of f on (0, 1), from sign changes on a fine grid, refined by brentq."""
    v = f(P_FINE)
    idx = np.flatnonzero(np.sign(v[:-1]) * np.sign(v[1:]) < 0)
    return [brentq(f, P_FINE[i], P_FINE[i + 1], xtol=1e-14) for i in idx]


def p_hat_c2(n, k):
    """Root of 2 S_k(n/2, p) = S_k(n, p); None if there is none in (0, 1)."""
    r = roots(lambda p: 2 * S(k, n // 2, p) - S(k, n, p))
    assert len(r) <= 1
    return r[0] if r else None


def colocation_edge_limits(n, k, c):
    b = n // c
    lo = roots(lambda p: c * S(k, b, p) - S(k, n, p))
    hi = roots(lambda p: c * S(k, n - b, p) - (c - 1) * S(k, n, p))
    assert len(lo) <= 1 and len(hi) <= 1
    return (lo[0] if lo else None), (hi[0] if hi else None)


def worst_share(n, k, c):
    """Share of the (s, p) grid where c is strictly below both extremes, and strictly below every divisor."""
    cs = [d for d in range(1, n + 1) if n % d == 0]
    vs_ext, vs_all = 0, 0
    for s in S_GRID:
        C = {d: cov(d, n, k, s, P_GRID) for d in cs}
        vs_ext += int(np.sum(C[c] < np.minimum(C[1], C[n])))
        vs_all += int(np.sum(C[c] < np.min([C[d] for d in cs if d != c], axis=0)))
    total = len(S_GRID) * len(P_GRID)
    return vs_ext / total, vs_all / total


def main():
    c2 = []
    for n in N_VALUES:
        for k in range(1, n + 1):
            ph = p_hat_c2(n, k)
            regime = "never worse" if k == 1 else ("always worse" if k > n // 2 else "worse iff p < p_hat")
            c2.append({"n": n, "k": k, "p_hat": ph, "regime": regime})

    general = []
    for n in N_VALUES:
        for c in (d for d in range(2, n) if n % d == 0):
            for k in range(2, n + 1):
                lim0, lim1 = colocation_edge_limits(n, k, c)
                edges = {str(s): roots(lambda p, s=s: cov(c, n, k, s, p) - cov(1, n, k, s, p)) for s in S_EDGE}
                ext, allc = worst_share(n, k, c)
                general.append({"n": n, "c": c, "k": k, "edge_limit_s0": lim0, "edge_limit_s1": lim1,
                                "colocation_edge_at_s": edges,
                                "share_worst_vs_extremes": ext, "share_worst_vs_all_divisors": allc})

    out = {"c2_closed_form": c2, "general_c": general,
           "grid": {"s": [float(S_GRID[0]), float(S_GRID[-1]), len(S_GRID)],
                    "p": [float(P_GRID[0]), float(P_GRID[-1]), len(P_GRID)]}}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    for r in c2:
        if r["p_hat"] is not None:
            print(f"c=2 n={r['n']:2d} k={r['k']:2d} p_hat={r['p_hat']:.4f}")
    for g in general:
        e = {s: [round(x, 4) for x in v] for s, v in g["colocation_edge_at_s"].items()}
        lims = [None if x is None else round(x, 4) for x in (g["edge_limit_s0"], g["edge_limit_s1"])]
        print(f"n={g['n']:2d} c={g['c']} k={g['k']:2d} limits={lims} edges={e} "
              f"worst={g['share_worst_vs_extremes']:.3f}/{g['share_worst_vs_all_divisors']:.3f}")


if __name__ == "__main__":
    main()
