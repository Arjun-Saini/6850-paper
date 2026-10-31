"""CLI parsing and the E3/E5 tipping-point bisection (on a tiny network; full experiments are too slow for unit tests)."""
import numpy as np
import pytest

from run_experiments import collapses, critical_hits, nested_hit, selected_experiments
from simulate import simulate


def test_default_is_original_four():
    assert selected_experiments([]) == ["E1", "E2", "E3", "E4"]


def test_names_are_normalized_and_quick_ignored():
    assert selected_experiments(["e5", "E6", "--quick"]) == ["E5", "E6"]


def test_unknown_name_rejected():
    with pytest.raises(ValueError):
        selected_experiments(["E9"])



SMALL = dict(_exp="T", _guess=60, m=1, n=4, k=2, x=0.9, c=2, seed=3, depth=5, N=2000, G=200, balanced=True)


def test_nested_hits_grow_with_h():
    assert nested_hit(7, 5, 50).sum() == 5
    assert np.all(nested_hit(7, 5, 50) <= nested_hit(7, 9, 50))


def test_balanced_placement_is_exact():
    # with exactly N/G firms per region, hitting h regions removes exactly h/G of the bottom layer
    _, _, layers = simulate(m=1, n=4, k=2, c=1, depth=2, N=2000, G=200, balanced=True,
                            hit=nested_hit(0, 7, 200), return_layers=True)
    assert layers[0] == 1 - 7 / 200


def test_bisection_finds_exact_tipping_point():
    h = critical_hits(SMALL)["h_crit"]
    assert 0 < h < SMALL["G"]
    assert collapses(SMALL, h) and not collapses(SMALL, h - 1)
