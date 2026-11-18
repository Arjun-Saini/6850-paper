"""A7: the large-n limit formulas, and the finite-n ordering they predict, against exploratory/code/model.py."""
import numpy as np

from large_n import X, g, phi_star_limit
from model import phi_star

S_GRID = np.linspace(0.01, 0.99, 99)


def test_extremes_and_markov_bound():
    for m in (1, 2, 3):
        assert np.allclose([g(1, s, m) for s in S_GRID], S_GRID**m)
    for c in (2, 3, 4, 5, 10, 20):
        assert all(g(c, s, 1) < s for s in S_GRID)          # intermediate c strictly below spread (Markov)
        assert all(g(c, s, 2) < s for s in S_GRID)


def test_c2_closed_form():
    for alpha in (0.1, 0.3, 0.4):
        t = alpha / X
        s_star = min(np.sqrt(t), 1 - np.sqrt(1 - 2 * t))
        assert abs(phi_star_limit(2, alpha, X, 1) - (1 - s_star)) < 1e-8


def test_finite_n_ordering_m1():
    for n in (10, 20):
        k = round(0.4 * n)
        ext = phi_star(X, 1, n, k, 1)
        assert abs(ext - phi_star(X, 1, n, k, n)) < 1e-4
        assert phi_star(X, 1, n, k, 2) < ext and phi_star(X, 1, n, k, 5) < ext
