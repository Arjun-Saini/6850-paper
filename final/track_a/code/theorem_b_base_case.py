"""Theorem B, base case (task A4): n = 4, k = 2, m = 1, x = 0.9.

Computes from exploratory/code/model.py:
  * phi* for spread (c = 4), pairs (c = 2) and co-located (c = 1);
  * r_P, the largest fixed point of the pairs recursion at phi = phi*_pairs (the tangency point);
  * F_c(r_P) at phi*_pairs for each geography: Theorem B's hypothesis is F_X(r_P) > F_pairs(r_P) = r_P;
  * whether (s, p) = (1 - phi*_pairs, x r_P) lies in the Lemma A window from lemma_a_n4k2.py.

Usage:  python3 theorem_b_base_case.py      (writes ../results/theorem_b_base_case.json)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "exploratory", "code"))

import sympy as sp  # noqa: E402

from lemma_a_n4k2 import derive, s as s_sym  # noqa: E402
from model import F, largest_fixed_point, phi_star  # noqa: E402

OUT = os.path.join(HERE, "..", "results", "theorem_b_base_case.json")
X, M, N, K = 0.9, 1, 4, 2
GEO = {"spread": 4, "pairs": 2, "co-located": 1}


def tangency(x, m):
    """phi* per geography, the pairs tangency point r_P, and F_c(r_P) at phi*_pairs."""
    phis = {g: phi_star(x, m, N, K, c) for g, c in GEO.items()}
    r_p = float(largest_fixed_point(x, m, N, K, 2, phis["pairs"]))
    F_at = {g: float(F(r_p, x, m, N, K, c, phis["pairs"])) for g, c in GEO.items()}
    return phis, r_p, F_at


def other_cases():
    """Same check for other (m, x) with n = 4, k = 2: the hypothesis is sufficient, not necessary."""
    rows = []
    for m in (1, 2, 3):
        for x in (0.95, 1.0):
            phis, r_p, F_at = tangency(x, m)
            for g in ("spread", "co-located"):
                rows.append({"m": m, "x": x, "vs": g, "phi_pairs": phis["pairs"], "r_P": r_p,
                             "F_X_at_r_P": F_at[g], "phi_X": phis[g],
                             "hypothesis": bool(F_at[g] > r_p), "conclusion": bool(phis[g] > phis["pairs"])})
    return rows


def main():
    phis, r_p, F_at = tangency(X, M)
    phi_p = phis["pairs"]
    s_p, p_p = 1.0 - phi_p, X * r_p
    lo = float(derive()["p_minus"].subs(s_sym, sp.Float(s_p)))
    out = {
        "setting": {"x": X, "m": M, "n": N, "k": K},
        "phi_star": phis,
        "pairs_tangency": {"phi": phi_p, "s": s_p, "r_P": r_p, "p": p_p},
        "F_at_r_P": F_at,
        "hypothesis_holds": {g: bool(F_at[g] > F_at["pairs"]) for g in ("spread", "co-located")},
        "conclusion_holds": {g: bool(phis[g] > phi_p) for g in ("spread", "co-located")},
        "lemma_a_window_at_s": {"p_lo": lo, "p_hi": 2 / 3, "p_in_window": bool(lo < p_p < 2 / 3)},
        "other_cases_n4k2": other_cases(),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
