"""Coverage and tipping points for suppliers in clusters of ARBITRARY sizes (Track A).

exploratory/code/model.py only allows c equal clusters (c | n). Here a geography is a tuple of
cluster sizes, e.g. (3, 1) or (2, 1, 1). Each cluster sits in its own region, hit independently
with probability phi; a surviving supplier is usable with probability p = x * r.

  coverage(sizes, s, p, k) = P[# usable suppliers >= k],   s = 1 - phi
  F(r) = coverage(sizes, 1 - phi, x r, k) ** m             (same recursion as model.F)

With equal sizes these reduce to model.F (checked in tests/test_partition_coverage.py).
"""
import numpy as np
from scipy.stats import binom

GRID = np.linspace(1e-6, 1.0, 200_001)    # same grid as model.py


def coverage(sizes, s, p, k):
    """P[at least k usable suppliers], vectorized over p. Convolves the clusters' usable counts."""
    p = np.asarray(p, dtype=float)
    n = sum(sizes)
    dist = np.zeros((n + 1,) + p.shape)       # dist[j] = P[j usable so far]
    dist[0] = 1.0
    used = 0
    for b in sizes:
        new = np.zeros_like(dist)
        for j in range(used + 1):
            new[j] += (1.0 - s) * dist[j]     # region hit: the cluster adds nothing
            for i in range(b + 1):
                new[j + i] += s * binom.pmf(i, b, p) * dist[j]
        dist, used = new, used + b
    return dist[k:].sum(axis=0)


def F(r, x, m, sizes, k, phi):
    return coverage(sizes, 1.0 - phi, x * np.asarray(r, dtype=float), k) ** m


def largest_fixed_point(x, m, sizes, k, phi):
    """Largest root of F(r) = r on (0, 1]; 0 if none. Same method as model.largest_fixed_point."""
    g = F(GRID, x, m, sizes, k, phi) - GRID
    pos = np.flatnonzero(g >= 0)
    if len(pos) == 0:
        return 0.0
    i = pos[-1]
    if i == len(GRID) - 1:
        return 1.0
    lo, hi = GRID[i], GRID[i + 1]
    for _ in range(50):
        mid = 0.5 * (lo + hi)
        if F(mid, x, m, sizes, k, phi) - mid >= 0:
            lo = mid
        else:
            hi = mid
    r = 0.5 * (lo + hi)
    return r if r > 1e-4 else 0.0


def phi_star(x, m, sizes, k, tol=1e-6):
    """Largest regional shock probability the deep network survives (r* > 0)."""
    if largest_fixed_point(x, m, sizes, k, 0.0) == 0:
        return 0.0
    lo, hi = 0.0, 1.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if largest_fixed_point(x, m, sizes, k, mid) > 0:
            lo = mid
        else:
            hi = mid
    return lo


def partitions(n, max_part=None):
    """All partitions of n as non-increasing tuples."""
    max_part = n if max_part is None else max_part
    if n == 0:
        return [()]
    return [(a,) + rest for a in range(min(n, max_part), 0, -1) for rest in partitions(n - a, a)]


def refines(fine, coarse):
    """True if the parts of `fine` can be grouped to give `coarse` (fine is a refinement)."""
    if len(fine) < len(coarse) or sum(fine) != sum(coarse):
        return False

    def place(i, room):
        if i == len(fine):
            return all(r == 0 for r in room)
        for j in range(len(room)):
            if room[j] >= fine[i]:
                room[j] -= fine[i]
                if place(i + 1, room):
                    return True
                room[j] += fine[i]
        return False

    return place(0, list(coarse))
