# tests/examples/test_scenarios.py
"""Module to test tessifs scenario examples."""
from tessif_examples import scenarios


def test_generic_grid():
    """Test mwe creation."""
    esys = scenarios.create_generic_grid()
    assert esys.uid == "Generic_Grid"
