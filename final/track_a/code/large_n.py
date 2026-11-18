"""Large-n limit (task A7): n -> infinity with c fixed and a fixed share alpha = k / n of suppliers needed.

A surviving cluster then holds b p usable suppliers (law of large numbers), so the input is covered iff
at least ceil(c alpha / p) of the c clusters survive:

  C_c(s, p) -> P[Bin(c, s) >= ceil(c alpha / p)]      (co-located: s 1{p >= alpha}; spread: 1{s p >= alpha})

F(r) = C_c(s, x r)^m is then a step function, and the network survives (r* > 0) iff

  g_c(s) = max_j (j / c) P[Bin(c, s) >= j]^m  >=  alpha / x,      g_1 = s^m, g_spread = s,

so phi*_c = 1 - (the smallest s with g_c(s) >= alpha / x). This script computes those limits and the
finite-n phi* from exploratory/code/model.py, to show the convergence.

Usage:  python3 large_n.py      (writes ../results/large_n.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "exploratory", "code"))

import numpy as np  # noqa: E402
from scipy.stats import binom  # noqa: E402

from model import phi_star  # noqa: E402

OUT = os.path.join(HERE, "..", "results", "large_n.json")
X = 0.9
C_VALUES = (1, 2, 3, 4, 5, 10, 20)


def g(c, s, m):
    """max_j (j/c) P[Bin(c, s) >= j]^m; c = None means spread (the limit c -> infinity), g = s."""
    if c is None:
        return s
    j = np.arange(1, c + 1)
    return float(np.max(j / c * binom.sf(j - 1, c, s) ** m))


def phi_star_limit(c, alpha, x, m, tol=1e-10):
    """1 - min{s : g_c(s) >= alpha / x}; g_c is increasing in s, so bisect."""
    target = alpha / x
    if g(c, 1.0, m) < target:
        return 0.0
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if g(c, mid, m) >= target:
            hi = mid
        else:
            lo = mid
    return 1.0 - hi


def limit_table(alphas=(0.2, 0.4, 0.6), ms=(1, 2, 3)):
    rows = []
    for alpha in alphas:
        for m in ms:
            row = {"alpha": alpha, "m": m, "x": X,
                   "phi_star": {str(c): phi_star_limit(c, alpha, X, m) for c in C_VALUES}}
            row["phi_star"]["spread"] = phi_star_limit(None, alpha, X, m)
            rows.append(row)
    return rows


def convergence(alpha=0.4, m=1, ns=(10, 20, 40, 80, 160), cs=(1, 2, 5)):
    """Finite-n phi* (model.py) vs the limit, for n with alpha n integer and c | n."""
    rows = []
    for n in ns:
        k = round(alpha * n)
        row = {"n": n, "k": k, "phi_star": {str(c): phi_star(X, m, n, k, c) for c in cs}}
        row["phi_star"]["spread"] = phi_star(X, m, n, k, n)
        rows.append(row)
    limit = {str(c): phi_star_limit(c, alpha, X, m) for c in cs}
    limit["spread"] = phi_star_limit(None, alpha, X, m)
    return {"alpha": alpha, "m": m, "x": X, "finite_n": rows, "limit": limit}


def markov_gap(cs=C_VALUES, s_grid=np.linspace(0.01, 0.99, 99)):
    """Smallest s - g_c(s) over the grid for m = 1 (> 0 for 1 < c: intermediate c strictly below spread)."""
    return {str(c): float(min(s - g(c, s, 1) for s in s_grid)) for c in cs}


def main():
    out = {"limit": limit_table(), "convergence": convergence(), "markov_gap_m1": markov_gap()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
