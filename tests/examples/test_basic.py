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
    assert esys.uid == "Minimum_Working_Example"
def test_emission_objectiv():
    """Test emission_objectiv creation."""
    esys = basic.create_emission_objectiv()
    assert esys.uid == "Minimum_Working_Example"
def test_connected_es():
    """Test connected_es creation."""
    esys = basic.create_connected_es()
    assert esys.uid == "Minimum_Working_Example"
def test_chp():
    """Test chp creation."""
    esys = basic.create_chp()
    assert esys.uid == "Minimum_Working_Example"
def test_variable_chp():
    """Test variable_chp creation."""
    esys = basic.create_variable_chp()
    assert esys.uid == "Minimum_Working_Example"
def test_storage_example():
    """Test variable_chp creation."""
    esys = basic.create_storage_example()
    assert esys.uid == "Minimum_Working_Example"
def test_expansion_plan_example():
    """Test variable_chp creation."""
    esys = basic.create_expansion_plan_example()
    assert esys.uid == "Minimum_Working_Example"
def test_simple_transformer_grid_es():
    """Test variable_chp creation."""
    esys = basic.create_simple_transformer_grid_es()
    assert esys.uid == "Minimum_Working_Example"
def test_time_varying_efficiency_transformer():
    """Test variable_chp creation."""
    esys = basic.create_time_varying_efficiency_transformer()
    assert esys.uid == "Minimum_Working_Example"