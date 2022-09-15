# tests/examples/test_scenarios.py
"""Module to test tessifs scenario examples."""
from tessif_examples import scenarios


def test_generic_grid():
    """Test mwe creation."""
    esys = scenarios.create_generic_grid()
    assert esys.uid == "Generic_Grid"
def test_hhes():
    """Test mwe creation."""
    esys = scenarios.create_hhes()
    assert esys.uid == "Generic_Grid"
def test_grid_es():
    """Test mwe creation."""
    esys = scenarios.create_grid_es()
    assert esys.uid == "Generic_Grid"
def test_component_es():
    """Test mwe creation."""
    esys = scenarios.create_component_es()
    assert esys.uid == "Generic_Grid"
def test_grid_kp_es():
    """Test mwe creation."""
    esys = scenarios.create_grid_kp_es()
    assert esys.uid == "Generic_Grid"
def test_grid_cs_es():
    """Test mwe creation."""
    esys = scenarios.create_grid_cs_es()
    assert esys.uid == "Generic_Grid"
def test_grid_cp_es():
    """Test mwe creation."""
    esys = scenarios.create_grid_cp_es()
    assert esys.uid == "Generic_Grid"
def test_grid_ts_es():
    """Test mwe creation."""
    esys = scenarios.create_grid_ts_es()
    assert esys.uid == "Generic_Grid"
def test_grid_tp_es():
    """Test mwe creation."""
    esys = scenarios.create_grid_tp_es()
    assert esys.uid == "Generic_Grid"