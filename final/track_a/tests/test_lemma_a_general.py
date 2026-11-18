"""A5: the c = 2 identity and the general-c edge limits, against exploratory/code/model.py."""
from math import comb

import numpy as np

from lemma_a_general import S_EDGE, colocation_edge_limits, cov, p_hat_c2, roots
from model import S

P = np.linspace(0.01, 0.99, 99)


def test_c2_bracket_identity():
    for n in (4, 6, 8, 12):
        for k in range(1, n + 1):
            for s in (0.3, 0.7, 0.95):
                lhs = cov(2, n, k, s, P) - cov(1, n, k, s, P)
                rhs = s * (1 - s) * (2 * S(k, n // 2, P) - S(k, n, P))
                assert np.allclose(lhs, rhs, atol=1e-12)


def test_c2_root_regimes():
    assert abs(p_hat_c2(4, 2) - 2 / 3) < 1e-12
    for n in (4, 6, 8, 10, 12):
        assert p_hat_c2(n, 1) is None
        for k in range(n // 2 + 1, n + 1):
            assert p_hat_c2(n, k) is None
            assert np.all(cov(2, n, k, 0.8, P) < cov(1, n, k, 0.8, P))
        for k in range(2, n // 2 + 1):
            ph = p_hat_c2(n, k)
            assert 0 < ph < 1 and comb(n, k) > 2 * comb(n // 2, k)


def test_general_edge_between_limits_and_decreasing_in_s():
    for n in (6, 8, 10, 12):
        for c in (d for d in range(3, n) if n % d == 0):
            b = n // c
            for k in range(2, n - b + 1):
                lim0, lim1 = colocation_edge_limits(n, k, c)
                lim0 = 1.0 if lim0 is None else lim0
                edges = []
                for s in S_EDGE:
                    r = roots(lambda p, s=s: cov(c, n, k, s, p) - cov(1, n, k, s, p))
                    assert len(r) <= 1
                    edges.append(r[0] if r else 1.0)
                assert all(lim1 - 1e-9 <= e <= lim0 + 1e-9 for e in edges), (n, c, k)
                assert all(a >= b_ - 1e-12 for a, b_ in zip(edges, edges[1:])), (n, c, k)


def test_k_above_n_minus_b_always_worse_than_colocation():
    for n in (6, 8, 12):
        for c in (d for d in range(2, n) if n % d == 0):
            for k in range(n - n // c + 1, n + 1):
                for s in (0.5, 0.9):
                    assert np.all(cov(c, n, k, s, P) < cov(1, n, k, s, P))
