# src/tessif_examples/emission_objective.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_emission_objective(directory=None, filename=None):
    """
    Create a minimal working example using :mod:`tessif's
    model <tessif.model>` optimizing it for costs and keeping
    the total emissions below an emission objective.

    Return
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`examples_auto_comparison_emissions` - For simulating and
    comparing this energy system using different supported models.

    :ref:`Secondary_Objectives` - For a detailed description on how to
    constrain values like co2 emissions.

    Examples
    --------
    Visualize the energy system for better understanding what the output means:

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_emission_objective(),
            color_group={
              'Wind Power': '#00ccff',
              'Gas Source': '#336666',
              'Gas Grid': '#336666',
              'Gas Plant': '#336666',
              'Gas Station': '#666666',
              'Pipeline': '#666666',
              'Generator': '#666666',
                'Powerline': 'yellow',
                'Demand': 'yellow',
            },
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/emission_objective.png
        :align: center
        :alt: Image showing the emission_objective example energy system graph
    """

    # 2. Create a simulation time frame of four one-hour timesteps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=4, freq="H")

    # 3. Creating the individual energy system components:

    # first supply chain
    fuel_supply = components.Source(
        name="Gas Station",
        outputs=("fuel",),
        # Minimum number of arguments required
        flow_emissions={"fuel": 1.5},
        flow_costs={"fuel": 2},
    )

    fuel_supply_line = components.Bus(
        name="Pipeline",
        inputs=("Gas Station.fuel",),
        outputs=("Generator.fuel",),
        # Minimum number of arguments required
    )

    # conventional power supply is cheaper, but has emissions allocated to it
    power_generator = components.Transformer(
        name="Generator",
        inputs=("fuel",),
        outputs=("electricity",),
        conversions={("fuel", "electricity"): 0.42},
        # Minimum number of arguments required
        flow_costs={"electricity": 2, "fuel": 0},
        flow_emissions={"electricity": 3, "fuel": 0},
    )

    # second supply chain
    gas_supply = components.Source(
        name="Gas Source",
        outputs=("gas",),
        # Minimum number of arguments required
        flow_emissions={"gas": 0.5},
        flow_costs={"gas": 1},
    )

    gas_grid = components.Bus(
        name="Gas Grid",
        inputs=("Gas Source.gas",),
        outputs=("Gas Plant.gas",),
        # Minimum number of arguments required
    )

    # conventional power supply is cheaper, but has emissions allocated to it
    gas_plant = components.Transformer(
        name="Gas Plant",
        inputs=("gas",),
        outputs=("electricity",),
        conversions={("gas", "electricity"): 0.6},
        # Minimum number of arguments required
        flow_rates={"electricity": (0, 5), "gas": (0, float("+inf"))},
        flow_costs={"electricity": 1, "gas": 0},
        flow_emissions={"electricity": 2, "gas": 0},
    )

    # wind power is more expensive but has no emissions allocated to it
    wind_power = components.Source(
        name="Wind Power",
        outputs=("electricity",),
        flow_costs={"electricity": 10},
    )

    # Demand needing 10 energy units per time step
    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    electricity_line = components.Bus(
        name="Powerline",
        inputs=(
            "Generator.electricity",
            "Wind Power.electricity",
            "Gas Plant.electricity",
        ),
        outputs=("Demand.electricity",),
        # Minimum number of arguments required
    )

    global_constraints = {"emissions": 60}

    # 4. Creating the actual energy system:
    explicit_es = energy_system.AbstractEnergySystem(
        uid="Emission_Objective_Example",
        busses=(fuel_supply_line, electricity_line, gas_grid),
        sinks=(demand,),
        sources=(fuel_supply, wind_power, gas_supply),
        transformers=(power_generator, gas_plant),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return explicit_es
