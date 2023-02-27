# src/tessif_examples/expansion_plan_example.py
"""Tessif minimum working example energy system model."""
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_expansion_plan_example():
    """Create a minimum expansion problem example.

    Create a small energy system utilizing two emisison free and expandable
    sources, as well as an emitting one.

    Returns
    -------
    :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system.

    Examples
    --------
    Generic System Visualization:

    .. image:: ../../_static/system_model_graphs/expansion_plan_example.png
        :align: center
        :alt: Image showing the expansion plan example energy system graph.
    """
    # 2. Create a simulation time frame of 2 one hour time steps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = date_range("7/13/1990", periods=4, freq="H")

    # 3. Creating the individual energy system components:

    # emitting source having no costs and no flow constraints but emissions
    emitting_source = components.Source(
        name="Emitting Source",
        outputs=("electricity",),
        # Minimum number of arguments required
        flow_emissions={"electricity": 1},
    )

    # capped source having no costs, no emission, no flow constraints
    # but existing and max installed capacity (for expansion) as well
    # as expansion costs
    capped_renewable = components.Source(
        name="Capped Renewable",
        outputs=("electricity",),
        # Minimum number of arguments required
        flow_rates={"electricity": nts.MinMax(min=1, max=2)},
        flow_costs={
            "electricity": 2,
        },
        expandable={"electricity": True},
        expansion_costs={"electricity": 1},
        expansion_limits={"electricity": nts.MinMax(min=1, max=4)},
    )

    # uncapped source having no costs and no emissions
    # but an externally set timeseries as well as expansion costs
    uncapped_min, uncapped_max = [1, 2, 3, 1], [1, 2, 3, 1]

    uncapped_renewable = components.Source(
        name="Uncapped Renewable",
        outputs=("electricity",),
        # Minimum number of arguments required
        # flow_rates={'electricity': nts.MinMax(min=0, max=1)},
        flow_costs={
            "electricity": 2,
        },
        expandable={"electricity": True},
        expansion_costs={"electricity": 2},
        timeseries={"electricity": nts.MinMax(min=uncapped_min, max=uncapped_max)},
        expansion_limits={
            "electricity": nts.MinMax(
                min=max(uncapped_max),
                max=float("+inf"),
            )
        },
    )

    electricity_line = components.Bus(
        name="Powerline",
        inputs=(
            "Emitting Source.electricity",
            "Capped Renewable.electricity",
            "Uncapped Renewable.electricity",
        ),
        outputs=("Demand.electricity",),
        # Minimum number of arguments required
    )

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        flow_rates={"electricity": nts.MinMax(min=10, max=10)},
    )

    global_constraints = {"emissions": 20}

    # 4. Creating the actual energy system:
    explicit_es = system_model.AbstractEnergySystem(
        uid="Expansion Plan Example",
        busses=(electricity_line,),
        sinks=(demand,),
        sources=(
            emitting_source,
            capped_renewable,
            uncapped_renewable,
        ),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return explicit_es
