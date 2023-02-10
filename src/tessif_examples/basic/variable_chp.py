# src/tessif_examples/variable_chp.py
"""Tessif minimum working example energy system model."""
import numpy as np
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import energy_system

from tessif_examples.data.model import components


def create_variable_chp(directory=None, filename=None):
    """Same as create_chp() but with two chps that use additional functionality
    from tessif's :class:`tessif.model.components.CHP` class.

    Return
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`AutoCompare_CHP` - For simulating and
    comparing this energy system using different supported models.

    Examples
    --------
    Using :func:`create_chp` to quickly access a tessif energy system
    to use for doctesting, or trying out this frameworks utilities.

    (For a step by step explanation see :ref:`Models_Tessif_mwe`):

        import tessif.examples.data.tsf.py_hard as tsf_py
        es = tsf_py.create_variable_chp()

        for node in es.nodes:
            print(node.uid)
        Gas Grid
        Powerline
        Heat Grid
        CHP1
        CHP2
        Gas Source
        Backup Power
        Backup Heat
        Power Demand
        Heat Demand

    Visualize the energy system for better understanding what the output means::

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_variable_chp(),
            color_group={
                'Gas Source': '#336666',
                'Gas Grid': '#336666',
                'CHP1': '#006666',
                'CHP2': '#006666',
                'Backup Power': '#ffcc00',
                'Power Demand': '#ff6600',
                'Powerline': '#009900',
                'Backup Heat': '#b30000',
                'Heat Demand': '#b30000',
                'Heat Grid': '#b30000',
            },
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/variable_chp.png
        :align: center
        :alt: Image showing the variable_chp energy system graph

    """
    # 2. Create a simulation time frame of four one-hour timesteps as a
    # :class:`pandas.DatetimeIndex`:
    periods = 4
    timeframe = date_range("7/13/1990", periods=periods, freq="H")

    global_constraints = {"emissions": float("+inf")}

    # 3. Create the individual energy system components:
    gas_supply = components.Source(
        name="Gas Source",
        outputs=("gas",),
        # Minimum number of arguments required
    )

    gas_grid = components.Bus(
        name="Gas Grid",
        inputs=("Gas Source.gas",),
        outputs=("CHP1.gas", "CHP2.gas"),
        # Minimum number of arguments required
    )

    # conventional power supply is cheaper, but has emissions allocated to it
    chp1 = components.CHP(
        name="CHP1",
        inputs=("gas",),
        outputs=("electricity", "heat"),
        # Minimum number of arguments required
        conversions={
            ("gas", "electricity"): 0.3,
            ("gas", "heat"): 0.2,
        },
        conversion_factor_full_condensation={("gas", "electricity"): 0.5},
        flow_rates={"electricity": (0, 9), "heat": (0, 6), "gas": (0, float("+inf"))},
        flow_costs={"electricity": 3, "heat": 2, "gas": 0},
        flow_emissions={"electricity": 2, "heat": 3, "gas": 0},
    )

    chp2 = components.CHP(
        name="CHP2",
        inputs=("gas",),
        outputs=("electricity", "heat"),
        # Minimum number of arguments required
        enthalpy_loss=nts.MinMax(
            [1.0 for p in range(0, periods)], [0.18 for p in range(0, periods)]
        ),
        power_wo_dist_heat=nts.MinMax(
            [8 for p in range(0, periods)], [20 for p in range(0, periods)]
        ),
        el_efficiency_wo_dist_heat=nts.MinMax(
            [0.43 for p in range(0, periods)], [0.53 for p in range(0, periods)]
        ),
        min_condenser_load=[3 for p in range(0, periods)],
        power_loss_index=[0.19 for p in range(0, periods)],
        back_pressure=False,
        flow_costs={"electricity": 3, "heat": 2, "gas": 0},
        flow_emissions={"electricity": 2, "heat": 3, "gas": 0},
    )

    # back up power, expensive
    backup_power = components.Source(
        name="Backup Power",
        outputs=("electricity",),
        flow_costs={"electricity": 10},
    )

    # Power demand needing 20 energy units per time step
    power_demand = components.Sink(
        name="Power Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        flow_rates={"electricity": nts.MinMax(min=20, max=20)},
    )

    power_line = components.Bus(
        name="Powerline",
        inputs=("Backup Power.electricity", "CHP1.electricity", "CHP2.electricity"),
        outputs=("Power Demand.electricity",),
        # Minimum number of arguments required
        sector="Power",
    )

    # Back up heat source, expensive
    backup_heat = components.Source(
        name="Backup Heat",
        outputs=("heat",),
        flow_costs={"heat": 10},
    )

    # Heat demand needing 10 energy units per time step
    heat_demand = components.Sink(
        name="Heat Demand",
        inputs=("heat",),
        # Minimum number of arguments required
        flow_rates={"heat": nts.MinMax(min=10, max=10)},
    )

    heat_grid = components.Bus(
        name="Heat Grid",
        inputs=("CHP1.heat", "CHP2.heat", "Backup Heat.heat"),
        outputs=("Heat Demand.heat",),
        # Minimum number of arguments required
        sector="Heat",
    )

    # 4. Create the actual energy system:
    explicit_es = energy_system.AbstractEnergySystem(
        uid="CHP_Example",
        busses=(gas_grid, power_line, heat_grid),
        chps=(
            chp1,
            chp2,
        ),
        sinks=(power_demand, heat_demand),
        sources=(gas_supply, backup_power, backup_heat),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return explicit_es
