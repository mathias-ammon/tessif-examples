# src/tessif_examples/self_similar_system_model.py
"""Tessif minimum working example energy system model."""
import datetime
import random

import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_self_similar_system_model(n=1, timeframe=None, unit="minimal", **kwargs):
    """Create a self similar system model.

    Created by Mathias Ammon, Frederik Emmel and Andreas Jessen.

    This energy system is obtained by repeating its unit N times. The singular
    units are connected to each other through their central bus. Meaning the
    central bus of energy system N is connected to the central bus of energy
    system N-1 via a :class:`~tessif.model.components.Connector` object.

    Parameters
    ----------
    N: int
        Number of units the self similar energy system consists of.

    timeframe: pandas.DatetimeIndex
        Datetime index representing the evaluated timeframe. Explicitly
        stating:

            - initial datatime
              (0th element of the :class:`pandas.DatetimeIndex`)
            - number of time steps (length of :class:`pandas.DatetimeIndex`)
            - temporal resolution (:attr:`pandas.DatetimeIndex.freq`)

        For example::

            idx = pd.DatetimeIndex(
                data=pd.date_range(
                    '2016-01-01 00:00:00', periods=11, freq='H'))

    unit: str
        Specify which of tessif's hardcoded examples should be used as unit of
        the self similar energy system.

        Currently available are:

            - 'minimal':
                Uses _create_minimal_es_unit() which is the smallest unit
                available.
            - 'component':
                Uses _create_component_es_unit() which is based on
                create_component_es().
            - 'grid':
                Uses _create_grid_es_unit() which is based on
                create_transcne_es().
            - 'hamburg':
                Uses _create_hhes_unit() which is based on create_hhes_unit().

    kwargs:
        Are passed to the _create_[...]_unit() function.
    """
    if timeframe is None:
        timeframe = date_range(datetime.datetime.now().date(), periods=5, freq="H")

    # Create the energy system using tessif
    fractals = list()
    for nmbr in range(n):
        # the n-th energy system starting to count at 0 is added to the list of
        # es units.
        if unit == "minimal":
            fractals.append(
                create_minimal_es_unit(n=nmbr, timeframe=timeframe, **kwargs)
            )
        # elif unit == 'component':
        #     fractals.append(
        #         _create_component_es_unit(n=n, timeframe=timeframe, **kwargs))
        # elif unit == 'grid':
        #     fractals.append(_create_grid_es_unit(
        #         n=n, timeframe=timeframe, **kwargs))
        # elif unit == 'hamburg':
        #     fractals.append(_create_hhes_unit(
        #         n=n, timeframe=timeframe, **kwargs))

    self_similar_es = system_model.AbstractEnergySystem(
        uid=f"Self Similar System Model (n={n})",
        busses=[bus for fractal in fractals for bus in fractal.busses],
        sinks=[sink for fractal in fractals for sink in fractal.sinks],
        sources=[source for fractal in fractals for source in fractal.sources],
        connectors=[
            connector for fractal in fractals for connector in fractal.connectors
        ],
        transformers=[
            transformer for fractal in fractals for transformer in fractal.transformers
        ],
        storages=[storage for fractal in fractals for storage in fractal.storages],
        timeframe=timeframe,
    )

    return self_similar_es


def create_minimal_es_unit(n, timeframe=None, seed=None):
    """Create a minimal self simular energy system unit.

    Is used by create_self_similar_energy_system().

    Created by Mathias Ammon and Andreas Jessen.

    The self similar energy system unit consists of:

        - 3 :class:`~tessif.components.Source` objects:

            - One having a randomized output, emulating renewable sources.
              With an installed power between 10 and 200 units.
            - One `slack source <https://en.wikipedia.org/wiki/Slack_bus>`_
              providing energy to balance the system if needed.
              (This could be interpreted as an import node, for meeting load
              demands)
            - One commodity source feeding the transformer

        - 2 :class:`~tessif.components.Sink` objects:

            - One having a fixed input with a net demand between 50 and 100
              units.
            - One `slack sink <https://en.wikipedia.org/wiki/Slack_bus>`_
              taking energy in to balance the system if needed.
              (This could be interpreted as an export node, for handling excess
              loads.)

        - 2 :class:`~tessif.components.Bus` objects:

            - One central bus connecting the storage and transformer, as well
              as the sinks and sources and up to 2 additional self similar
              energy system units.

            - An auxiliary bus connecting the transformer and the central bus

        - 1 :class:`~tessif.components.Transformer` object:

            - Fully parameterized transformer emulating a coal power plant
              with an installed capacity between 50 and 100 units.

        - 1 :class:`~tessif.components.Storage` object:

            - no constraints to in and outflow. Efficiency,
              losses, expansion investment etc. oriented at grid level
              batteries (e.g. tesla)

    Parameters
    ----------
    n: int
        Number of the es unit. This ist needed to be able to give each
        component in the complete self similar es a unique name.

    timeframe: pandas.DatetimeIndex
        Datetime index representing the evaluated timeframe. Explicitly
        stating:

            - initial datatime
              (0th element of the :class:`pandas.DatetimeIndex`)
            - number of time steps (length of :class:`pandas.DatetimeIndex`)
            - temporal resolution (:attr:`pandas.DatetimeIndex.freq`)

        For example::

            idx = pd.DatetimeIndex(
                data=pd.date_range(
                    '2016-01-01 00:00:00', periods=11, freq='H'))
    """
    if timeframe is None:
        timeframe = date_range(
            datetime.datetime.now(),
            periods=5,
            freq="H",
        )

    # See tessif.examples.data.tsf.py_hard as well as
    # tessif.components for examples and information
    # (both in the code and using the doc)

    # 1) randomize demand and production
    if seed:
        random.seed(seed)
    demand = random.randint(1, 100)
    renewable_output = random.randint(1, 50)

    demand_sink = components.Sink(
        name="Sink " + str(n),
        inputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=demand, max=demand)},
    )

    # excess_sink enables the energy system to be always solvable even if
    # the randomized components wouldn't provide a solvable energy system.
    excess_sink = components.Sink(
        name="Excess Sink " + str(n),
        inputs=("electricity",),
        flow_costs={"electricity": 100},
    )

    # 2) Create the sources
    excess_source = components.Source(
        name="Excess Source " + str(n),
        outputs=("electricity",),
        flow_costs={"electricity": 100},
    )

    # 2.1) renewable source
    renewable_source = components.Source(
        name="Renewable Source " + str(n),
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
        name="Non Renewable Source " + str(n),
        outputs=("fuel",),
        flow_costs={"fuel": 10},
    )

    # 3) Create the transformer
    power_generator = components.Transformer(
        name="Power Generator " + str(n),
        inputs=("fuel",),
        outputs=("electricity",),
        conversions={("fuel", "electricity"): 0.42},
    )

    # 4) Create the connector. (Use connectors list to prevent error in case no
    # connector is created.)
    connectors = list()

    if n == 0:
        pass
    else:
        connector = components.Connector(
            name="Connector " + str(n),
            interfaces=(
                "Central Bus " + str(n - 1),
                "Central Bus " + str(n),
            ),
            inputs=[
                "Central Bus " + str(n - 1),
                "Central Bus " + str(n),
            ],
            outputs=(
                "Central Bus " + str(n - 1),
                "Central Bus " + str(n),
            ),
        )
        connectors.append(connector)

    # 5) Create the storage
    storage = components.Storage(
        name="Storage " + str(n),
        input="electricity",
        output="electricity",
        capacity=1,
        initial_soc=1,
    )

    # 6) Create the bus
    central_bus = components.Bus(
        name="Central Bus " + str(n),
        inputs=(
            "Excess Source " + str(n) + ".electricity",
            "Storage " + str(n) + ".electricity",
            "Renewable Source " + str(n) + ".electricity",
            "Power Generator " + str(n) + ".electricity",
        ),
        outputs=(
            "Excess Sink " + str(n) + ".electricity",
            "Sink " + str(n) + ".electricity",
            "Storage " + str(n) + ".electricity",
        ),
    )

    # There needs to be another bus which connects the transformer and the
    # non-renewable source.
    fuel_line = components.Bus(
        name="Fuel Line " + str(n),
        inputs=("Non Renewable Source " + str(n) + ".fuel",),
        outputs=("Power Generator " + str(n) + ".fuel",),
    )

    minimal_es = system_model.AbstractEnergySystem(
        uid="Minimum Self Similar System Model Unit " + str(n),
        busses=(central_bus, fuel_line),
        sinks=(demand_sink, excess_sink),
        sources=(excess_source, non_renewable_source, renewable_source),
        connectors=connectors,
        transformers=(power_generator,),
        storages=(storage,),
        timeframe=timeframe,
    )

    return minimal_es
