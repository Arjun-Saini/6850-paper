"""CLI parsing for run_experiments.py (running experiments themselves is too slow for unit tests)."""
import pytest

from run_experiments import selected_experiments


def test_default_is_original_four():
    assert selected_experiments([]) == ["E1", "E2", "E3", "E4"]


def test_names_are_normalized_and_quick_ignored():
    assert selected_experiments(["e5", "E6", "--quick"]) == ["E5", "E6"]


def test_unknown_name_rejected():
    with pytest.raises(ValueError):
        selected_experiments(["E9"])
