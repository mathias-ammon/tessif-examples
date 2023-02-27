# src/tessif_examples/simple_transformer_grid_es.py
"""Tessif minimum working example energy system model."""
import tessif.frused.namedtuples as nts
from pandas import date_range
from tessif import components, system_model


def create_simple_transformer_grid_es():
    """Create a simplified grid energy system  for testing.

    Emulates common grid (congestion) behaviours, during its 6 timesteps:

        1. Everything provided by HV-Source
        2. Too much provided by HV-Source; H2M grid congests
           and MV-BS and MV-XS need to compensate
        3. Too little provided, so MV-BS needs to provide
        4. Everything provided by MV-Source
        5. Too much provided by MV-Source, M2H grid congests
           and HV-BS and HV-XS need to compensate
        6. Too little provided, so MV-BS needs to provide

    Returns
    -------
    tessif.system_model.AbstractEnergySystem
        Tessif energy system model (scenario comibnation) emulating common
        grid analysis topics.

    Example
    -------
    Generic System Visualization:

    .. image:: ../../_static/system_model_graphs/simple_transformer_grid_es.png
        :align: center
        :alt: Image showing the simple transformer grid es generic graph
    """
    # predefine high -> med and med -> high efficiencies for cleaner
    # code and integer results
    eta_h2m = 10 / 12
    eta_m2h = 10 / 11

    # define optimization timespan
    opt_timespan = date_range("7/13/1990", periods=6, freq="H")

    # 3. Creating the individual energy system components:
    hv_source = components.Source(
        name="HV-Source",
        outputs=("hv-electricity",),
        flow_rates={"hv-electricity": nts.MinMax(min=0, max=30)},
        # Minimum number of arguments required
        timeseries={
            "hv-electricity": nts.MinMax(
                min=[10 + 10 / eta_h2m, 30, 10, 0, 0, 0],
                max=[10 + 10 / eta_h2m, 30, 10, 0, 0, 0],
            ),
        },
    )

    mv_source = components.Source(
        name="MV-Source",
        outputs=("mv-electricity",),
        flow_rates={"mv-electricity": nts.MinMax(min=0, max=30)},
        timeseries={
            "mv-electricity": nts.MinMax(
                min=[
                    0,
                    0,
                    0,
                    10 + 10 / eta_m2h,
                    30,
                    10,
                ],
                max=[
                    0,
                    0,
                    0,
                    10 + 10 / eta_m2h,
                    30,
                    10,
                ],
            ),
        },
    )

    hv_balance_source = components.Source(
        name="HV-BS",
        outputs=("hv-electricity",),
        flow_rates={"hv-electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={"hv-electricity": 10},
    )

    mv_balance_source = components.Source(
        name="MV-BS",
        outputs=("mv-electricity",),
        flow_rates={"mv-electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={"mv-electricity": 10},
    )

    high_to_med = components.Transformer(
        name="H2M",
        inputs=("hv-electricity",),
        outputs=("mv-electricity",),
        conversions={("hv-electricity", "mv-electricity"): eta_h2m},
        flow_rates={
            "hv-electricity": nts.MinMax(min=0, max=float("+inf")),
            "mv-electricity": nts.MinMax(min=0, max=10),
        },
    )

    med_to_high = components.Transformer(
        name="M2H",
        inputs=("mv-electricity",),
        outputs=("hv-electricity",),
        conversions={("mv-electricity", "hv-electricity"): eta_m2h},
        flow_rates={
            "mv-electricity": nts.MinMax(min=0, max=float("+inf")),
            "hv-electricity": nts.MinMax(min=0, max=10),
        },
    )

    mv_demand = components.Sink(
        name="MV-Demand",
        inputs=("mv-electricity",),
        # Minimum number of arguments required
        flow_rates={"mv-electricity": nts.MinMax(min=10, max=10)},
        timeseries={
            "mv-electricity": nts.MinMax(
                min=[10, 12, 10, 10, 10, 10],
                max=[10, 12, 10, 10, 10, 10],
            ),
        },
    )

    hv_demand = components.Sink(
        name="HV-Demand",
        inputs=("hv-electricity",),
        # Minimum number of arguments required
        flow_rates={"hv-electricity": nts.MinMax(min=10, max=10)},
        timeseries={
            "hv-electricity": nts.MinMax(
                min=[10, 10, 10, 10, 12, 10],
                max=[10, 10, 10, 10, 12, 10],
            ),
        },
    )

    hv_excess_sink = components.Sink(
        name="HV-XS",
        inputs=("hv-electricity",),
        flow_rates={"hv-electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={"hv-electricity": 10},
    )

    mv_excess_sink = components.Sink(
        name="MV-XS",
        inputs=("mv-electricity",),
        flow_rates={"mv-electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={"mv-electricity": 10},
    )

    hv_bus = components.Bus(
        name="HV-Bus",
        inputs=(
            "HV-Source.hv-electricity",
            "M2H.hv-electricity",
            "HV-BS.hv-electricity",
        ),
        outputs=(
            "H2M.hv-electricity",
            "HV-Demand.hv-electricity",
            "HV-XS.hv-electricity",
        ),
    )

    mv_bus = components.Bus(
        name="MV-Bus",
        inputs=(
            "MV-Source.mv-electricity",
            "H2M.mv-electricity",
            "MV-BS.mv-electricity",
        ),
        outputs=(
            "M2H.mv-electricity",
            "MV-Demand.mv-electricity",
            "MV-XS.mv-electricity",
        ),
    )

    # 4. Creating the actual energy system:
    model_scenario_combination = system_model.AbstractEnergySystem(
        uid="Two Transformer Grid Example",
        busses=(hv_bus, mv_bus),
        sinks=(hv_demand, mv_demand, hv_excess_sink, mv_excess_sink),
        sources=(hv_source, mv_source, hv_balance_source, mv_balance_source),
        transformers=(med_to_high, high_to_med),
        timeframe=opt_timespan,
    )

    return model_scenario_combination
