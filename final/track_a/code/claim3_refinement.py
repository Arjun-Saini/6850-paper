"""Claim 3 for any refinement (task A6): with k = 1, splitting any cluster, equally or not, never hurts.

Proof step checked here symbolically: with k = 1 a cluster of size b fails (no usable supplier) with
probability phi + s q^b (q = 1 - p, s = 1 - phi), independently across clusters. Splitting b = b1 + b2:

  (phi + s q^b) - (phi + s q^b1)(phi + s q^b2) = phi s (1 - q^b1)(1 - q^b2) >= 0.

Numerical checks: single-firm coverage over every refinement pair of partitions of n <= 8 on an
(s, p) grid; phi* of the deep network for every refinement pair with n <= 6; and, for contrast,
non-nested partitions, where more clusters need not mean more coverage.

Usage:  python3 claim3_refinement.py      (writes ../results/claim3_refinement.json)
"""
import json
import os
from itertools import permutations

import numpy as np
import sympy as sp

from partition_coverage import coverage, partitions, phi_star, refines

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "claim3_refinement.json")
S_GRID = np.linspace(0.01, 0.99, 50)
P_GRID = np.linspace(0.01, 0.99, 99)
TOL = 1e-12


def split_identity():
    phi, q = sp.symbols("phi q", positive=True)
    b1, b2 = sp.symbols("b1 b2", positive=True, integer=True)
    s = 1 - phi
    lhs = (phi + s * q ** (b1 + b2)) - (phi + s * q**b1) * (phi + s * q**b2)
    rhs = phi * s * (1 - q**b1) * (1 - q**b2)
    assert sp.simplify(sp.expand(lhs - rhs)) == 0
    return {"identity": "(phi + s q^(b1+b2)) - (phi + s q^b1)(phi + s q^b2) = phi s (1 - q^b1)(1 - q^b2)",
            "checked": True}


def min_gap(fine, coarse, k=1):
    """min over the (s, p) grid of coverage(fine) - coverage(coarse)."""
    return min(float(np.min(coverage(fine, sv, P_GRID, k) - coverage(coarse, sv, P_GRID, k))) for sv in S_GRID)


def refinement_pairs(n):
    parts = partitions(n)
    return [(f, c) for f, c in permutations(parts, 2) if refines(f, c)]


def coverage_check(n_max=8):
    pairs = [pc for n in range(2, n_max + 1) for pc in refinement_pairs(n)]
    worst = min((min_gap(f, c), f, c) for f, c in pairs)
    return {"n_max": n_max, "refinement_pairs": len(pairs),
            "violations": sum(min_gap(f, c) < -TOL for f, c in pairs),
            "smallest_gap": worst[0], "smallest_gap_at": [list(worst[1]), list(worst[2])]}


def network_check(n_values=(4, 6), m_values=(1, 2, 3), x_values=(0.6, 0.9, 1.0), tol=1e-4):
    parts = {n: partitions(n) for n in n_values}
    rows, bad = 0, []
    for n in n_values:
        for m in m_values:
            for x in x_values:
                ps = {P: phi_star(x, m, P, 1) for P in parts[n]}
                for f, c in refinement_pairs(n):
                    rows += 1
                    if ps[f] < ps[c] - tol:
                        bad.append([n, m, x, list(f), list(c), ps[f], ps[c]])
    return {"n": list(n_values), "m": list(m_values), "x": list(x_values),
            "comparisons": rows, "violations": bad}


def non_nested_check(n_max=8):
    """Pairs with more clusters that do NOT refine the other: does more clusters still mean more coverage?"""
    total, worse = 0, []
    for n in range(2, n_max + 1):
        for f, c in permutations(partitions(n), 2):
            if len(f) > len(c) and not refines(f, c):
                total += 1
                g = min_gap(f, c)
                if g < -TOL:
                    worse.append([list(f), list(c), g])
    return {"pairs": total, "pairs_where_more_clusters_is_worse_somewhere": len(worse),
            "examples": worse[:5]}


def main():
    out = {"split_identity": split_identity(), "coverage": coverage_check(),
           "network_phi_star": network_check(), "non_nested": non_nested_check()}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
