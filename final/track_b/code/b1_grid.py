"""B1: reproduce the single-firm check of plan.md section 4 in code.

  1. Grid counts: on s in [0.5, 0.99] x p in [0.3, 0.99], how many points have an intermediate split strictly
     worse than both extremes. n = 4, k = 2 on a 50 x 70 grid (3500 points); the other (n, k) on 40 x 40
     (1600 points); k = 1 for each n, where Claim 3 says the count must be 0.
  2. The n = 4, k = 2 window at s = 0.6, 0.8, 0.9, 0.95: edges found numerically from cov(), next to
     Track A's closed form (A3).

The informal Nov 11 check did not record its exact grid spacing, so counts can differ slightly from plan.md's
754 / 283 / 606 / 83 / 543 / 222 / 616. The saved counts below are the ones to cite.

Usage:  python3 b1_grid.py      (writes ../results/b1_grid.json; seconds)
"""
import json
import os

import numpy as np

from coverage import interior_worst, lemma_a_window_n4k2, window_intervals

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "b1_grid.json")

S_RANGE, P_RANGE = (0.5, 0.99), (0.3, 0.99)
GRID_N4K2 = (50, 70)                        # (s points, p points) = 3500
GRID_OTHER = (40, 40)                       # 1600
OTHER_NK = [(6, 2), (6, 3), (8, 2), (8, 4), (12, 3), (12, 6)]
K1_N = [4, 6, 8, 12]
WINDOW_S = [0.6, 0.8, 0.9, 0.95]


def grid_count(n, k, shape):
    s = np.linspace(*S_RANGE, shape[0])
    p = np.linspace(*P_RANGE, shape[1])
    S_, P_ = np.meshgrid(s, p, indexing="ij")
    return int(interior_worst(S_, P_, k, n).sum()), int(S_.size)


def window_table():
    rows = []
    for s in WINDOW_S:
        num = window_intervals(s, c=2, k=2, n=4)
        cf = lemma_a_window_n4k2(s)
        rows.append(dict(s=s,
                         numeric=[list(map(float, iv)) for iv in num],
                         closed_form=None if cf is None else [float(cf[0]), float(cf[1])]))
    return rows


def main():
    counts = []
    count, total = grid_count(4, 2, GRID_N4K2)
    counts.append(dict(n=4, k=2, grid=list(GRID_N4K2), interior_worst=count, points=total))
    for n, k in OTHER_NK:
        count, total = grid_count(n, k, GRID_OTHER)
        counts.append(dict(n=n, k=k, grid=list(GRID_OTHER), interior_worst=count, points=total))
    for n in K1_N:
        count, total = grid_count(n, 1, GRID_OTHER)
        counts.append(dict(n=n, k=1, grid=list(GRID_OTHER), interior_worst=count, points=total))
    res = dict(
        definition="interior_worst: some c with 1 < c < n, c | n, has C_c(s, p) < min(C_1(s, p), C_n(s, p))",
        s_range=list(S_RANGE), p_range=list(P_RANGE), grid_spacing="numpy.linspace, endpoints included",
        counts=counts,
        window_n4k2=window_table(),
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    for r in counts:
        print(f"n={r['n']:2d} k={r['k']}: {r['interior_worst']} / {r['points']}")
    for r in res["window_n4k2"]:
        print(f"s={r['s']}: numeric {r['numeric']}  closed form {r['closed_form']}")


if __name__ == "__main__":
    main()
