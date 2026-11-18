"""B2: test Theorem B's condition on every setting of the exploratory paper's grid search.

The grid is the exploratory trap scan (exploratory/code/make_figures.py): n in {2, 4, 6, 8}, k = 1..n,
m in {1, 2, 3}, x in {0.6, 0.7, 0.8, 0.9, 0.95, 1.0}. The paper counts the k >= 2 settings where some
geography tolerates a shock (max_c phi*_c > 0): 109. A setting shows a network reversal when some refinement
c | c2 has phi*_c > phi*_c2 + 1e-4 (model.refinement_violations): 72 of the 109.

For each refinement pair (c, c2) the finer geography c2 is the candidate loser. Theorem B
(final/track_a/notes/theorem_b.md) says: let phi_2 = phi*_c2, r_2 = r*_c2(phi_2) > 0 its reliability at the
tipping point, s_2 = 1 - phi_2 and p_2 = x r_2. If C_c(s_2, p_2) > C_c2(s_2, p_2), then phi*_c > phi*_c2.
So "hypothesis holds" must imply "reversal". The converse can fail (Track A: n = 4, k = 2, m = 1, x = 1 against
co-location), so every reversal without the hypothesis is listed with how far it misses.

Per setting it also records the plan.md section 4 notion: whether an intermediate c is worst in the network
(phi*_c < min(phi*_1, phi*_n) - 1e-4) and, at that c's tipping point, in the single firm
(C_c < min(C_1, C_n)). For n = 4, k = 2 it adds Track A's closed-form window test at the pairs tipping point.

Usage:  python3 b2_settings.py      (writes ../results/b2_settings.json; slow, about 10-15 minutes)
"""
import json
import os
import sys
import time

import numpy as np

from coverage import cov, divisors, extremes_min, lemma_a_window_n4k2
from model import largest_fixed_point, phi_star

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "b2_settings.json")

NS, MS, XS = (2, 4, 6, 8), (1, 2, 3), (0.6, 0.7, 0.8, 0.9, 0.95, 1.0)
REV_TOL = 1e-4        # same tolerance as model.refinement_violations, so the 72 is the paper's 72
PHI_TOL = 1e-9        # tipping points to 1e-9, so r at the tipping point is close to the tangency value
HYP_EPS = 1e-9        # coverage margin must exceed this to count as "hypothesis holds" (ties are not strict)


def settings(k_min=2):
    return [(n, k, m, x) for n in NS for k in range(k_min, n + 1) for m in MS for x in XS]


def analyze(n, k, m, x):
    """Everything B2 needs for one setting."""
    cs = divisors(n)
    ps = {c: phi_star(x, m, n, k, c, tol=PHI_TOL) for c in cs}
    rs = {c: largest_fixed_point(x, m, n, k, c, ps[c]) for c in cs}
    active = max(ps.values()) > 0

    pairs = []
    for c in cs:
        for c2 in cs:
            if not (c < c2 and c2 % c == 0):
                continue
            s2, p2 = 1.0 - ps[c2], x * rs[c2]
            applicable = rs[c2] > 0
            margin = float(cov(c, s2, p2, k, n) - cov(c2, s2, p2, k, n)) if applicable else None
            pairs.append(dict(
                c=c, c2=c2, phi_c=ps[c], phi_c2=ps[c2], phi_gap=ps[c] - ps[c2],
                reversal=ps[c] > ps[c2] + REV_TOL,
                applicable=applicable, s2=s2, p2=p2, r2=rs[c2],
                cov_margin=margin, hypothesis=applicable and margin > HYP_EPS,
            ))

    # plan.md section 4 notion: an intermediate split worst of all three (network and single firm)
    interior = []
    for c in cs[1:-1]:
        s_c, p_c = 1.0 - ps[c], x * rs[c]
        net = ps[c] < min(ps[1], ps[n]) - REV_TOL
        firm_gap = float(cov(c, s_c, p_c, k, n) - extremes_min(s_c, p_c, k, n)) if rs[c] > 0 else None
        entry = dict(c=c, network_worst=net, s=s_c, p=p_c, firm_gap=firm_gap,
                     firm_worst=firm_gap is not None and firm_gap < -HYP_EPS)
        if (n, k, c) == (4, 2, 2):
            w = lemma_a_window_n4k2(s_c)
            entry["lemma_a_window"] = None if w is None else [float(w[0]), float(w[1])]
            entry["in_lemma_a_window"] = w is not None and w[0] < p_c < w[1]
        interior.append(entry)

    return dict(n=n, k=k, m=m, x=x, phi_star={str(c): ps[c] for c in cs}, r_tip={str(c): rs[c] for c in cs},
                active=active, reversal=any(q["reversal"] for q in pairs),
                predicted=any(q["hypothesis"] for q in pairs), pairs=pairs, interior=interior)


def summarize(rows):
    act = [r for r in rows if r["active"]]
    all_pairs = [(r, q) for r in act for q in r["pairs"]]
    hyp_no_rev = [(r, q) for r, q in all_pairs if q["hypothesis"] and not q["reversal"]]
    rev_no_hyp = [(r, q) for r, q in all_pairs if q["reversal"] and not q["hypothesis"]]

    def brief(r, q):
        return dict(n=r["n"], k=r["k"], m=r["m"], x=r["x"], c=q["c"], c2=q["c2"], phi_gap=q["phi_gap"],
                    s2=q["s2"], p2=q["p2"], cov_margin=q["cov_margin"], applicable=q["applicable"])

    inter = [(r, e) for r in act for e in r["interior"]]
    return dict(
        settings_k_ge_2=len(rows),
        active=len(act),
        reversal=sum(r["reversal"] for r in act),
        predicted=sum(r["predicted"] for r in act),
        predicted_and_reversal=sum(r["predicted"] and r["reversal"] for r in act),
        reversal_not_predicted=sum(r["reversal"] and not r["predicted"] for r in act),
        predicted_not_reversal=sum(r["predicted"] and not r["reversal"] for r in act),
        pairs_total=len(all_pairs),
        pairs_hypothesis=sum(q["hypothesis"] for _, q in all_pairs),
        pairs_reversal=sum(q["reversal"] for _, q in all_pairs),
        # Theorem B says this list must be empty; any entry is a bug or a numerical edge case to inspect
        pairs_hypothesis_without_reversal=[brief(r, q) for r, q in hyp_no_rev],
        # the hypothesis is only sufficient: these are the reversals it does not explain
        pairs_reversal_without_hypothesis=[brief(r, q) for r, q in rev_no_hyp],
        interior_network_worst=sum(e["network_worst"] for _, e in inter),
        interior_network_worst_and_firm_worst=sum(e["network_worst"] and e["firm_worst"] for _, e in inter),
        interior_firm_worst_not_network_worst=sum(e["firm_worst"] and not e["network_worst"] for _, e in inter),
    )


def main():
    t0 = time.time()
    rows = []
    todo = settings()
    for i, st in enumerate(todo):
        rows.append(analyze(*st))
        print(f"[{i + 1}/{len(todo)}] n={st[0]} k={st[1]} m={st[2]} x={st[3]}  "
              f"reversal={rows[-1]['reversal']} predicted={rows[-1]['predicted']}  ({time.time() - t0:.0f}s)",
              file=sys.stderr)
    summary = summarize(rows)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(dict(grid=dict(n=NS, m=MS, x=XS, k="2..n"), tolerances=dict(reversal=REV_TOL, phi=PHI_TOL,
                       hypothesis=HYP_EPS), summary=summary, settings=rows), f, indent=1)
    print(json.dumps({k: v for k, v in summary.items() if not isinstance(v, list)}, indent=1))
    print(f"hypothesis without reversal: {len(summary['pairs_hypothesis_without_reversal'])} (Theorem B: must be 0)")
    print(f"reversal without hypothesis: {len(summary['pairs_reversal_without_hypothesis'])}")


if __name__ == "__main__":
    main()
