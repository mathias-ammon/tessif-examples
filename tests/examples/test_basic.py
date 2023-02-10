# tests/examples/test_basic.py
"""Module to test tessifs basic examples."""
from tessif_examples import basic


def test_mwe():
    """Test mwe creation."""
    esys = basic.create_mwe()
    assert esys.uid == "Minimum_Working_Example"


def test_fpw():
    """Test fpwe creation."""
    esys = basic.create_fpwe()
    assert esys.uid == "Fully_Parameterized_Working_Example"


def test_emission_objective():
    """Test emission_objective creation."""
    esys = basic.create_emission_objective()
    assert esys.uid == "Emission_Objective_Example"


def test_connected_es():
    """Test connected_es creation."""
    esys = basic.create_connected_es()
    assert esys.uid == "Connected-Energy-Systems-Example"


def test_chp():
    """Test chp creation."""
    esys = basic.create_chp()
    assert esys.uid == "CHP_Example"


def test_variable_chp():
    """Test variable_chp creation."""
    esys = basic.create_variable_chp()
    assert esys.uid == "CHP_Example"


def test_storage_example():
    """Test storage_example creation."""
    esys = basic.create_storage_example()
    assert esys.uid == "Storage-Energysystem-Example"


def test_expansion_plan_example():
    """Test expansion_plan_example creation."""
    esys = basic.create_expansion_plan_example()
    assert esys.uid == "Expansion Plan Example"


def test_simple_transformer_grid_es():
    """Test simple_transformer_grid_es creation."""
    esys = basic.create_simple_transformer_grid_es()
    assert esys.uid == "Two Transformer Grid Example"


def test_time_varying_efficiency_transformer():
    """Test time_varying_efficiency_transformer creation."""
    esys = basic.create_time_varying_efficiency_transformer()
    assert esys.uid == "Transformer-Timeseries-Example"


def test_zero_costs_es():
    """Test zero_costs_es creation."""
    esys = basic.create_zero_costs_es()
    assert esys.uid == "Zero Costs Example"


def test_self_similar_energy_system():
    """Test self_similar_energy_system creation."""
    esys = basic.create_self_similar_energy_system()
    assert esys.uid == "Self_Similar_Energy_System_(N=1)"


def test_mssesu():
    """Test mssesu creation."""
    esys = basic.create_mssesu()
    assert esys.uid == "Energy_System_1"


def test_storage_fixed_ratio_expansion_example():
    """Test storage_fixed_ratio_expansion_example creation."""
    esys = basic.create_storage_fixed_ratio_expansion_example()
    assert esys.uid == "Storage-Energysystem-Example"
