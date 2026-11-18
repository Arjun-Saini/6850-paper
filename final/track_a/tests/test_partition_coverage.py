"""partition_coverage.py against exploratory/code/model.py (equal clusters) and against the k = 1 closed form."""
import numpy as np

import model
from partition_coverage import F, coverage, partitions, phi_star, refines

R = np.linspace(0.0, 1.0, 101)


def test_equal_clusters_match_model():
    for n, k in [(4, 1), (4, 2), (6, 3), (8, 2)]:
        for c in (c for c in range(1, n + 1) if n % c == 0):
            for x, m, phi in [(0.9, 1, 0.2), (0.7, 2, 0.5), (1.0, 3, 0.05)]:
                ours = F(R, x, m, (n // c,) * c, k, phi)
                assert np.allclose(ours, model.F(R, x, m, n, k, c, phi), atol=1e-12)


def test_phi_star_matches_model():
    for c in (1, 2, 4):
        assert abs(phi_star(0.9, 1, (4 // c,) * c, 2) - model.phi_star(0.9, 1, 4, 2, c)) < 1e-5


def test_k1_unequal_closed_form():
    rng = np.random.default_rng(1)
    for sizes in [(3, 1), (2, 1, 1), (4, 2), (5, 2, 1)]:
        s, p = rng.random(10), rng.random(10)
        closed = 1 - np.prod([(1 - s) + s * (1 - p) ** b for b in sizes], axis=0)
        assert np.allclose([coverage(sizes, si, pi, 1) for si, pi in zip(s, p)], closed, atol=1e-12)


def test_partitions_and_refines():
    assert len(partitions(6)) == 11
    assert refines((2, 1, 1), (3, 1)) and refines((2, 1, 1), (2, 2))
    assert not refines((2, 2), (3, 1)) and not refines((3, 1), (2, 2))
    assert not refines((3, 3), (4, 2))
