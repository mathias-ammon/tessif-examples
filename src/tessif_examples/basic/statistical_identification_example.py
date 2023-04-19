# src/tessif_examples/basic/identification_example.py
"""tessif system model example for testing statistical identification."""
import os

import numpy as np
import pandas as pd
import tessif.frused.namedtuples as nts
from tessif import components, system_model

# from tessif_examples import utils
from tessif_examples.paths import data_dir


def create_statistical_identification_example(periods=24):
    """Create a generic system model for testing automated identification.

    Parameters
    ----------
    periods : int, default=24
        Number of time steps of the evaluated timeframe
        (one time step is one hour)

    Return
    ------
    :class:`tessif.system_model.AbstractEnergySystem`
        Tessif energy system model.

    Examples
    --------
    Generic System Visualization:

    .. image:: ../../_static/system_model_graphs/hh_es_example.png
        :align: center
        :alt: Image showing the create_hhes energy system graph.
    """
    # 2. Create a simulation time frame as a :class:`pandas.DatetimeIndex`:
    timeframe = pd.date_range("2019-01-01", periods=periods, freq="H")

    # 3. Parse csv files with the demand and renewables load data:
    data_directory = os.path.join(data_dir, "load_profiles")

    # solar:
    pv_hh = pd.read_csv(
        os.path.join(data_directory, "solar_HH_2019.csv"), index_col=0, sep=";"
    )
    pv_hh = pv_hh.values.flatten()[0:periods]
    max_pv = np.max(pv_hh)

    # # wind onshore:
    # wo_hh = pd.read_csv(
    #     os.path.join(data_directory, "wind_HH_2019.csv"), index_col=0, sep=";"
    # )
    # wo_hh = wo_hh.values.flatten()[0:periods]
    # max_wo = np.max(wo_hh)

    # electricity demand:
    de_hh = pd.read_csv(
        os.path.join(data_directory, "el_demand_HH_2019.csv"), index_col=0, sep=";"
    )
    de_hh = de_hh["Last (MW)"].values.flatten()[0:periods]
    de_hh = np.array(de_hh)
    max_de = np.max(de_hh)

    # heat demand:
    # th_hh = pd.read_csv(
    #     os.path.join(data_directory, "th_demand_HH_2019.csv"), index_col=0, sep=";"
    # )
    # th_hh = th_hh["actual_total_load"].values.flatten()[0:periods]
    # th_hh = np.array(th_hh)
    # max_th = np.max(th_hh)

    # 4. Create the individual energy system components:
    # in_stat = False
    # cfba = 0

    global_constraints = {
        "name": "2019",
        "emissions": float("+inf"),  # 800,
        "resources": float("+inf"),
    }

    powerline = components.Bus(
        name="Powerline",
        region="HH",
        sector="Power",
        node_type="AC-Bus",
        component="bus",
        carrier="electricity",
        inputs=(
            "Gas Powerplant.electricity",
            "Import.electricity",
            "Solar.electricity",
        ),
        outputs=(
            "Demand.electricity",
            "Excess.electricity",
        ),
    )

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        region="HH",
        node_type="demand",
        component="sink",
        sector="power",
        carrier="electricity",
        flow_rates={"electricity": nts.MinMax(min=0, max=max_de)},
        timeseries={"electricity": nts.MinMax(min=de_hh, max=de_hh)},
    )

    excess = components.Sink(
        name="Excess",
        region="HH",
        node_type="Demand",
        component="sink",
        carrier="electricity",
        inputs=("electricity",),
    )

    solar = components.Source(
        name="Solar",
        outputs=("electricity",),
        region="HH",
        sector="Power",
        carrier="electricity",
        component="source",
        node_type="renewable",
        flow_rates={"electricity": nts.MinMax(min=0, max=max_pv)},
        flow_costs={"electricity": 9},
        flow_emissions={"electricity": 0},
        timeseries={"electricity": nts.MinMax(min=pv_hh, max=pv_hh)},
        expandable={"electricity": True},
        expansion_costs={"electricity": 5},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
    )

    gas_pipeline = components.Bus(
        name="Gas Pipeline",
        region="HH",
        sector="Power",
        node_type="GAS",
        component="bus",
        carrier="gas",
        inputs=("Gas Supply.gas",),
        outputs=("Gas Powerplant.gas",),
    )

    gas_supply = components.Source(
        name="Gas Supply",
        region="HH",
        node_type="Gas Supply",
        component="source",
        carrier="GAS",
        # flow_costs=21,
        outputs=("gas",),
    )

    gas_powerplant = components.Transformer(
        name="Gas Powerplant",
        inputs=("gas",),
        outputs=("electricity",),
        conversions={
            ("gas", "electricity"): 0.4075,
        },
        region="HH",
        node_type="Gas Powerplant",
        component="transformer",
        sector="ELECTRICITY",
        carrier="GAS",
        flow_rates={
            "gas": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=400),
        },
        flow_costs={
            "gas": 10,
            "electricity": 82,
        },
        flow_emissions={
            "gas": 0.2,
            "electricity": 0,
        },
    )

    el_import = components.Source(
        name="Import",
        outputs=("electricity",),
        region="HH",
        node_type="Import",
        component="source",
        carrier="electricity",
        flow_rates={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={
            "electricity": 999,
        },
        flow_emissions={
            "electricity": 0.45,
        },
    )

    explicit_es = system_model.AbstractEnergySystem(
        uid="Statistical Identification Example",
        busses=(
            powerline,
            gas_pipeline,
        ),
        sinks=(demand, excess),
        sources=(
            el_import,
            solar,
            gas_supply,
        ),
        transformers=(gas_powerplant,),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return explicit_es
