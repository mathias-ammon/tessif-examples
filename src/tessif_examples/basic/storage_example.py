# src/tessif_examples/basic/storage_example.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_storage_example():
    """Create a small energy system utilizing a storage.

    Return
    ------
    :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system.

    Warning
    -------
    In this example the installed capacity is set to 0, but expandable
    (A common use case). Common ESSMOS tools, however, use capacity specific
    values for idle losses and initial as well as final soc constraints.

    Given the initial capacity is 0, this problem is solved by setting the
    initial soc as well as the idle losses to 0, if necessary.

    To avoid this caveat, set the inital capacity to a small value and adjust
    initial soc and idle changes accordingly. This might involve some trial and
    error.

    Examples
    --------
    Generic System Visualization:

    .. image:: ../../_static/system_model_graphs/storage_es_example.png
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
        flow_costs={"electricity": 2},
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
        capacity=0,
        initial_soc=0,
        carrier="electricity",
        node_type="storage",
        flow_efficiencies={"electricity": nts.InOut(inflow=0.9, outflow=0.9)},
        flow_costs={"electricity": 1},
        flow_emissions={"electricity": 0.5},
        expandable={"capacity": True, "electricity": False},
        expansion_costs={"capacity": 0, "electricity": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
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
