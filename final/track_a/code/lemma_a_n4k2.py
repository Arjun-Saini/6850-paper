"""Lemma A for n = 4, k = 2: closed-form edges of the single-firm reversal window (task A3).

Single firm, 4 suppliers in c equal clusters, each region survives with probability s = 1 - phi,
each surviving supplier is usable with probability p, the input is covered iff >= 2 are usable:

  co-located (c = 1):  C1 = s * S2(4, p)
  pairs      (c = 2):  C2 = s^2 * S2(4, p) + 2 s (1 - s) * p^2
  spread     (c = 4):  C4 = S2(4, s p)                       S2(N, p) = P[Bin(N, p) >= 2]

The window is the set of (s, p) where pairs are strictly worst: C2 < min(C1, C4).
sympy derives both edges and the smallest s at which the window opens.

Usage:  python3 lemma_a_n4k2.py      (writes ../results/lemma_a_n4k2.json)
"""
import json
import os

import sympy as sp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "lemma_a_n4k2.json")
s, p = sp.symbols("s p", positive=True)
S_TABLE = (0.6, 0.8, 0.9, 0.95)   # the s values of the plan.md section 4 table


def S2(N, q):
    """P[Bin(N, q) >= 2] as a polynomial."""
    return sp.expand(1 - (1 - q) ** N - N * q * (1 - q) ** (N - 1))


C1 = s * S2(4, p)
C2 = s**2 * S2(4, p) + 2 * s * (1 - s) * p**2
C4 = S2(4, s * p)


def derive():
    # upper edge (pairs vs co-located): C2 - C1 = s(1 - s) [2p^2 - S2(4, p)], free of s
    bracket = sp.factor(sp.cancel((C2 - C1) / (s * (1 - s))))
    assert sp.expand(bracket - (2 * p**2 - S2(4, p))) == 0
    upper_roots = [r for r in sp.solve(bracket, p) if r.is_real and 0 < r < 1]
    assert upper_roots == [sp.Rational(2, 3)]
    p_upper = upper_roots[0]

    # lower edge (pairs vs spread): C2 - C4 = s(1 - s) p^2 g(s, p), g quadratic in p
    g = sp.expand(sp.cancel((C2 - C4) / (s * (1 - s) * p**2)))
    assert sp.expand(g - (3 * s * (1 + s) * p**2 - 8 * s * p + 2)) == 0
    disc = sp.factor(sp.discriminant(g, p))                    # 8 s (5s - 3): real roots iff s >= 3/5
    p_minus = 2 / (4 * s + sp.sqrt(2 * s * (5 * s - 3)))       # smaller root, rationalized
    p_plus = (4 * s + sp.sqrt(2 * s * (5 * s - 3))) / (3 * s * (1 + s))
    for root in (p_minus, p_plus):
        assert sp.simplify(g.subs(p, root)) == 0

    # the window opens when the lower edge drops below 2/3: g(s, 2/3) < 0
    s_open = [r for r in sp.solve(g.subs(p, p_upper), s) if 0 < r < 1]
    assert len(s_open) == 1
    s_open = sp.nsimplify(s_open[0])
    return dict(bracket=bracket, g=g, disc=disc, p_upper=p_upper, p_minus=p_minus,
                p_plus=p_plus, s_open=s_open)


def main():
    d = derive()
    table = []
    for sv in S_TABLE:
        lo = float(d["p_minus"].subs(s, sv)) if sv >= 0.6 else None
        hi = float(d["p_upper"])
        table.append({"s": sv, "p_lo": lo, "p_hi": hi, "open": lo is not None and lo < hi})
    out = {
        "setting": {"n": 4, "k": 2, "c_compared": [1, 2, 4]},
        "upper_edge": {"vs": "co-located", "p": str(d["p_upper"]), "p_float": float(d["p_upper"]),
                       "bracket": str(d["bracket"]), "note": "C2 - C1 = s(1-s)*bracket; edge does not depend on s"},
        "lower_edge": {"vs": "spread", "p_minus": str(d["p_minus"]), "p_plus": str(d["p_plus"]),
                       "g": str(d["g"]), "discriminant": str(d["disc"]),
                       "note": "C2 - C4 = s(1-s)p^2*g; pairs < spread iff p_minus < p < p_plus (needs s >= 3/5)"},
        "window": "p_minus(s) < p < 2/3, nonempty iff s > s_open",
        "s_open": {"exact": str(d["s_open"]), "float": float(d["s_open"])},
        "p_minus_limit_s_to_1": str(sp.limit(d["p_minus"], s, 1)),
        "table": table,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
