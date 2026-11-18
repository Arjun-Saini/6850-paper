"""A4: Theorem B's comparison step on the base case and a few other (m, x) for n = 4, k = 2.

Theorem B: if F_X(r_P) > r_P at phi = phi*_pairs (r_P = the pairs tangency point), then phi*_X > phi*_pairs.
Here: whenever the hypothesis holds, the conclusion must hold too."""
from model import F, largest_fixed_point, phi_star

GEO = {"spread": 4, "co-located": 1}


def check(x, m, n=4, k=2):
    phi_p = phi_star(x, m, n, k, 2)
    r_p = largest_fixed_point(x, m, n, k, 2, phi_p)
    out = {}
    for g, c in GEO.items():
        hyp = F(r_p, x, m, n, k, c, phi_p) > r_p
        out[g] = (bool(hyp), phi_star(x, m, n, k, c) > phi_p, r_p)
    return phi_p, out


def test_base_case():
    phi_p, out = check(0.9, 1)
    assert abs(phi_p - 0.1705) < 1e-4
    assert abs(out["spread"][2] - 0.6787) < 1e-4
    assert all(hyp and concl for hyp, concl, _ in out.values())


def test_hypothesis_implies_conclusion():
    for m in (1, 2, 3):
        for x in (0.95, 1.0):
            phi_p, out = check(x, m)
            if phi_p == 0:
                continue
            for hyp, concl, r_p in out.values():
                assert r_p > 0
                assert (not hyp) or concl
