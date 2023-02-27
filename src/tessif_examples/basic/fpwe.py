# src/tessif_examples/fpwe.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_fpwe():
    """Create a fully parameterized working example.

    Return
    ------
    :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system.

    Examples
    --------
    Generic System Visualization:

    .. image:: ../../_static/system_model_graphs/fpwe.png
        :align: center
        :alt: Image showing the fpwe energy system graph
    """
    # 2. Create a simulation time frame of of 3 one hour time steps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=3, freq="H")

    # 3. Initiate the global constraints
    global_constraints = {
        "name": "default",
        "emissions": float("+inf"),
        "resources": float("+inf"),
    }

    # 3. Creating the individual energy system components:
    solar_panel = components.Source(
        name="Solar Panel",
        outputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="Renewable",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=1000)},
        flow_rates={"electricity": nts.MinMax(min=20, max=20)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={"electricity": nts.PositiveNegative(positive=42, negative=42)},
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([12, 3, 7]), max=np.array([12, 3, 7])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 5},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    fuel_supply = components.Source(
        name="Gas Station",
        outputs=("fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="Gas",
        node_type="source",
        accumulated_amounts={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"fuel": nts.MinMax(min=0, max=100)},  # float('+inf'))},
        flow_costs={"fuel": 10},
        flow_emissions={"fuel": 3},
        flow_gradients={"fuel": nts.PositiveNegative(positive=100, negative=100)},
        gradient_costs={"fuel": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"fuel": False},
        expansion_costs={"fuel": 5},
        expansion_limits={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        milp={"fuel": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    power_generator = components.Transformer(
        name="Generator",
        inputs=("fuel",),
        outputs=("electricity",),
        conversions={("fuel", "electricity"): 0.42},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=50),
            "electricity": nts.MinMax(min=0, max=15),
        },
        flow_costs={"fuel": 0, "electricity": 10},
        flow_emissions={"fuel": 0, "electricity": 10},
        flow_gradients={
            "fuel": nts.PositiveNegative(positive=50, negative=50),
            "electricity": nts.PositiveNegative(positive=15, negative=15),
        },
        gradient_costs={
            "fuel": nts.PositiveNegative(positive=0, negative=0),
            "electricity": nts.PositiveNegative(positive=0, negative=0),
        },
        timeseries=None,
        expandable={"fuel": False, "electricity": False},
        expansion_costs={"fuel": 0, "electricity": 0},
        expansion_limits={
            "fuel": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False, "fuel": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=2),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=9),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"electricity": nts.MinMax(min=11, max=11)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={"electricity": nts.PositiveNegative(positive=12, negative=12)},
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"electricity": False},
        expansion_costs={"electricity": 0},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=2, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=8),
        costs_for_being_active=0
        # Total number of arguments to specify sink object
    )

    storage = components.Storage(
        name="Battery",
        input="electricity",
        output="electricity",
        capacity=10,
        initial_soc=10,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=1),
        flow_rates={"electricity": nts.MinMax(min=0, max=30)},
        flow_efficiencies={"electricity": nts.InOut(inflow=1, outflow=1)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(
                positive=float("+inf"), negative=float("+inf")
            )
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"capacity": False, "electricity": False},
        expansion_costs={"capacity": 2, "electricity": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=2),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=42),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    fuel_supply_line = components.Bus(
        name="Pipeline",
        inputs=("Gas Station.fuel",),
        outputs=("Generator.fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="gas",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    electricity_line = components.Bus(
        name="Powerline",
        inputs=(
            "Generator.electricity",
            "Battery.electricity",
            "Solar Panel.electricity",
        ),
        outputs=("Demand.electricity", "Battery.electricity"),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    # 4. Creating the actual energy system:

    explicit_es = system_model.AbstractEnergySystem(
        uid="Fully_Parameterized_Working_Example",
        busses=(fuel_supply_line, electricity_line),
        sinks=(demand,),
        sources=(fuel_supply, solar_panel),
        transformers=(power_generator,),
        storages=(storage,),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return explicit_es
