"""Single-firm coverage under regional shocks (task B1).

One firm, one input, n suppliers in c equal regional clusters of b = n / c. Each region survives
independently with probability s = 1 - phi, each supplier in a surviving region is usable
independently with probability p, and the input is covered iff at least k suppliers are usable:

  C_c(s, p) = sum_{j=0}^{c} Binom(j; c, s) * S_k(j b, p),      S_k(N, p) = P[Bin(N, p) >= k]

In the network, p = x * r. With m = 1 this is exactly exploratory/code/model.py's F(r, x, 1, n, k, c, phi)
at x = 1, r = p, phi = 1 - s (tests/test_track_b.py checks this).

"The intermediate split is worst" at (s, p) means some c strictly between 1 and n (c | n) has
C_c(s, p) < min(C_1(s, p), C_n(s, p)). For n = 4 the only such c is 2 (pairs), and the set of these
(s, p) is the single-firm reversal window of plan.md section 4.
"""
import os
import sys

import numpy as np
from scipy.optimize import brentq
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "exploratory", "code"))

from model import S  # noqa: E402  (P[Bin(N, p) >= k], zero when N < k)


def divisors(n):
    return [c for c in range(1, n + 1) if n % c == 0]


def cov(c, s, p, k=2, n=4):
    """Single-firm coverage C_c(s, p). Vectorized: s and p broadcast against each other."""
    if n % c:
        raise ValueError(f"c = {c} does not divide n = {n}")
    b = n // c
    s, p = np.broadcast_arrays(np.asarray(s, dtype=float), np.asarray(p, dtype=float))
    tot = np.zeros(s.shape)
    for j in range(c + 1):
        tot = tot + binom.pmf(j, c, s) * S(k, j * b, p)
    return tot


def extremes_min(s, p, k=2, n=4):
    """min(C_1, C_n): the better of co-location and full spreading is the bar an intermediate split must clear."""
    return np.minimum(cov(1, s, p, k, n), cov(n, s, p, k, n))


def interior_gap(c, s, p, k=2, n=4):
    """C_c - min(C_1, C_n). Negative exactly where the split into c clusters is strictly worse than both extremes."""
    return cov(c, s, p, k, n) - extremes_min(s, p, k, n)


def interior_worst(s, p, k=2, n=4):
    """True where some intermediate c (1 < c < n, c | n) is strictly worse than both extremes."""
    s, p = np.broadcast_arrays(np.asarray(s, dtype=float), np.asarray(p, dtype=float))
    out = np.zeros(s.shape, dtype=bool)
    for c in divisors(n)[1:-1]:
        out |= interior_gap(c, s, p, k, n) < 0
    return out


def window_intervals(s, c=2, k=2, n=4, num=4001):
    """The p-intervals in (0, 1) where cluster count c is strictly worse than both extremes, at a fixed s.

    Scans a fine p grid for sign changes of interior_gap and refines each edge with brentq.
    Returns a list of (p_lo, p_hi), empty when there is no window at this s."""
    ps = np.linspace(0.0, 1.0, num)[1:-1]            # coverage gaps vanish at p = 0 and p = 1
    g = interior_gap(c, s, ps, k, n)
    f = lambda q: float(interior_gap(c, s, q, k, n))
    neg = g < 0
    out, i = [], 0
    while i < len(ps):
        if not neg[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(ps) and neg[j + 1]:
            j += 1
        lo = brentq(f, ps[i - 1], ps[i], xtol=1e-14) if i > 0 else ps[0]
        hi = brentq(f, ps[j], ps[j + 1], xtol=1e-14) if j + 1 < len(ps) else ps[-1]
        out.append((lo, hi))
        i = j + 1
    return out


# ---------------------------------------------------------------- Track A's closed form (A3), for cross-checks
S_OPEN_N4K2 = (3 - np.sqrt(3)) / 2            # the n = 4, k = 2 window opens for s above this


def lemma_a_window_n4k2(s):
    """Track A's closed-form n = 4, k = 2 window (final/track_a/notes/lemma_a_n4k2.md on aryavardhan/track-a):
    pairs are strictly worst iff p_minus(s) < p < 2/3, p_minus(s) = 2 / (4 s + sqrt(2 s (5 s - 3))).
    Returns (p_minus, 2/3), or None where the window is empty (s <= (3 - sqrt 3) / 2)."""
    if s <= S_OPEN_N4K2:
        return None
    return 2.0 / (4.0 * s + np.sqrt(2.0 * s * (5.0 * s - 3.0))), 2.0 / 3.0
