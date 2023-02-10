# src/tessif_examples/mssesu.py
"""Tessif minimum working example energy system model."""
import datetime
import random

import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_mssesu(n=1, seed=None):
    """
    Create a minimum self simular energy system unit (mssesu).
    """
    timeframe = date_range(datetime.datetime.now(), periods=1, freq="H")

    # See tessif.examples.data.tsf.py_hard as well as
    # tessif.model.components for examples and information
    # (both in the code and using the doc)

    # 1) randomize demand and production
    if seed:
        random.seed(seed)
    demand = random.randint(1, 100)
    renewable_output = random.randint(1, 50)

    demand_sink = components.Sink(
        name="_".join(["sink", str(n)]),
        inputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=demand, max=demand)},
    )

    # excess sink enables the energy system to always be solveable even if
    # the randomized components wouldn't provide a solveable energy system

    excess_sink = components.Sink(
        name="_".join(["excess_sink", str(n)]),
        inputs=("electricity",),
        flow_costs={"electricity": 100},
    )

    # 2) Create the sources

    excess_source = components.Source(
        name="_".join(["excess_source", str(n)]),
        outputs=("electricity",),
        flow_costs={"electricity": 100},
    )

    # 2.1) renewable source

    renewable_source = components.Source(
        name="_".join(["renewable_source", str(n)]),
        outputs=("electricity",),
        flow_costs={"electricity": 5},
        node_type="Renewable",
        carrier="Electricity",
        flow_rates={
            "electricity": nts.MinMax(min=renewable_output, max=renewable_output)
        },
        flow_emissions={"electricity": 0},
    )

    # 2.2) non-renewable source

    non_renewable_source = components.Source(
        name="_".join(["non_renewable_source", str(n)]),
        outputs=("fuel",),
        flow_costs={"fuel": 10},
    )

    # 3) Create the transformer

    power_generator = components.Transformer(
        name="_".join(["power_generator", str(n)]),
        inputs=("fuel",),
        outputs=("electricity",),
        conversions={("fuel", "electricity"): 0.42},
    )

    # 4) Create the connector

    connectors = list()

    if n == 0:
        pass
    else:
        connector = components.Connector(
            name="_".join(["connector", str(n - 1)]),
            interfaces=(
                "_".join(["central_bus", str(n - 1)]),
                "_".join(["central_bus", str(n)]),
            ),
            inputs=[
                "_".join(["central_bus", str(n - 1)]),
                "_".join(["central_bus", str(n)]),
            ],
            outputs=(
                "_".join(["central_bus", str(n - 1)]),
                "_".join(["central_bus", str(n)]),
            ),
        )
        connectors.append(connector)

    # 5) Create the storage
    storage = components.Storage(
        name="_".join(["storage", str(n)]),
        input="electricity",
        output="electricity",
        capacity=1,
        initial_soc=1,
    )

    # 6) Create the bus
    central_bus = components.Bus(
        name="_".join(["central_bus", str(n)]),
        inputs=(
            "".join(["excess_source_", str(n), ".electricity"]),
            "".join(["storage_", str(n), ".electricity"]),
            "".join(["renewable_source_", str(n), ".electricity"]),
            "".join(["power_generator_", str(n), ".electricity"]),
        ),
        outputs=(
            "".join(["excess_sink_", str(n), ".electricity"]),
            "".join(["sink_", str(n), ".electricity"]),
            "".join(["storage_", str(n), ".electricity"]),
        ),
    )

    # there needs to be another bus which connects the transformer and the non-renewable source

    fuel_line = components.Bus(
        name="_".join(["fuel_line", str(n)]),
        inputs=("".join(["non_renewable_source_", str(n), ".fuel"]),),
        outputs=("".join(["power_generator_", str(n), ".fuel"]),),
    )

    msses = energy_system.AbstractEnergySystem(
        uid="_".join(["Energy_System", str(n)]),
        busses=(central_bus, fuel_line),
        sinks=(demand_sink, excess_sink),
        sources=(excess_source, non_renewable_source, renewable_source),
        connectors=connectors,
        transformers=(power_generator,),
        storages=(storage,),
        timeframe=timeframe,
    )

    return msses
