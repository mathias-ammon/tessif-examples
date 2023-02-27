# src/tessif_examples/storage_fixed_expansion_example.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_storage_fixed_ratio_expansion_example():
    """Create a storage with fixed expansion ratio example.

    Create a small energy system utilizing an expandable storage with a fixed
    capacity to outflow ratio.

    Return
    ------
    es: :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system.

    Warning
    -------
    In this example the installed capacity is set to 1, but expandable.
    The flow rate to 0.1. By enabling both expandables (capacity and flow rate)
    as well as fixing their ratios the installed capacity result will be
    much higher than needed. Or in other words, the flow rate will determine
    the amount of installed capacity.

    Example
    -------
    Generic System Visualization

    .. image:: ../images/storage_es_example.png
        :align: center
        :alt: Image showing the create_storage_example energy system graph.
    """
    timeframe = date_range("7/13/1990", periods=5, freq="H")

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        carrier="electricity",
        node_type="sink",
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([10, 10, 7, 10, 10]), max=np.array([10, 10, 7, 10, 10])
            )
        },
    )

    generator = components.Source(
        name="Generator",
        outputs=("electricity",),
        carrier="electricity",
        node_type="source",
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        flow_costs={"electricity": 0},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([19, 19, 19, 0, 0]), max=np.array([19, 19, 19, 0, 0])
            )
        },
    )

    powerline = components.Bus(
        name="Powerline",
        inputs=("Generator.electricity", "Storage.electricity"),
        outputs=(
            "Demand.electricity",
            "Storage.electricity",
        ),
        carrier="electricity",
        node_type="bus",
    )

    storage = components.Storage(
        name="Storage",
        input="electricity",
        output="electricity",
        capacity=1,
        initial_soc=0,
        carrier="electricity",
        node_type="storage",
        flow_rates={"electricity": nts.MinMax(min=0, max=0.1)},
        flow_efficiencies={"electricity": nts.InOut(inflow=0.95, outflow=0.89)},
        flow_costs={"electricity": 1},
        flow_emissions={"electricity": 0.5},
        expandable={"capacity": True, "electricity": True},
        fixed_expansion_ratios={"electricity": True},
        expansion_costs={"capacity": 2, "electricity": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=1, max=float("+inf")),
            "electricity": nts.MinMax(min=0.1, max=float("+inf")),
        },
    )

    storage_es = system_model.AbstractEnergySystem(
        uid="Storage-Energysystem-Example",
        busses=(powerline,),
        sinks=(demand,),
        sources=(generator,),
        storages=(storage,),
        timeframe=timeframe,
    )

    return storage_es
