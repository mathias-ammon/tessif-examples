"""Test basic examples."""

from tessif_examples import basic


def test_basic_examples():
    """Test succesfull system model creation."""
    mwe = basic.create_mwe()

    assert mwe
