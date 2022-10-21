# tests/examples/test_scenarios.py
"""Module to test tessifs scenario examples."""
from tessif_examples import scenarios


def test_generic_grid():
    """Test generic_grid creation."""
    esys = scenarios.create_generic_grid()
    assert esys.uid == "Generic_Grid"


def test_hhes():
    """Test hhes creation."""
    esys = scenarios.create_hhes()
    assert esys.uid == "Energy System Hamburg"


def test_grid_es():
    """Test grid_es creation."""
    esys = scenarios.create_grid_es()
    assert esys.uid == "my_energy_system"


def test_component_es():
    """Test component_es creation."""
    esys = scenarios.create_component_es()
    assert esys.uid == "Component_es"


def test_grid_kp_es():
    """Test grid_kp_es creation."""
    esys = scenarios.create_grid_kp_es()
    assert esys.uid == 'Energy System Grid "Kupferplatte"'


def test_grid_cs_es():
    """Test grid_cs_es creation."""
    esys = scenarios.create_grid_cs_es()
    assert esys.uid == "Energy System Grid Connectors and Storage"


def test_grid_cp_es():
    """Test grid_cp_es creation."""
    esys = scenarios.create_grid_cp_es()
    assert esys.uid == "Energy System Grid Connectors and Powersource/-sink"


def test_grid_ts_es():
    """Test grid_ts_es creation."""
    esys = scenarios.create_grid_ts_es()
    assert esys.uid == "Energy System Grid Transformers and Storages"


def test_grid_tp_es():
    """Test grid_tp_es creation."""
    esys = scenarios.create_grid_tp_es()
    assert esys.uid == "Energy System Grid Transformers and Powersources/-sinks"


def test_losslc_es():
    """Test losslc_es creation."""
    esys = scenarios.create_losslc_es()
    assert esys.uid == "LossLC"