"""Numerical checks of the paper's theorems (brute force against the recursion in model.py)."""
from model import (dgm_er_Qc, jump_at_threshold, phi_star, phi_star_closed_form,
                   refinement_violations)


def test_thm1_abrupt_iff_km_ge_2():
    for (m, n, k) in [(1, 4, 2), (2, 4, 1), (2, 4, 2), (3, 4, 1), (1, 6, 3)]:
        assert jump_at_threshold(m, n, k) > 0.05
    assert jump_at_threshold(1, 4, 1) < 0.01


def test_thm2_closed_form():
    for (m, n, k, x) in [(2, 4, 1, .9), (2, 4, 2, .9), (3, 4, 2, .95), (2, 8, 2, .9), (3, 6, 3, 1.0), (1, 4, 2, .9)]:
        cf = phi_star_closed_form(x, m, n, k)
        assert abs(cf["spread"] - phi_star(x, m, n, k, n)) < 1e-4
        assert abs(cf["colocated"] - phi_star(x, m, n, k, 1)) < 1e-4


def test_thm2_m1_extremes_equal():
    assert abs(phi_star(0.9, 1, 4, 2, 1) - phi_star(0.9, 1, 4, 2, 4)) < 1e-4


def test_thm2_dead_network_returns_zero():
    assert phi_star_closed_form(0.5, 2, 4, 2) == {"spread": 0.0, "colocated": 0.0}   # x < x_crit = 0.831


def test_thm3_k1_monotone():
    for n in (4, 6, 8):
        for m in (1, 2, 3):
            for x in (0.6, 0.9, 1.0):
                assert refinement_violations(x, m, n, 1) == []


def test_prop4_trap_counterexample():
    a, b, c = (phi_star(0.9, 1, 4, 2, cc) for cc in (1, 2, 4))
    assert abs(a - 0.1946) < 1e-3 and abs(b - 0.1705) < 1e-3 and abs(c - 0.1946) < 1e-3
    assert any(v[:2] == (1, 2) for v in refinement_violations(0.95, 2, 6, 3))    # two-input trap


def test_refinement_prime_n():
    assert refinement_violations(0.9, 1, 5, 2) == []


def test_dgm_er_thresholds():
    assert abs(dgm_er_Qc(7, 10) - 0.0125) < 5e-4
    assert abs(dgm_er_Qc(2, 10) - 0.900) < 2e-3
