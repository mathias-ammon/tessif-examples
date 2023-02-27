# src/tessif_examples/conected_es.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_connected_es():
    """Create a minimal transipment problem example.

    Return
    ------
    :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system.

    Examples
    --------
    Generic System Visualization:

    .. image:: ../../_static/system_model_graphs/connected_es.png
        :align: center
        :alt: Image showing the connected_es energy system graph
    """
    timeframe = date_range("7/13/1990", periods=3, freq="H")

    s1 = components.Sink(
        name="sink-01",
        inputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=15)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([0, 15, 10]), max=np.array([0, 15, 10])
            )
        },
    )

    so1 = components.Source(
        name="source-01",
        outputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        flow_costs={"electricity": 1},
        flow_emissions={"electricity": 0.8},
    )

    mb1 = components.Bus(
        name="bus-01",
        inputs=("source-01.electricity",),
        outputs=("sink-01.electricity",),
    )

    s2 = components.Sink(
        name="sink-02",
        inputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=15)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([15, 0, 10]), max=np.array([15, 0, 10])
            )
        },
    )

    so2 = components.Source(
        name="source-02",
        outputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        flow_costs={"electricity": 1},
        flow_emissions={"electricity": 1.2},
    )

    mb2 = components.Bus(
        name="bus-02",
        inputs=("source-02.electricity",),
        outputs=("sink-02.electricity",),
    )

    c = components.Connector(
        name="connector",
        interfaces=("bus-01", "bus-02"),
        conversions={("bus-01", "bus-02"): 0.9, ("bus-02", "bus-01"): 0.8},
    )

    connected_es = system_model.AbstractEnergySystem(
        uid="Connected-Energy-Systems-Example",
        busses=(mb1, mb2),
        sinks=(
            s1,
            s2,
        ),
        sources=(so1, so2),
        connectors=(c,),
        timeframe=timeframe,
    )

    return connected_es
