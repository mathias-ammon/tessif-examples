# src/tessif_examples/basic/variable_chp.py
"""Tessif minimum working example energy system model."""

import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model

# from tessif_examples.data.model import components


def create_variable_chp():
    """Create a specialized variable chp example.

    Same as create_chp() but with two chps that use additional functionality
    from tessif's :class:`tessif.components.CHP` class.

    Return
    ------
    :class:`tessif.model.system_model.AbstractEnergySystem`
        Tessif energy system.

    Examples
    --------
    Generic System Visualization:

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
    explicit_es = system_model.AbstractEnergySystem(
        uid="Variable_CHP_Example",
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
