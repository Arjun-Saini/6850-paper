"""A3: the closed-form n = 4, k = 2 window against brute force on exploratory/code/model.py.

With m = 1, x = 1 and r = p, model.F(r, x, 1, 4, 2, c, phi) is the single-firm coverage C_c(1 - phi, p)."""
import numpy as np
import sympy as sp

from lemma_a_n4k2 import C1, C2, C4, derive, p, s
from model import F

D = derive()
P_GRID = np.linspace(0.01, 0.99, 981)


def cov(c, sv, pv):
    return F(pv, 1.0, 1, 4, 2, c, 1.0 - sv)


def test_symbolic_coverage_matches_model():
    for sv in (0.55, 0.7, 0.9):
        for c, C in ((1, C1), (2, C2), (4, C4)):
            f = sp.lambdify(p, C.subs(s, sv))
            assert np.allclose(f(P_GRID), cov(c, sv, P_GRID), atol=1e-12)


def test_window_edges_match_brute_force():
    lo_f = sp.lambdify(s, D["p_minus"])
    for sv in np.linspace(0.64, 0.99, 36):
        worst = cov(2, sv, P_GRID) < np.minimum(cov(1, sv, P_GRID), cov(4, sv, P_GRID))
        expected = (P_GRID > lo_f(sv)) & (P_GRID < 2 / 3)
        assert np.array_equal(worst, expected), sv


def test_no_window_below_s_open():
    s_open = float(D["s_open"])
    for sv in np.linspace(0.5, s_open - 1e-3, 20):
        worst = cov(2, sv, P_GRID) < np.minimum(cov(1, sv, P_GRID), cov(4, sv, P_GRID))
        assert not worst.any(), sv


def test_upper_root_of_g_stays_above_two_thirds():
    hi_f = sp.lambdify(s, D["p_plus"])
    assert all(hi_f(sv) > 2 / 3 for sv in np.linspace(0.6, 0.999, 200))
