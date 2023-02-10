# src/tessif_examples/expansion_plan_example.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_expansion_plan_example(directory=None, filename=None):
    """
    Create a small energy system utilizing two emisison free and
    expandable sources, as well as an emitting one.

    Returns
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`AutoCompare_Expansion` - For simulating and
    comparing this energy system using different supported models.

    :ref:`Examples_Application_Components`,  - For a comprehensive example
    on a reference energy system to analyze and compare commitment
    optimization among models.

    Examples
    --------
    Use :func:`create_expansion_plan_example` to quickly access a tessif
    energy system to use for doctesting, or trying out this framework's
    utilities.

    (For a step by step explanation see :ref:`Models_Tessif_mwe`):

        import tessif.examples.data.tsf.py_hard as tsf_py
        es = tsf_py.create_expansion_plan_example()

        for node in es.nodes:
            print(str(node.uid))
        Powerline
        Emitting Source
        Capped Renewable
        Uncapped Renewable
        Demand

    Visualize the energy system for better understanding what the output means::

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_expansion_plan_example(),
            color_group={
              'Powerline': '#009900',
                'Emitting Source': '#cc0033',
                'Demand': '#00ccff',
                'Capped Renewable': '#ffD700',
                'Uncapped Renewable': '#ffD700',
            },
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)


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
    explicit_es = energy_system.AbstractEnergySystem(
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
