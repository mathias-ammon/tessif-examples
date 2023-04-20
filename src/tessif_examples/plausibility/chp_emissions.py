# src/tessif_examples/plausbility/mwe.py
"""Tessif chp emissions plausibility check MSC."""
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_chp_emissions():
    """Create a chp-emissions plausibility check MSC.

    Returns
    -------
    :class:`tessif.system_model.AbstractEnergySystem`
        Chp-Emissions plausibility check MSC.

    Example
    -------

    .. image:: ../../_static/system_model_graphs/chp_emissions.png
        :align: center
        :alt: Image showing the mwe energy system graph
    """
    # 2. Create a simulation time frame of 2 one hour time steps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=4, freq="H")

    global_constraints = {
        "name": "emissions_constraint",
        "emissions": 54,
    }

    power_demand = components.Sink(
        name="Power Demand Component",
        inputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    heat_demand = components.Sink(
        name="Heat Demand Component",
        inputs=("hot_water",),
        flow_rates={"hot_water": nts.MinMax(min=8, max=8)},
    )

    chp = components.Transformer(
        name="CHP",
        inputs=("gas",),
        outputs=("electricity", "hot_water"),
        conversions={
            ("gas", "electricity"): 0.5,
            ("gas", "hot_water"): 0.4,
        },
        flow_rates={
            "gas": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=10),
            "hot_water": nts.MinMax(min=0, max=8),
        },
        flow_emissions={"electricity": 1, "hot_water": 1, "gas": 0},
    )

    gas_source = components.Source(
        name="Gas Commodity",
        outputs=("gas",),
        flow_rates={"gas": nts.MinMax(min=0, max=float("+inf"))},
    )

    power_source = components.Source(
        name="Power Source Component",
        outputs=("electricity",),
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        flow_costs={"electricity": 1},
    )

    heat_source = components.Source(
        name="Heat Source Component",
        outputs=("hot_water",),
        flow_rates={"hot_water": nts.MinMax(min=0, max=8)},
        flow_costs={"hot_water": 1},
    )

    gas_bus = components.Bus(
        name="Gas Bus",
        inputs=("Gas Commodity.gas",),
        outputs=("CHP.gas",),
    )

    power_bus = components.Bus(
        name="Power Bus",
        inputs=(
            "Power Source Component.electricity",
            "CHP.electricity",
        ),
        outputs=("Power Demand Component.electricity",),
    )

    heat_bus = components.Bus(
        name="Heat Bus",
        inputs=(
            "Heat Source Component.hot_water",
            "CHP.hot_water",
        ),
        outputs=("Heat Demand Component.hot_water",),
    )

    # 4. Creating the actual energy system:
    chp_emissions_msc = system_model.AbstractEnergySystem(
        uid="Chp Emissions MSC",
        busses=(gas_bus, power_bus, heat_bus),
        sinks=(power_demand, heat_demand),
        sources=(gas_source, power_source, heat_source),
        chps=(chp,),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return chp_emissions_msc
