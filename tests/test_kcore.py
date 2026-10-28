"""k-core peeling: hand-checked graph and agreement with DGM's ER theory."""
import numpy as np

from kcore import clean_edges, core_numbers, er_edges, kcore_sizes
from model import dgm_er_core_size


def test_core_numbers_small():
    # triangle 0-1-2 plus pendant 3 on 0, isolated 4, a duplicate edge (1,0) and a self-loop (2,2)
    e = np.array([[0, 1], [1, 2], [2, 0], [0, 3], [1, 0], [2, 2]])
    assert core_numbers(5, clean_edges(e)).tolist() == [2, 2, 2, 1, 0]


def test_removed_vertices_have_core_zero():
    e = clean_edges(np.array([[0, 1], [1, 2], [2, 0]]))
    alive = np.array([True, True, False])
    assert core_numbers(3, e, alive).tolist() == [1, 1, 0]


def test_er_kcore_matches_dgm():
    rng = np.random.default_rng(1)
    N = 50_000
    e = er_edges(N, 10, rng)
    alive = rng.random(N) >= 0.10
    s = kcore_sizes(core_numbers(N, e, alive), range(3, 7))
    for k in range(3, 7):
        assert abs(s[k] - dgm_er_core_size(k, 0.90, 10)) < 0.01
