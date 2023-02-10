# src/tessif_examples/scenarios/hhes.py
# pylint: disable=too-many-locals
# pylint: disable=duplicate-code
# pylint: disable=too-many-lines
"""Generic grid tessif energy system model example."""
import os

import numpy as np
import pandas as pd
import tessif.namedtuples as nts
from oemof.tools import economics
from pandas import date_range
from tessif.model import components, energy_system

from tessif_examples.data.frused.paths import example_dir


def create_hhes(periods=24, directory=None, filename=None):
    """
    Create a model of Hamburg's energy system using :mod:`tessif's
    model <tessif.model>`.

    Parameters
    ----------
    periods : int, default=24
        Number of time steps of the evaluated timeframe (one time step is one
        hour)

    Return
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`AutoCompare_HH` - For simulating and
    comparing this energy system using different supported models.

    Examples
    --------
    Use :func:`create_hhes` to quickly access a tessif energy system
    to use for doctesting, or trying out this framework's utilities.

        import tessif.examples.data.tsf.py_hard as tsf_py
        es = tsf_py.create_hhes()

        for node in es.nodes:
            print(node.uid)
        coal supply line
        gas pipeline
        oil supply line
        waste supply
        powerline
        district heating pipeline
        biomass logistics
        gas supply
        coal supply
        oil supply
        waste
        pv1
        won1
        biomass supply
        imported el
        imported heat
        demand el
        demand th
        excess el
        excess th
        chp1
        chp2
        chp3
        chp4
        chp5
        chp6
        pp1
        pp2
        pp3
        pp4
        hp1
        p2h
        biomass chp
        est

    Visualize the energy system for better understanding what the output means:

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_hhes(),
            color_group={
                'coal supply': '#404040',
                'coal supply line': '#404040',
                'pp1': '#404040',
                'pp2': '#404040',
                'chp3': '#404040',
                'chp4': '#404040',
                'chp5': '#404040',
                'hp1': '#b30000',
                'imported heat': '#b30000',
                'district heating pipeline': 'Red',
                'demand th': 'Red',
                'excess th': 'Red',
                'p2h': '#b30000',
                'bm1': '#006600',
                'won1': '#99ccff',
                'gas supply': '#336666',
                'gas pipeline': '#336666',
                'chp1': '#336666',
                'chp2': '#336666',
                'waste': '#009900',
                'waste supply': '#009900',
                'chp6': '#009900',
                'oil supply': '#666666',
                'oil supply line': '#666666',
                'pp3': '#666666',
                'pp4': '#666666',
                'pv1': '#ffd900',
                'imported el': '#ffd900',
                'demand el': '#ffe34d',
                'excess el': '#ffe34d',
                'est': '#ffe34d',
                'powerline': '#ffcc00',
            },
            title='Generic Grid Example Energy System Graph',
        )
        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/hh_es_example.png
        :align: center
        :alt: Image showing the create_hhes energy system graph.

    """
    # 2. Create a simulation time frame as a :class:`pandas.DatetimeIndex`:
    timeframe = pd.date_range("2019-01-01", periods=periods, freq="H")

    # 3. Parse csv files with the demand and renewables load data:
    d = os.path.join(example_dir, "data", "tsf", "load_profiles")

    # solar:
    pv_HH = pd.read_csv(os.path.join(d, "solar_HH_2019.csv"), index_col=0, sep=";")
    pv_HH = pv_HH.values.flatten()[0:periods]
    max_pv = np.max(pv_HH)

    # wind onshore:
    wo_HH = pd.read_csv(os.path.join(d, "wind_HH_2019.csv"), index_col=0, sep=";")
    wo_HH = wo_HH.values.flatten()[0:periods]
    max_wo = np.max(wo_HH)

    # electricity demand:
    de_HH = pd.read_csv(os.path.join(d, "el_demand_HH_2019.csv"), index_col=0, sep=";")
    de_HH = de_HH["Last (MW)"].values.flatten()[0:periods]
    de_HH = np.array(de_HH)
    max_de = np.max(de_HH)

    # heat demand:
    th_HH = pd.read_csv(os.path.join(d, "th_demand_HH_2019.csv"), index_col=0, sep=";")
    th_HH = th_HH["actual_total_load"].values.flatten()[0:periods]
    th_HH = np.array(th_HH)
    max_th = np.max(th_HH)

    # 4. Create the individual energy system components:
    in_stat = False
    cfba = 0

    # Global Constraints:

    global_constraints = {
        "name": "2019",
        "emissions": float("+inf"),
        # 'resources': float('+inf'),
    }

    # Fossil Sources:

    gass = components.Source(
        name="gas supply",
        outputs=("gas",),
        region="HH",
        node_type="gas_supply",
        component="source",
        sector="coupled",
        carrier="gas",
        flow_emissions={"gas": 0.2},
    )

    coals = components.Source(
        name="coal supply",
        outputs=("coal",),
        region="HH",
        node_type="coal_supply",
        component="source",
        sector="coupled",
        carrier="coal",
        flow_emissions={"coal": 0.34},
    )

    oils = components.Source(
        name="oil supply",
        outputs=("oil",),
        region="HH",
        node_type="oil_supply",
        component="source",
        sector="power",
        carrier="oil",
    )

    waste = components.Source(
        name="waste",
        outputs=("waste",),
        region="HH",
        node_type="renewable",
        component="source",
        sector="coupled",
        carrier="waste",
        flow_emissions={"waste": 0.0426},
    )

    # HKW ADM:

    chp1 = components.Transformer(
        name="chp1",
        inputs=("gas",),
        outputs=("electricity", "hot_water"),
        conversions={
            ("gas", "electricity"): 0.3773,
            ("gas", "hot_water"): 0.3,
        },  # conventional_power_plants_DE.xls
        latitude=53.51,
        longitude=9.94985,
        region="HH",
        node_type="HKW ADM",
        component="transformer",
        sector="coupled",
        carrier="gas",
        flow_rates={
            "gas": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),  # 6.75
            "hot_water": nts.MinMax(min=0, max=float("+inf")),
        },
        flow_costs={"gas": 0, "electricity": 90, "hot_water": 21.6},
        # emissions are attributed to gas supply
        # so pypsa can handle them better
        flow_emissions={
            "gas": 0,  # 0.2,
            "electricity": 0,  # 0.2/0.3773,
            "hot_water": 0,
        },  # 0.2/0.3},
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 1),
        status_changing_costs=nts.OnOff(24, 0),
        costs_for_being_active=cfba,
    )

    # HKW Moorburg:

    pp1 = components.Transformer(
        name="pp1",
        inputs=("coal",),
        outputs=("electricity",),
        conversions={("coal", "electricity"): 0.4625},
        latitude=53.489,
        longitude=9.949,
        region="HH",
        node_type="HKW Moorburg Block A",
        component="transformer",
        sector="power",
        carrier="coal",
        flow_rates={
            "coal": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=784),  # 296
        },
        flow_costs={"coal": 0, "electricity": 82},
        flow_emissions={"coal": 0, "electricity": 0.34 / 0.4625},  # 0.34,
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 7),
        status_changing_costs=nts.OnOff(49, 0),
        costs_for_being_active=cfba,
    )

    pp2 = components.Transformer(
        name="pp2",
        inputs=("coal",),
        outputs=("electricity",),
        conversions={("coal", "electricity"): 0.4625},
        latitude=53.489,
        longitude=9.949,
        region="HH",
        node_type="HKW Moorburg Block B",
        component="transformer",
        sector="power",
        carrier="coal",
        flow_rates={
            "coal": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=784),  # 296
        },
        flow_costs={"coal": 0, "electricity": 82},
        flow_emissions={"coal": 0, "electricity": 0.34 / 0.4625},  # 0.34,
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 7),
        status_changing_costs=nts.OnOff(49, 0),
        costs_for_being_active=cfba,
    )

    # HKW Tiefstack:

    chp2 = components.Transformer(
        name="chp2",
        inputs=("gas",),
        outputs=(
            "electricity",
            "hot_water",
        ),
        conversions={
            ("gas", "electricity"): 0.585,
            ("gas", "hot_water"): 0.40,
        },
        latitude=53.53,
        longitude=10.07,
        region="HH",
        node_type="HKW Tiefstack GuD",
        component="transformer",
        sector="coupled",
        carrier="gas",
        flow_rates={
            "gas": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=123),  # 51
            "hot_water": nts.MinMax(min=0, max=180),
        },
        flow_costs={
            "gas": 0,
            "electricity": 90,
            "hot_water": 18.9,
        },
        # emissions are attributed to gas supply
        # so pypsa can handle them better
        flow_emissions={
            "gas": 0,  # 0.2,
            "electricity": 0,  # 0.2/0.585,
            "hot_water": 0,  # 0.2/0.4,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 5),
        status_changing_costs=nts.OnOff(40, 0),
        costs_for_being_active=cfba,
    )

    chp3 = components.Transformer(
        name="chp3",
        inputs=("coal",),
        outputs=(
            "electricity",
            "hot_water",
        ),
        conversions={
            ("coal", "electricity"): 0.4075,
            ("coal", "hot_water"): 0.40,
        },
        latitude=53.53,
        longitude=10.06,
        region="HH",
        node_type="HKW Tiefstack Block 2",
        component="transformer",
        sector="coupled",
        carrier="coal",
        flow_rates={
            "coal": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=188),  # 68
            "hot_water": nts.MinMax(min=0, max=293),
        },
        flow_costs={
            "coal": 0,
            "electricity": 82,
            "hot_water": 19.68,
        },
        # emissions are attributed to coal supply
        # so pypsa can handle them better
        flow_emissions={
            "coal": 0,  # 0.34,
            "electricity": 0,  # 0.34/0.4075,
            "hot_water": 0,  # 0.34/0.4,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 7),
        status_changing_costs=nts.OnOff(49, 0),
        costs_for_being_active=cfba,
    )

    # Wedel GT:

    pp3 = components.Transformer(
        name="pp3",
        inputs=("oil",),
        outputs=("electricity",),
        conversions={("oil", "electricity"): 0.3072},
        latitude=53.5662,
        longitude=9.72864,
        region="SH",
        node_type="Wedel GT A",
        component="transformer",
        sector="power",
        carrier="oil",
        flow_rates={
            "oil": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=50.5),  # 20.2
        },
        flow_costs={"oil": 0, "electricity": 90},
        flow_emissions={
            "oil": 0,  # 0.28,
            "electricity": 0.28 / 0.3072,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 9),
        status_changing_costs=nts.OnOff(45, 0),
        costs_for_being_active=cfba,
    )

    pp4 = components.Transformer(
        name="pp4",
        inputs=("oil",),
        outputs=("electricity",),
        conversions={("oil", "electricity"): 0.3072},
        latitude=53.5662,
        longitude=9.72864,
        region="SH",
        node_type="Wedel GT B",
        component="transformer",
        sector="power",
        carrier="oil",
        flow_rates={
            "oil": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=50.5),  # 20.2
        },
        flow_costs={"oil": 0, "electricity": 90},
        flow_emissions={
            "oil": 0,  # 0.28,
            "electricity": 0.28 / 0.3072,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 9),
        status_changing_costs=nts.OnOff(45, 0),
        costs_for_being_active=cfba,
    )

    # HKW Wedel:

    chp4 = components.Transformer(
        name="chp4",
        inputs=("coal",),
        outputs=(
            "electricity",
            "hot_water",
        ),
        conversions={
            ("coal", "electricity"): 0.4075,
            ("coal", "hot_water"): 0.40,
        },
        latitude=53.5667,
        longitude=9.72864,
        region="SH",
        node_type="HKW Wedel Block 1",
        component="transformer",
        sector="coupled",
        carrier="coal",
        flow_rates={
            "coal": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=130),  # 57
            "hot_water": nts.MinMax(min=0, max=130),
        },
        flow_costs={
            "coal": 0,
            "electricity": 82,
            "hot_water": 19.68,
        },
        # emissions are attributed to coal supply
        # so pypsa can handle them better
        flow_emissions={
            "coal": 0,  # 0.34,
            "electricity": 0,  # 0.34/0.4075,
            "hot_water": 0,  # 0.34/0.40,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 7),
        status_changing_costs=nts.OnOff(49, 0),
        costs_for_being_active=cfba,
    )

    chp5 = components.Transformer(
        name="chp5",
        inputs=("coal",),
        outputs=("electricity", "hot_water"),
        conversions={
            ("coal", "electricity"): 0.4075,
            ("coal", "hot_water"): 0.40,
        },
        latitude=53.5667,
        longitude=9.72864,
        region="SH",
        node_type="HKW Wedel Block 2",
        component="transformer",
        sector="coupled",
        carrier="coal",
        flow_rates={
            "coal": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=118),  # 44
            "hot_water": nts.MinMax(min=0, max=88),
        },
        flow_costs={
            "coal": 0,
            "electricity": 82,
            "hot_water": 19.68,
        },
        # emissions are attributed to coal supply
        # so pypsa can handle them better
        flow_emissions={
            "coal": 0,  # 0.34,
            "electricity": 0,  # 0.34/0.4075,
            "hot_water": 0,  # 0.34/0.40,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 7),
        status_changing_costs=nts.OnOff(49, 0),
        costs_for_being_active=cfba,
    )

    # MVR Waste Combustion Rugenberger Damm:

    chp6 = components.Transformer(
        name="chp6",
        inputs=("waste",),
        outputs=(
            "electricity",
            "hot_water",
        ),
        conversions={
            ("waste", "electricity"): 0.06,
            ("waste", "hot_water"): 0.15,
        },
        latitude=53.52111,
        longitude=9.93339,
        region="HH",
        node_type="MVR Müllverwertung Rugenberger Damm",
        component="transformer",
        sector="coupled",
        carrier="waste",
        flow_rates={
            "waste": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=24),  # 9.6
            "hot_water": nts.MinMax(min=0, max=70),
        },
        flow_costs={
            "waste": 0,
            "electricity": 82,
            "hot_water": 20,
        },
        # emissions are attributed to waste supply
        # so pypsa can handle them better
        flow_emissions={
            "waste": 0,  # 0.0426,
            "electricity": 0,  # 0.0426/0.06,
            "hot_water": 0,  # 0.0426/0.15,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 9),
        status_changing_costs=nts.OnOff(40, 0),
        costs_for_being_active=cfba,
    )

    # Heizwerk Hafencity:
    hp1 = components.Transformer(
        name="hp1",
        inputs=("gas",),
        outputs=("hot_water",),
        conversions={
            ("gas", "hot_water"): 0.96666,
        },
        latitude=53.54106052,
        longitude=9.99590096,
        region="HH",
        node_type="Heizwerk Hafencity",
        component="transformer",
        sector="heat",
        carrier="gas",
        flow_rates={
            "gas": nts.MinMax(min=0, max=float("+inf")),
            "hot_water": nts.MinMax(min=0, max=348),  # max=348
        },
        flow_costs={
            "gas": 0,
            "hot_water": 20,
        },
        flow_emissions={
            "gas": 0.0,  # 0.2
            "hot_water": 0.2 / 0.96666,
        },
        expandable={"gas": False, "hot_water": True},
        expansion_costs={
            "gas": 0,
            "hot_water": 0,
        },
        expansion_limits={
            "gas": nts.MinMax(min=0, max=float("+inf")),
            "hot_water": nts.MinMax(min=348, max=float("+inf")),
        },
    )

    # Biomass Combined Heat and Power
    bm_chp = components.Transformer(
        name="biomass chp",
        latitude=53.54106052,
        longitude=9.99590096,
        region="HH",
        node_type="Heizwerk Hafencity",
        component="transformer",
        sector="heat",
        carrier="gas",
        inputs=("biomass",),
        outputs=(
            "electricity",
            "hot_water",
        ),
        conversions={
            ("biomass", "electricity"): 48.4 / 126,
            ("biomass", "hot_water"): 1,
        },
        flow_rates={
            "biomass": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=48.4),
            "hot_water": nts.MinMax(min=0, max=126),
        },
        flow_costs={
            "biomass": 0,
            "electricity": 61,  # 61
            "hot_water": 20,  # 61
        },
        flow_emissions={
            "biomass": 0,
            # emissions reallocated to source
            "electricity": 0,  # 0.001,
            "hot_water": 0,  # 0.001,
        },
        initial_status=in_stat,
        status_inertia=nts.OnOff(0, 9),
        status_changing_costs=nts.OnOff(40, 0),
    )

    # Renewables:

    pv1 = components.Source(
        name="pv1",
        outputs=("electricity",),
        region="HH",
        node_type="renewable",
        component="source",
        sector="power",
        carrier="solar",
        flow_rates={"electricity": nts.MinMax(min=0, max=max_pv)},
        flow_costs={"electricity": 74},
        flow_emissions={"electricity": 0},
        timeseries={"electricity": nts.MinMax(min=pv_HH, max=pv_HH)},
        expandable={"electricity": True},
        expansion_costs={
            "electricity": economics.annuity(capex=1000000, n=20, wacc=0.05)
        },
        expansion_limits={"electricity": nts.MinMax(min=max_pv, max=float("+inf"))},
    )

    won1 = components.Source(
        name="won1",
        outputs=("electricity",),
        region="HH",
        node_type="renewable",
        component="source",
        sector="power",
        carrier="wind",
        flow_rates={"electricity": nts.MinMax(min=0, max=max_wo)},
        flow_costs={"electricity": 61},
        flow_emissions={"electricity": 0.007},  # 0.007
        timeseries={"electricity": nts.MinMax(min=wo_HH, max=wo_HH)},
        expandable={"electricity": True},
        expansion_costs={
            "electricity": economics.annuity(capex=1750000, n=20, wacc=0.05)
        },
        expansion_limits={"electricity": nts.MinMax(min=max_wo, max=float("+inf"))},
    )

    bm_supply = components.Source(
        name="biomass supply",
        outputs=("biomass",),
        region="HH",
        node_type="renewable",
        component="source",
        sector="coupled",
        carrier="biomass",
        # reallocating the biomass chp emissions to the source
        flow_emissions={"biomass": 0.001 / 1 + 0.001 / (48.8 / 126)},
    )

    # Storages:

    est = components.Storage(
        name="est",
        input="electricity",
        output="electricity",
        capacity=1,
        initial_soc=1,
        region="HH",
        sector="power",
        carrier="electricity",
        component="storage",
        flow_rates={"electricity": nts.MinMax(0, float("+inf"))},
        flow_costs={"electricity": 20},
        flow_emissions={"electricity": 0},
        expendable={"capacity": True, "electricity": False},
        expansion_costs={"capacity": economics.annuity(capex=1000000, n=10, wacc=0.05)},
    )

    # P2H Karoline:

    p2h = components.Transformer(
        name="p2h",
        inputs=("electricity",),
        outputs=("hot_water",),
        conversions={
            ("electricity", "hot_water"): 0.99,
        },
        latitude=53.55912,
        longitude=9.97148,
        region="HH",
        node_type="power2heat",
        component="transformer",
        sector="heat",
        carrier="hot_water",
        flow_rates={
            "electricity": nts.MinMax(min=0, max=float("+inf")),
            "hot_water": nts.MinMax(min=0, max=45),
        },  # 45
        flow_costs={"electricity": 0, "hot_water": 0},
        flow_emissions={"electricity": 0, "hot_water": 0},  # 0.007
        expandable={"electricity": False, "hot_water": True},
        expansion_costs={"hot_water": economics.annuity(capex=200000, n=30, wacc=0.05)},
        expansion_limits={"hot_water": nts.MinMax(min=45, max=200)},
    )

    # Imported Electricity/ Heat:

    imel = components.Source(
        name="imported el",
        outputs=("electricity",),
        region="HH",
        node_type="import",
        component="source",
        sector="power",
        carrier="electricity",
        flow_costs={"electricity": 999},
        flow_emissions={"electricity": 0.401},
        expendable={"electricity": True},
        expansion_costs={"electricity": 999999999},
    )

    imth = components.Source(
        name="imported heat",
        outputs=("hot_water",),
        region="HH",
        node_type="import",
        component="source",
        sector="heat",
        carrier="hot_water",  # ('hot_water', 'steam'),
        flow_costs={"hot_water": 999},
        flow_emissions={"hot_water": 0.1},
        expendable={"hot_water": True},
        expansion_costs={"hot_water": 999999999},
    )

    # Sinks:

    demand_el = components.Sink(
        name="demand el",
        inputs=("electricity",),
        region="HH",
        node_type="demand",
        component="sink",
        sector="power",
        carrier="electricity",
        flow_rates={"electricity": nts.MinMax(min=0, max=max_de)},
        timeseries={"electricity": nts.MinMax(min=de_HH, max=de_HH)},
    )

    demand_th = components.Sink(
        name="demand th",
        inputs=("hot_water",),
        region="HH",
        node_type="demand",
        component="sink",
        sector="heat",
        carrier="hot_water",  # ('hot_water', 'steam'),
        flow_rates={"hot_water": nts.MinMax(min=0, max=max_th)},
        timeseries={"hot_water": nts.MinMax(min=th_HH, max=th_HH)},
    )

    excess_el = components.Sink(
        name="excess el",
        inputs=("electricity",),
        region="HH",
        node_type="excess",
        component="sink",
        sector="power",
        carrier="electricity",
    )

    excess_th = components.Sink(
        name="excess th",
        inputs=("hot_water",),
        region="HH",
        node_type="excess",
        component="sink",
        sector="heat",
        carrier="hot_water",  # ('hot_water', 'steam'),
    )

    # Busses:

    bm_logistics = components.Bus(
        name="biomass logistics",
        region="HH",
        node_type="logistics",
        component="bus",
        sector="coupled",
        carrier="biomass",
        inputs=("biomass supply.biomass",),
        outputs=("biomass chp.biomass",),
    )

    gas_pipeline = components.Bus(
        name="gas pipeline",
        region="HH",
        node_type="gas_pipeline",
        component="bus",
        sector="coupled",
        carrier="gas",
        inputs=("gas supply.gas",),
        outputs=("chp1.gas", "chp2.gas", "hp1.gas"),
    )

    coal_supply_line = components.Bus(
        name="coal supply line",
        region="HH",
        node_type="gas_pipeline",
        component="bus",
        sector="coupled",
        carrier="coal",
        inputs=("coal supply.coal",),
        outputs=(
            "pp1.coal",
            "pp2.coal",
            "chp3.coal",
            "chp4.coal",
            "chp5.coal",
        ),
    )

    oil_supply_line = components.Bus(
        name="oil supply line",
        region="HH",
        node_type="oil_delivery",
        component="bus",
        sector="power",
        carrier="oil",
        inputs=("oil supply.oil",),
        outputs=(
            "pp3.oil",
            "pp4.oil",
        ),
    )

    waste_supply = components.Bus(
        name="waste supply",
        region="HH",
        node_type="waste_supply",
        component="bus",
        sector="coupled",
        carrier="waste",
        inputs=("waste.waste",),
        outputs=("chp6.waste",),
    )

    powerline = components.Bus(
        name="powerline",
        region="HH",
        node_type="powerline",
        component="bus",
        sector="power",
        carrier="electricity",
        inputs=(
            "chp1.electricity",
            "chp2.electricity",
            "chp3.electricity",
            "chp4.electricity",
            "chp5.electricity",
            "chp6.electricity",
            "pp1.electricity",
            "pp2.electricity",
            "pp3.electricity",
            "pp4.electricity",
            "pv1.electricity",
            "won1.electricity",
            "biomass chp.electricity",
            # 'bm1.electricity',
            "imported el.electricity",
            "est.electricity",
        ),
        outputs=(
            "demand el.electricity",
            "excess el.electricity",
            "est.electricity",
            "p2h.electricity",
        ),
    )

    district_heating = components.Bus(
        name="district heating pipeline",
        region="HH",
        node_type="district_heating_pipeline",
        component="bus",
        sector="heat",
        carrier="hot_water",
        inputs=(
            "chp1.hot_water",
            "chp2.hot_water",
            "chp3.hot_water",
            "chp4.hot_water",
            "chp6.hot_water",
            "chp5.hot_water",
            # 'bm1.hot_water',
            "biomass chp.hot_water",
            "imported heat.hot_water",
            "p2h.hot_water",
            "hp1.hot_water",
        ),
        outputs=(
            "demand th.hot_water",
            "excess th.hot_water",
        ),
    )

    # 4. Create the actual energy system:
    explicit_es = energy_system.AbstractEnergySystem(
        uid="Energy System Hamburg",
        busses=(
            coal_supply_line,
            gas_pipeline,
            oil_supply_line,
            waste_supply,
            powerline,
            district_heating,
            bm_logistics,
        ),
        sinks=(
            demand_el,
            demand_th,
            excess_el,
            excess_th,
        ),
        sources=(
            gass,
            coals,
            oils,
            waste,
            pv1,
            won1,
            bm_supply,
            imel,
            imth,
        ),
        transformers=(
            chp1,
            chp2,
            chp3,
            chp4,
            chp5,
            chp6,
            pp1,
            pp2,
            pp3,
            pp4,
            hp1,
            p2h,
            bm_chp,
        ),
        storages=(est,),
        timeframe=timeframe,
        global_constraints=global_constraints,
        # milp=True,
    )

    return explicit_es


# pylint: enable=too-many-locals
# pylint: enable=duplicate-code
