# tests/examples/test_basic.py
"""Module to test tessifs basic examples."""
from tessif_examples import basic


def test_mwe():
    """Test mwe creation."""
    esys = basic.create_mwe()
    assert esys.uid == "Minimum_Working_Example"
