# src/tessif_examples/time_varying_efficiency_transformer.py
"""Tessif minimum working example energy system model."""
import numpy as np
import pandas as pd
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_time_varying_efficiency_transformer():
    """Create a small es having a transformer with varying efficiency.

    Returns
    -------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif minimum working example energy system.

    Example
    -------
    Visualize the energy system for better understanding what the output means:

          from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_time_varying_efficiency_transformer(),
            color_group={
                'Transformer': '#006666',
                'Commodity': '#006666',
                'Com Bus': '#006666',
                'Powerline': '#ffcc00',
                'Import': '#ff6600',
                'Demand': '#009900',
             },
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        # app.run_server(debug=False)

    .. image:: ../images/time_varying_efficiency_transformer.png
        :align: center
        :alt: Image showing the mwe energy system graph
    """

    opt_timespan = pd.date_range("7/13/1990", periods=3, freq="H")

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        carrier="electricity",
        node_type="sink",
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    commodity = components.Source(
        name="Commodity",
        outputs=("energy",),
        carrier="energy",
        node_type="source",
    )

    import_source = components.Source(
        name="Import",
        outputs=("electricity",),
        carrier="electricity",
        node_type="source",
        flow_costs={"electricity": 1000},
    )

    transformer = components.Transformer(
        name="Transformer",
        inputs=("energy",),
        outputs=("electricity",),
        conversions={("energy", "electricity"): [3 / 5, 4 / 5, 2 / 5]},
        # conversions={('energy', 'electricity'): 1},
        #
        # flow_rates={
        #     "energy": nts.MinMax(0, float("+inf")),
        #     "electricity": nts.MinMax(0, 10)
        # },
        flow_costs={"energy": 0, "electricity": 100},
        flow_emissions={"energy": 0, "electricity": 1000},
    )

    commodity_bus = components.Bus(
        name="Com Bus",
        inputs=("Commodity.energy",),
        outputs=("Transformer.energy",),
        carrier="energy",
        node_type="bus",
    )

    powerline = components.Bus(
        name="Powerline",
        inputs=("Transformer.electricity", "Import.electricity"),
        outputs=("Demand.electricity",),
        carrier="electricity",
        node_type="bus",
    )

    transformer_eff_es = energy_system.AbstractEnergySystem(
        uid="Transformer-Timeseries-Example",
        busses=(
            commodity_bus,
            powerline,
        ),
        sinks=(demand,),
        sources=(commodity, import_source),
        transformers=(transformer,),
        timeframe=opt_timespan,
    )

    return transformer_eff_es
