# src/tessif_examples/mwe.py
"""Tessif minimum working example energy system model."""
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_mwe():
    """Create minimally parameterized working example.

    Creates a simple energy system simulation to potentially
    store it on disc inside :paramref:`~create_mwe.directory` as
    :paramref:`~create_mwe.filename`.

    Returns
    -------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif minimum working example energy system.

    Example
    -------
    Visualize the energy system for better understanding what the output means::

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_mwe(),
            color_group={
                'Gas Station': '#006666',
                'Pipeline': '#006666',
                'Generator': '#006666',
                'Powerline': '#ffcc00',
                'Battery': '#ff6600',
                'Demand': '#009900',
            },
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/mwe.png
        :align: center
        :alt: Image showing the mwe energy system graph
    """
    # 2. Create a simulation time frame of 2 one hour time steps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=4, freq="H")

    # 3. Creating the individual energy system components:
    fuel_supply = components.Source(
        name="Gas Station",
        outputs=("fuel",),
        # Minimum number of arguments required
    )

    power_generator = components.Transformer(
        name="Generator",
        inputs=("fuel",),
        outputs=("electricity",),
        conversions={("fuel", "electricity"): 0.42},
        # Minimum number of arguments required
        flow_costs={"electricity": 2, "fuel": 0},
    )

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    storage = components.Storage(
        name="Battery",
        input="electricity",
        output="electricity",
        capacity=20,
        initial_soc=10,
        # Minimum number of arguments required
        # flow_rates={'electricity': nts.MinMax(min=0, max=11)},
        flow_costs={"electricity": 0.1},
    )

    fuel_supply_line = components.Bus(
        name="Pipeline",
        inputs=("Gas Station.fuel",),
        outputs=("Generator.fuel",),
        # Minimum number of arguments required
    )

    electricity_line = components.Bus(
        name="Powerline",
        inputs=("Generator.electricity", "Battery.electricity"),
        outputs=("Demand.electricity", "Battery.electricity"),
        # Minimum number of arguments required
    )

    # 4. Creating the actual energy system:
    explicit_es = energy_system.AbstractEnergySystem(
        uid="Minimum_Working_Example",
        busses=(fuel_supply_line, electricity_line),
        sinks=(demand,),
        sources=(fuel_supply,),
        transformers=(power_generator,),
        storages=(storage,),
        timeframe=timeframe,
    )

    return explicit_es
