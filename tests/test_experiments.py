"""CLI parsing and threshold estimation for run_experiments.py (running experiments themselves is too slow for unit tests)."""
import numpy as np
import pytest

from run_experiments import selected_experiments, threshold_from_runs


def test_default_is_original_four():
    assert selected_experiments([]) == ["E1", "E2", "E3", "E4"]


def test_names_are_normalized_and_quick_ignored():
    assert selected_experiments(["e5", "E6", "--quick"]) == ["E5", "E6"]


def test_unknown_name_rejected():
    with pytest.raises(ValueError):
        selected_experiments(["E9"])


def test_threshold_ignores_order_of_tied_shocks():
    # realized shocks repeat (multiples of 1/G); the estimate must not depend on how ties are ordered
    phis = np.array([0.10, 0.10, 0.10, 0.12, 0.12, 0.14])
    col = np.array([False, True, False, True, False, True])
    base = threshold_from_runs(phis, col)
    rng = np.random.default_rng(0)
    for _ in range(20):
        o = rng.permutation(len(phis))
        assert threshold_from_runs(phis[o], col[o]) == base
    assert base[0] not in (0.10, 0.12)          # never splits inside a tie
