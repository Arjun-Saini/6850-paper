"""Track B checks. Fast by default; the full B2 scan runs only with RUN_SLOW=1 (about 10-15 minutes)."""
import os

import numpy as np
import pytest

from coverage import cov, divisors, interior_worst, lemma_a_window_n4k2, window_intervals
from model import F, S

S_GRID = np.linspace(0.5, 0.99, 25)
P_GRID = np.linspace(0.05, 0.99, 25)
SS, PP = np.meshgrid(S_GRID, P_GRID)


# ------------------------------------------------------------------ B1: cov()
@pytest.mark.parametrize("n,k", [(2, 1), (2, 2), (4, 1), (4, 2), (4, 3), (6, 2), (6, 3), (8, 4), (12, 3)])
def test_cov_matches_model_F(n, k):
    """cov(c, s, p) is the exploratory recursion with m = 1, x = 1, r = p, phi = 1 - s."""
    for c in divisors(n):
        for s in (0.55, 0.8, 0.97):
            np.testing.assert_allclose(cov(c, s, P_GRID, k, n), F(P_GRID, 1.0, 1, n, k, c, 1.0 - s),
                                       rtol=0, atol=1e-13)


def test_cov_n4_closed_forms():
    """plan.md section 4: spread S_k(n, s p); co-located s S_k(n, p); pairs s^2 S_2(4, p) + 2 s phi S_2(2, p)."""
    phi = 1 - SS
    np.testing.assert_allclose(cov(4, SS, PP), S(2, 4, SS * PP), atol=1e-13)
    np.testing.assert_allclose(cov(1, SS, PP), SS * S(2, 4, PP), atol=1e-13)
    np.testing.assert_allclose(cov(2, SS, PP), SS**2 * S(2, 4, PP) + 2 * SS * phi * S(2, 2, PP), atol=1e-13)


def test_cov_bounds_and_monotone():
    for n, k in [(4, 2), (6, 3), (8, 2)]:
        for c in divisors(n):
            v = cov(c, SS, PP, k, n)
            assert np.all((v >= -1e-15) & (v <= 1 + 1e-15))
            assert np.all(np.diff(v, axis=0) >= -1e-13)   # rows: increasing p
            assert np.all(np.diff(v, axis=1) >= -1e-13)   # columns: increasing s


def test_cov_rejects_non_divisor():
    with pytest.raises(ValueError):
        cov(3, 0.9, 0.5, 2, 4)


@pytest.mark.parametrize("n", [2, 4, 6, 8, 12])
def test_k1_interior_never_worst(n):
    """Claim 3: with k = 1 no intermediate split is worse than both extremes."""
    assert not interior_worst(SS, PP, k=1, n=n).any()


def test_upper_edge_two_thirds():
    """At p = 2/3, S_2(4, p) = 2 p^2 (72/81), so pairs and co-location tie for every s."""
    assert float(S(2, 4, 2 / 3)) == pytest.approx(72 / 81, abs=1e-14)
    for s in (0.7, 0.85, 0.95):
        assert float(cov(2, s, 2 / 3) - cov(1, s, 2 / 3)) == pytest.approx(0, abs=1e-14)


@pytest.mark.parametrize("s", [0.65, 0.7, 0.8, 0.83, 0.9, 0.95, 0.99])
def test_window_matches_track_a_closed_form(s):
    num = window_intervals(s, c=2, k=2, n=4)
    lo, hi = lemma_a_window_n4k2(s)
    assert len(num) == 1
    assert num[0][0] == pytest.approx(lo, abs=1e-10)
    assert num[0][1] == pytest.approx(hi, abs=1e-10)


@pytest.mark.parametrize("s", [0.5, 0.6, 0.63])
def test_window_empty_below_opening(s):
    assert lemma_a_window_n4k2(s) is None
    assert window_intervals(s, c=2, k=2, n=4) == []


def test_window_plan_table():
    """plan.md section 4 table: lower edges about 0.448 / 0.382 / 0.356 at s = 0.8 / 0.9 / 0.95, none at 0.6."""
    for s, lo in [(0.8, 0.448), (0.9, 0.382), (0.95, 0.356)]:
        (a, b), = window_intervals(s, c=2, k=2, n=4)
        assert a == pytest.approx(lo, abs=1e-3)
        assert b == pytest.approx(2 / 3, abs=1e-10)


# ------------------------------------------------------------------ B2: Theorem B on single settings
def test_b2_base_case():
    """n = 4, k = 2, m = 1, x = 0.9: phi* 0.1946 / 0.1705 / 0.1946 and the pairs tipping point in the window."""
    from b2_settings import analyze
    r = analyze(4, 2, 1, 0.9)
    assert r["phi_star"]["4"] == pytest.approx(0.1946, abs=1e-4)
    assert r["phi_star"]["2"] == pytest.approx(0.1705, abs=1e-4)
    assert r["phi_star"]["1"] == pytest.approx(0.1946, abs=1e-4)
    assert r["r_tip"]["2"] == pytest.approx(0.6787, abs=1e-3)
    assert r["active"] and r["reversal"] and r["predicted"]
    pq = {(q["c"], q["c2"]): q for q in r["pairs"]}
    assert pq[(1, 2)]["reversal"] and pq[(1, 2)]["hypothesis"]
    assert not pq[(2, 4)]["reversal"] and not pq[(2, 4)]["hypothesis"]
    # Track A's numbers at the pairs tangency: F_coloc(r_P) = 0.6910; the margin is F_coloc - r_P
    assert pq[(1, 2)]["cov_margin"] == pytest.approx(0.6910 - 0.6787, abs=1e-3)
    (inter,) = r["interior"]
    assert inter["network_worst"] and inter["firm_worst"] and inter["in_lemma_a_window"]
    # Theorem B: hypothesis implies reversal, pair by pair
    assert all(q["reversal"] for q in r["pairs"] if q["hypothesis"])


def test_b2_reversal_without_hypothesis_track_a_example():
    """Track A's example: n = 4, k = 2, m = 1, x = 1 vs co-location reverses without the strict hypothesis.

    The pairs tipping point is exactly (s, p) = (3/4, 2/3), on the window's upper edge, where pairs and
    co-location tie (Track A quoted p = 0.6677, from a looser phi* tolerance)."""
    from b2_settings import analyze
    r = analyze(4, 2, 1, 1.0)
    q = next(q for q in r["pairs"] if (q["c"], q["c2"]) == (1, 2))
    assert q["reversal"] and not q["hypothesis"]
    assert q["p2"] == pytest.approx(2 / 3, abs=1e-4)
    assert q["phi_c2"] == pytest.approx(0.25, abs=1e-6)
    assert q["phi_c"] == pytest.approx(0.2752, abs=1e-3)


def test_pairs_x1_exact_tangency():
    """At x = 1, s = 3/4, p = 2/3: pairs coverage C_2 = p and dC_2/dp = 1, so phi*_pairs = 1/4 exactly."""
    s, p, h = 0.75, 2 / 3, 1e-6
    assert float(cov(2, s, p)) == pytest.approx(p, abs=1e-14)
    assert float((cov(2, s, p + h) - cov(2, s, p - h)) / (2 * h)) == pytest.approx(1.0, abs=1e-8)
    assert float(cov(1, s, p)) == pytest.approx(p, abs=1e-14)   # co-location ties there too


def test_b2_k1_never_reverses():
    from b2_settings import analyze
    r = analyze(4, 1, 2, 0.9)
    assert not r["reversal"] and not r["predicted"]


def test_b2_summary_logic():
    """summarize() on hand-made rows: counts and the two mismatch lists."""
    from b2_settings import summarize

    def pair(rev, hyp):
        return dict(c=1, c2=2, phi_c=0.2, phi_c2=0.1, phi_gap=0.1, reversal=rev, applicable=True,
                    s2=0.9, p2=0.6, r2=0.67, cov_margin=0.01 if hyp else -0.01, hypothesis=hyp)

    def row(active, pairs):
        return dict(n=4, k=2, m=1, x=0.9, active=active, reversal=any(p["reversal"] for p in pairs),
                    predicted=any(p["hypothesis"] for p in pairs), pairs=pairs, interior=[])

    rows = [row(True, [pair(True, True)]), row(True, [pair(True, False)]), row(True, [pair(False, False)]),
            row(False, [pair(True, True)])]
    s = summarize(rows)
    assert (s["settings_k_ge_2"], s["active"], s["reversal"], s["predicted"]) == (4, 3, 2, 1)
    assert s["reversal_not_predicted"] == 1 and s["predicted_not_reversal"] == 0
    assert len(s["pairs_reversal_without_hypothesis"]) == 1
    assert s["pairs_hypothesis_without_reversal"] == []


def test_b2_grid_matches_trap_scan():
    """B2 scans the same settings as the exploratory trap scan (k >= 2 part)."""
    import json
    from b2_settings import settings
    here = os.path.dirname(os.path.abspath(__file__))
    scan = json.load(open(os.path.join(here, "..", "..", "..", "exploratory", "results", "trap_scan.json")))
    want = sorted((r["n"], r["k"], r["m"], r["x"]) for r in scan if r["k"] >= 2)
    assert sorted(settings()) == want
    assert sum(1 for r in scan if r["k"] >= 2 and r["violations"]) == 72


@pytest.mark.skipif(os.environ.get("RUN_SLOW") != "1", reason="full B2 scan; set RUN_SLOW=1")
def test_b2_full_scan_counts():
    """The paper's 72 of 109, and Theorem B's implication on every pair."""
    from b2_settings import analyze, settings, summarize
    s = summarize([analyze(*st) for st in settings()])
    assert s["active"] == 109
    assert s["reversal"] == 72
    assert s["pairs_hypothesis_without_reversal"] == []


# ------------------------------------------------------------------ B3: key figure (small grid)
def test_b3_figure_builds_and_pairs_tip_in_window(tmp_path):
    from b3_key_figure import build
    tips = build(fig_path=str(tmp_path / "f.pdf"), res_path=str(tmp_path / "p.json"), n_phi=6, n_grid=60)
    assert (tmp_path / "f.pdf").stat().st_size > 0
    by_c = {t["c"]: t for t in tips}
    assert by_c[2]["in_window"]
    assert by_c[2]["phi_star"] < min(by_c[1]["phi_star"], by_c[4]["phi_star"])
    lo, hi = lemma_a_window_n4k2(by_c[2]["s"])
    assert lo < by_c[2]["p"] < hi
