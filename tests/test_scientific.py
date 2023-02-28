"""Test scientific examples."""

from tessif_examples import scientific


def test_basic_examples():
    """Test succesfull system model creation."""
    hhes = scientific.create_hamburg_inspired_hnp_msc()

    assert hhes
