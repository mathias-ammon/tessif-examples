# src/tessif_examples/plausbility/mwe.py
"""Tessif storage emissions plausibility check MSC."""
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_storage_emissions():
    """Create a storage-emissions plausibility check MSC.

    Returns
    -------
    :class:`tessif.system_model.AbstractEnergySystem`
        Storage-Emissions plausibility check MSC.

    Example
    -------
    .. image:: ../../_static/system_model_graphs/storage_emissions.png
        :align: center
        :alt: Image showing the mwe energy system graph
    """
    # 2. Create a simulation time frame of 2 one hour time steps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=4, freq="H")

    global_constraints = {
        "name": "emissions_constraint",
        "emissions": 20,
    }

    demand = components.Sink(
        name="Energy Demand Component",
        inputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    storage = components.Storage(
        name="Energy Storage Component",
        input="electricity",
        output="electricity",
        capacity=100,
        initial_soc=0,
        flow_emissions={"electricity": 1},
    )

    source_1 = components.Source(
        name="Energy Source Component 1",
        outputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=100)},
        # fixing flow rate to timeseries helps fine parsing mimimum flow
        timeseries={
            "electricity": nts.MinMax(
                min=[
                    110,
                    0,
                    0,
                    0,
                ],
                max=[
                    110,
                    0,
                    0,
                    0,
                ],
            ),
        },
    )

    source_2 = components.Source(
        name="Energy Source Component 2",
        outputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        flow_costs={"electricity": 1},
    )

    central_bus = components.Bus(
        name="Central Bus",
        inputs=(
            "Energy Source Component 1.electricity",
            "Energy Source Component 2.electricity",
            "Energy Storage Component.electricity",
        ),
        outputs=(
            "Energy Storage Component.electricity",
            "Energy Demand Component.electricity",
        ),
    )

    # 4. Creating the actual energy system:
    storage_emissions_msc = system_model.AbstractEnergySystem(
        uid="Storage Emissions MSC",
        busses=(central_bus,),
        sinks=(demand,),
        sources=(
            source_1,
            source_2,
        ),
        storages=(storage,),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return storage_emissions_msc
