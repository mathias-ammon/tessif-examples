# src/tessif_examples/self_similar_energy_system.py
"""Tessif minimum working example energy system model."""
import datetime
import random

import numpy as np
import pandas as pd
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_self_similar_energy_system(N=1, timeframe=None):
    """
    Create a `self-similar <https://en.wikipedia.org/wiki/Self-similarity>`_
    energy system. This energy system obtained by repeating it's smallest unit
    N times. The singular units are connected one level down through their
    central bus. Meaning the central bus of energy system N is connected to
    the central bus of energy system N-1 via a
    :class:`~tessif.model.components.Connector` object.

    The self similar energy system consists of:

        - 3 :class:`~tessif.model.components.Source` objects:

            - One having a randomized output, emulating renweable sources.
              With an installed power between 10 and 200 units.
            - One `slack source <https://en.wikipedia.org/wiki/Slack_bus>`_
              providing energy to balance the system if nedded.
              (This could be interpreted as an import node, for meeting load
              demands)
            - One commodity source feeding the transformer

        - 2 :class:`~tessif.model.components.Sink` objects:

            - One having a fixed input with a net demand between 50 and 100
              units.
            - One `slack sink <https://en.wikipedia.org/wiki/Slack_bus>`_
              taking energy in to balance the system if nedded.
              (This could be interpreted as an export node, for handling excess
              loads.)

        - 2 :class:`~tessif.model.components.Bus` objects:

            - One central bus connecting the storage and transformer, as well
              as the sinks and sources and up to 2 additonal self similar
              energy system units.

            - An auxillary bus connecting the transformer and the central bus

        - 1 :class:`~tessif.model.components.Transformer` object:

            - Fully parameterized transformer emulating a coal power plant
              with a installed capacity between 50 and 100 units.

        - 1 :class:`~tessif.model.components.Storage` object:

            - no constraints to in and outflow. Efficiency,
              losses, expansion investment etc. oriented at grid level
              batteries (i.e tesla)



    Parameters
    ----------
    N: int
        Number of minimum self similar energy system units (MiSSESUs) the self
        similar energy system consists of.

    timeframe: pandas.DatetimeIndex
        Datetime index representing the evaluated timeframe. Explicitly
        stating:

            - initial datatime
              (0th element of the :class:`pandas.DatetimeIndex`)
            - number of timesteps (length of :class:`pandas.DatetimeIndex`)
            - temporal resolution (:attr:`pandas.DatetimeIndex.freq`)

        For example::

            idx = pd.DatetimeIndex(
                data=pd.date_range(
                    '2016-01-01 00:00:00', periods=11, freq='H'))

    Examples
    --------
    Creating a self similar energy system out of N=2 minimum self similar
    energy system units:

        from tessif.frused.paths import example_dir
        import os
        storage_path = os.path.join(example_dir, 'data', 'tsf',)

        import tessif.examples.data.tsf.py_hard as coded_examples
        sses = coded_examples.create_self_similar_energy_system(N=2)

    # Create an image using AbstractEnergySystem.to_nxgrph() and
    # tessif.visualize.nxgrph
    """

    # 1.) Create the energy system using tessif
    fractals = list()
    for n in range(N):
        # the n-th energy system starting to count at 0
        # as added to the list of mssess
        fractals.append(_create_mssesu(n))

    if timeframe is None:
        timeframe = pd.date_range(datetime.datetime.now().date(), periods=1, freq="H")

    self_similar_es = energy_system.AbstractEnergySystem(
        uid="".join(["Self_Similar_Energy_System_(N=", str(N), ")"]),
        #     busses=[bus for fractal in fractals for bus in fractal.busses],
        #     sinks=[sink for fractal in fractals for sink in fractal.sinks],
        #     sources=[source for fractal in fractals for source in fractal.sources],
        #     connectors=[
        #         connector for fractal in fractals for connector in fractal.connectors
        #     ],
        #     transformers=[
        #         transformer for fractal in fractals for transformer in fractal.transformers
        #     ],
        #     storages=[storage for fractal in fractals for storage in fractal.storages],
        #     timeframe=timeframe,
    )

    return self_similar_es


def _create_mssesu(n, seed=None):
    """
    Create a minimum self simular energy system unit (mssesu).
    """
    timeframe = pd.date_range(datetime.datetime.now(), periods=1, freq="H")

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

    # msses = energy_system.AbstractEnergySystem(
    #     uid="_".join(["Energy_System", str(n)]),
    #     busses=(central_bus, fuel_line),
    #     sinks=(demand_sink, excess_sink),
    #     sources=(excess_source, non_renewable_source, renewable_source),
    #     connectors=connectors,
    #     transformers=(power_generator,),
    #     storages=(storage,),
    #     timeframe=timeframe,
    # )

    # return msses
