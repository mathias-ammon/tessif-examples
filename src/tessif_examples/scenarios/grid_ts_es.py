# src/tessif_examples/scenarios/grid_ts_es.py
# pylint: disable=too-many-locals
# pylint: disable=duplicate-code
# pylint: disable=too-many-lines
"""Generic grid tessif energy system model example."""
import os

import numpy as np
import pandas as pd
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system

from tessif_examples.data.frused.paths import example_dir


def create_grid_ts_es(
    periods=24,
    transformer_efficiency=0.99,
    gridcapacity=60000,
    directory=None,
    filename=None,
):
    """
    Create a model of a generic grid style energy system using
    :mod:`tessif's model <tessif.model>`.

    Parameters
    ----------
    periods : int, default=24
        Number of time steps of the evaluated timeframe (one time step is one
        hour)

    transformer_efficiency : int, default=0.99
        Efficiency of the grid transformers (must be a value between 0 and 1)

    gridcapacity : int, default=60000
        Transmission capacity of the transformers of the gridstructure
        (at 0 the parts of the grid are not connected)

    Return
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`AutoCompare_Grid` - For simulating and
    comparing this energy system using different supported models.

    :ref:`Examples_Application_Grid`,  - For a comprehensive example
    on a reference energy system to analyze and compare commitment
    optimization respecting among models.

    Examples
    --------
    Use :func:`create_grid_ts_es` to quickly access a tessif energy system
    to use for doctesting, or trying out this framework's utilities.

        import tessif.examples.data.tsf.py_hard as tsf_py
        es = tsf_py.create_grid_ts_es()

        for node in es.nodes:
            print(node.uid)
        Gaspipeline
        Low Voltage Powerline
        District Heating
        Medium Voltage Powerline
        High Voltage Powerline
        Coal Supply Line
        Biogas
        Solar Panel
        Gas Station
        Onshore Wind Power
        Offshore Wind Power
        Coal Supply
        Solar Thermal
        Biogas plant
        Household Demand
        Commercial Demand
        District Heating Demand
        Industrial Demand
        Car charging Station
        BHKW
        Power to Heat
        GuD
        HKW
        High Medium Transformator
        Low Medium Transformator
        Medium Low Transformator
        Medium High Transformator
        HKW2
        Pumped Storage LV
        Pumped Storage MV
        Pumped Storage HV

    Visualize the energy system for better understanding what the output means:

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_generic_grid(),
            color_group={
                'Coal Supply': '#666666',
                'Coal Supply Line': '#666666',
                'HKW': '#666666',
                'HKW2': '#666666',
                'Solar Thermal': '#b30000',
                'Heat Storage': '#cc0033',
                'District Heating': 'Red',
                'District Heating Demand': 'Red',
                'Power to Heat': '#b30000',
                'Biogas plant': '#006600',
                'Biogas': '#006600',
                'BHKW': '#006600',
                'Onshore Wind Power': '#99ccff',
                'Offshore Wind Power': '#00ccff',
                'Gas Station': '#336666',
                'Gaspipeline': '#336666',
                'GuD': '#336666',
                'Solar Panel': '#ffe34d',
                'Commercial Demand': '#ffe34d',
                'Household Demand': '#ffe34d',
                'Industrial Demand': '#ffe34d',
                'Car charging Station': '#669999',
                'Low Voltage Powerline': '#ffcc00',
                'Medium Voltage Powerline': '#ffcc00',
                'High Voltage Powerline': '#ffcc00',
                'High Voltage Transformator': 'yellow',
                'Low Voltage Transformator': 'yellow',
                'Pumped Storage LV': '#0000cc',
                'Pumped Storage MV': '#0000cc',
                'Pumped Storage HV': '#0000cc',
           },
           title='Energy System Grid Transformer and Storages Graph',
        )
        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/grid_es_TS_example.png
        :align: center
        :alt: Image showing the create_grid_TS_es energy system graph.
    """
    # 2. Create a simulation time frame as a :class:`pandas.DatetimeIndex`:
    timeframe = pd.date_range("10/13/2030", periods=periods, freq="H")

    # 3. Parse csv files with the demand and renewables load data:
    d = os.path.join(example_dir, "data", "tsf", "load_profiles")

    # solar:
    pv = pd.read_csv(os.path.join(d, "Renewable_Energy.csv"), index_col=0, sep=";")
    pv = pv["pv_load"].values.flatten()[0:periods]
    max_pv = np.max(pv)

    # wind onshore:
    w_on = pd.read_csv(os.path.join(d, "Renewable_Energy.csv"), index_col=0, sep=";")
    w_on = w_on["won_load"].values.flatten()[0:periods]
    max_w_on = np.max(w_on)

    # wind offshore:
    w_off = pd.read_csv(os.path.join(d, "Renewable_Energy.csv"), index_col=0, sep=";")
    w_off = w_off["woff_load"].values.flatten()[0:periods]
    max_w_off = np.max(w_off)

    # solar thermal:
    s_t = pd.read_csv(os.path.join(d, "Renewable_Energy.csv"), index_col=0, sep=";")
    s_t = s_t["st_load"].values.flatten()[0:periods]
    max_s_t = np.max(s_t)

    # household demand
    h_d = pd.read_csv(os.path.join(d, "Loads.csv"), index_col=0, sep=";")
    h_d = h_d["household_demand"].values.flatten()[0:periods]
    max_h_d = np.max(h_d)

    # industrial demand
    i_d = pd.read_csv(os.path.join(d, "Loads.csv"), index_col=0, sep=";")
    i_d = i_d["industrial_demand"].values.flatten()[0:periods]
    max_i_d = np.max(i_d)

    # commercial demand
    c_d = pd.read_csv(os.path.join(d, "Loads.csv"), index_col=0, sep=";")
    c_d = c_d["commercial_demand"].values.flatten()[0:periods]
    max_c_d = np.max(c_d)

    # district heating demand
    dh_d = pd.read_csv(os.path.join(d, "Loads.csv"), index_col=0, sep=";")
    dh_d = dh_d["heat_demand"].values.flatten()[0:periods]
    max_dh_d = np.max(dh_d)

    # car charging demand
    cc_d = pd.read_csv(os.path.join(d, "Car_Charging.csv"), index_col=0, sep=";")
    cc_d = cc_d["cc_demand"].values.flatten()[0:periods]
    max_cc_d = np.max(cc_d)

    # 4. Create the individual energy system components:
    global_constraints = {
        "name": "default",
        "emissions": float("+inf"),
        "resources": float("+inf"),
    }

    # Low Voltage and heat

    solar_panel = components.Source(
        name="Solar Panel",
        outputs=("low-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="Renewable",
        flow_rates={"low-voltage-electricity": nts.MinMax(min=0, max=max_pv)},
        flow_costs={"low-voltage-electricity": 60.85},
        flow_emissions={"low-voltage-electricity": 0},
        timeseries={"low-voltage-electricity": nts.MinMax(min=pv, max=pv)},
    )

    gas_supply = components.Source(
        name="Gas Station",
        outputs=("fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="Gas",
        node_type="source",
        flow_rates={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={"fuel": 0},
        flow_emissions={"fuel": 0},
        timeseries=None,
    )

    biogas_supply = components.Source(
        name="Biogas plant",
        outputs=("fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="Gas",
        node_type="source",
        flow_rates={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        flow_costs={"fuel": 0},
        flow_emissions={"fuel": 0},
        timeseries=None,
    )

    bhkw_generator = components.Transformer(
        name="BHKW",
        inputs=("fuel",),
        outputs=("low-voltage-electricity", "heat"),
        conversions={("fuel", "low-voltage-electricity"): 0.33, ("fuel", "heat"): 0.52},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=25987.87879),
            "low-voltage-electricity": nts.MinMax(min=0, max=8576),
            "heat": nts.MinMax(min=0, max=13513.69697),
        },
        flow_costs={"fuel": 0, "low-voltage-electricity": 124.4, "heat": 31.1},
        flow_emissions={"fuel": 0, "low-voltage-electricity": 0.1573, "heat": 0.0732},
        timeseries=None,
    )

    household_demand = components.Sink(
        name="Household Demand",
        inputs=("low-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        flow_rates={"low-voltage-electricity": nts.MinMax(min=0, max=max_h_d)},
        flow_costs={"low-voltage-electricity": 0},
        flow_emissions={"low-voltage-electricity": 0},
        timeseries={"low-voltage-electricity": nts.MinMax(min=h_d, max=h_d)},
    )

    commercial_demand = components.Sink(
        name="Commercial Demand",
        inputs=("low-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        flow_rates={"low-voltage-electricity": nts.MinMax(min=0, max=max_c_d)},
        flow_costs={"low-voltage-electricity": 0},
        flow_emissions={"low-voltage-electricity": 0},
        timeseries={"low-voltage-electricity": nts.MinMax(min=c_d, max=c_d)},
    )

    heat_demand = components.Sink(
        name="District Heating Demand",
        inputs=("heat",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Heat",
        carrier="hot Water",
        node_type="demand",
        flow_rates={"heat": nts.MinMax(min=0, max=max_dh_d)},
        flow_costs={"heat": 0},
        flow_emissions={"heat": 0},
        timeseries={"heat": nts.MinMax(min=dh_d, max=dh_d)},
    )

    gas_supply_line = components.Bus(
        name="Gaspipeline",
        inputs=("Gas Station.fuel",),
        outputs=("GuD.fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="gas",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    biogas_supply_line = components.Bus(
        name="Biogas",
        inputs=("Biogas plant.fuel",),
        outputs=("BHKW.fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="gas",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    low_electricity_line = components.Bus(
        name="Low Voltage Powerline",
        inputs=(
            "BHKW.low-voltage-electricity",
            "Solar Panel.low-voltage-electricity",
            "Medium Low Transformator.low-voltage-electricity",
            "Pumped Storage LV.low-voltage-electricity",
        ),
        outputs=(
            "Household Demand.low-voltage-electricity",
            "Commercial Demand.low-voltage-electricity",
            "Low Medium Transformator.low-voltage-electricity",
            "Pumped Storage LV.low-voltage-electricity",
        ),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    heat_line = components.Bus(
        name="District Heating",
        inputs=("BHKW.heat", "Solar Thermal.heat", "Power to Heat.heat", "HKW.heat"),
        outputs=("District Heating Demand.heat",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Heat",
        carrier="hot Water",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    # Medium Voltage and heat

    onshore_wind_power = components.Source(
        name="Onshore Wind Power",
        outputs=("medium-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="power",
        carrier="electricity",
        node_type="Renewable",
        flow_rates={"medium-voltage-electricity": nts.MinMax(min=0, max=max_w_on)},
        flow_costs={"medium-voltage-electricity": 61.1},
        flow_emissions={"medium-voltage-electricity": 0},
        timeseries={"medium-voltage-electricity": nts.MinMax(min=w_on, max=w_on)},
    )

    solar_thermal = components.Source(
        name="Solar Thermal",
        outputs=("heat",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Heat",
        carrier="Hot Water",
        node_type="Renewable",
        flow_rates={"heat": nts.MinMax(min=0, max=max_s_t)},
        flow_costs={"heat": 73},
        flow_emissions={"heat": 0},
        timeseries={"heat": nts.MinMax(min=s_t, max=s_t)},
    )

    industrial_demand = components.Sink(
        name="Industrial Demand",
        inputs=("medium-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        flow_rates={"medium-voltage-electricity": nts.MinMax(min=0, max=max_i_d)},
        flow_costs={"medium-voltage-electricity": 0},
        flow_emissions={"medium-voltage-electricity": 0},
        timeseries={"medium-voltage-electricity": nts.MinMax(min=i_d, max=i_d)},
    )

    car_charging_station_demand = components.Sink(
        name="Car charging Station",
        inputs=("medium-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        flow_rates={"medium-voltage-electricity": nts.MinMax(min=0, max=max_cc_d)},
        flow_costs={"medium-voltage-electricity": 0},
        flow_emissions={"medium-voltage-electricity": 0},
        timeseries={"medium-voltage-electricity": nts.MinMax(min=cc_d, max=cc_d)},
    )

    power_to_heat = components.Transformer(
        name="Power to Heat",
        inputs=("medium-voltage-electricity",),
        outputs=("heat",),
        conversions={("medium-voltage-electricity", "heat"): 1.00},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        carrier="Hot Water",
        node_type="transformer",
        flow_rates={
            "medium-voltage-electricity": nts.MinMax(min=0, max=float("+inf")),
            "heat": nts.MinMax(min=0, max=float("+inf")),
        },
        flow_costs={"medium-voltage-electricity": 0, "heat": 0},
        flow_emissions={"medium-voltage-electricity": 0, "heat": 0},
        timeseries=None,
    )

    medium_electricity_line = components.Bus(
        name="Medium Voltage Powerline",
        inputs=(
            "Onshore Wind Power.medium-voltage-electricity",
            "High Medium Transformator.medium-voltage-electricity",
            "Low Medium Transformator.medium-voltage-electricity",
            "Pumped Storage MV.medium-voltage-electricity",
        ),
        outputs=(
            "Car charging Station.medium-voltage-electricity",
            "Industrial Demand.medium-voltage-electricity",
            "Power to Heat.medium-voltage-electricity",
            "Medium High Transformator.medium-voltage-electricity",
            "Medium Low Transformator.medium-voltage-electricity",
            "Pumped Storage MV.medium-voltage-electricity",
        ),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    # High Voltage

    offshore_wind_power = components.Source(
        name="Offshore Wind Power",
        outputs=("high-voltage-electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="Renewable",
        flow_rates={"high-voltage-electricity": nts.MinMax(min=0, max=max_w_off)},
        flow_costs={"high-voltage-electricity": 106.4},
        flow_emissions={"high-voltage-electricity": 0},
        timeseries={"high-voltage-electricity": nts.MinMax(min=w_off, max=w_off)},
    )

    coal_supply = components.Source(
        name="Coal Supply",
        outputs=("fuel",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="Coal",
        node_type="source",
        flow_rates={"fuel": nts.MinMax(min=0, max=102123.3)},
        flow_costs={"fuel": 0},
        flow_emissions={"fuel": 0},
        timeseries=None,
    )

    hkw_generator = components.Transformer(
        name="HKW",
        inputs=("fuel",),
        outputs=("high-voltage-electricity", "heat"),
        conversions={("fuel", "high-voltage-electricity"): 0.24, ("fuel", "heat"): 0.6},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=102123.3),
            "high-voltage-electricity": nts.MinMax(min=0, max=24509.6),
            "heat": nts.MinMax(min=0, max=61273.96),
        },
        flow_costs={"fuel": 0, "high-voltage-electricity": 80.65, "heat": 20.1625},
        flow_emissions={"fuel": 0, "high-voltage-electricity": 0.5136, "heat": 0.293},
        timeseries=None,
    )

    hkw_generator_2 = components.Transformer(
        name="HKW2",
        inputs=("fuel",),
        outputs=("high-voltage-electricity",),
        conversions={("fuel", "high-voltage-electricity"): 0.43},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="electricity",
        node_type="connector",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=102123.3),
            "high-voltage-electricity": nts.MinMax(min=0, max=43913),
        },
        flow_costs={"fuel": 0, "high-voltage-electricity": 80.65},
        flow_emissions={"fuel": 0, "high-voltage-electricity": 0.5136},
        timeseries=None,
    )

    gud_generator = components.Transformer(
        name="GuD",
        inputs=("fuel",),
        outputs=("high-voltage-electricity",),
        conversions={("fuel", "high-voltage-electricity"): 0.59},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=45325.42373),
            "high-voltage-electricity": nts.MinMax(min=0, max=26742),
        },
        flow_costs={"fuel": 0, "high-voltage-electricity": 88.7},
        flow_emissions={"fuel": 0, "high-voltage-electricity": 0.3366},
        timeseries=None,
    )

    coal_supply_line = components.Bus(
        name="Coal Supply Line",
        inputs=("Coal Supply.fuel",),
        outputs=("HKW.fuel", "HKW2.fuel"),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="Coal",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    high_electricity_line = components.Bus(
        name="High Voltage Powerline",
        inputs=(
            "Offshore Wind Power.high-voltage-electricity",
            "HKW2.high-voltage-electricity",
            "GuD.high-voltage-electricity",
            "HKW.high-voltage-electricity",
            "Medium High Transformator.high-voltage-electricity",
            "Pumped Storage HV.high-voltage-electricity",
        ),
        outputs=(
            "High Medium Transformator.high-voltage-electricity",
            "Pumped Storage HV.high-voltage-electricity",
        ),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    # Gridstructure and Transformer

    low_medium_transformator = components.Transformer(
        name="Low Medium Transformator",
        inputs=("low-voltage-electricity",),
        outputs=("medium-voltage-electricity",),
        conversions={
            (
                "low-voltage-electricity",
                "medium-voltage-electricity",
            ): transformer_efficiency
        },
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="connector",
        flow_rates={
            "low-voltage-electricity": nts.MinMax(min=0, max=gridcapacity),
            "medium-voltage-electricity": nts.MinMax(
                min=0, max=transformer_efficiency * gridcapacity
            ),
        },
        flow_costs={"low-voltage-electricity": 0, "medium-voltage-electricity": 0},
        flow_emissions={"low-voltage-electricity": 0, "medium-voltage-electricity": 0},
        timeseries=None,
    )

    medium_low_transformator = components.Transformer(
        name="Medium Low Transformator",
        inputs=("medium-voltage-electricity",),
        outputs=("low-voltage-electricity",),
        conversions={
            (
                "medium-voltage-electricity",
                "low-voltage-electricity",
            ): transformer_efficiency
        },
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="connector",
        flow_rates={
            "low-voltage-electricity": nts.MinMax(
                min=0, max=transformer_efficiency * gridcapacity
            ),
            "medium-voltage-electricity": nts.MinMax(min=0, max=gridcapacity),
        },
        flow_costs={"low-voltage-electricity": 0, "medium-voltage-electricity": 0},
        flow_emissions={"low-voltage-electricity": 0, "medium-voltage-electricity": 0},
        timeseries=None,
    )

    medium_high_transformator = components.Transformer(
        name="Medium High Transformator",
        inputs=("medium-voltage-electricity",),
        outputs=("high-voltage-electricity",),
        conversions={
            (
                "medium-voltage-electricity",
                "high-voltage-electricity",
            ): transformer_efficiency
        },
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="connector",
        flow_rates={
            "high-voltage-electricity": nts.MinMax(
                min=0, max=transformer_efficiency * gridcapacity
            ),
            "medium-voltage-electricity": nts.MinMax(min=0, max=gridcapacity),
        },
        flow_costs={"high-voltage-electricity": 0, "medium-voltage-electricity": 0},
        flow_emissions={"high-voltage-electricity": 0, "medium-voltage-electricity": 0},
        timeseries=None,
    )

    high_medium_transformator = components.Transformer(
        name="High Medium Transformator",
        inputs=("high-voltage-electricity",),
        outputs=("medium-voltage-electricity",),
        conversions={
            (
                "high-voltage-electricity",
                "medium-voltage-electricity",
            ): transformer_efficiency
        },
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="connector",
        flow_rates={
            "high-voltage-electricity": nts.MinMax(min=0, max=gridcapacity),
            "medium-voltage-electricity": nts.MinMax(
                min=0, max=transformer_efficiency * gridcapacity
            ),
        },
        flow_costs={"high-voltage-electricity": 0, "medium-voltage-electricity": 0},
        flow_emissions={"high-voltage-electricity": 0, "medium-voltage-electricity": 0},
        timeseries=None,
    )

    # Storages

    pumped_storage_lv = components.Storage(
        name="Pumped Storage LV",
        input="low-voltage-electricity",
        output="low-voltage-electricity",
        capacity=40000,
        initial_soc=50,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=0),
        flow_rates={"low-voltage-electricity": nts.MinMax(min=0, max=8600)},
        flow_efficiencies={
            "low-voltage-electricity": nts.InOut(inflow=0.86, outflow=0.86)
        },
        flow_costs={"low-voltage-electricity": 0},
        flow_emissions={"low-voltage-electricity": 0},
        timeseries=None,
    )

    pumped_storage_mv = components.Storage(
        name="Pumped Storage MV",
        input="medium-voltage-electricity",
        output="medium-voltage-electricity",
        capacity=40000,
        initial_soc=50,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=0),
        flow_rates={"medium-voltage-electricity": nts.MinMax(min=0, max=8600)},
        flow_efficiencies={
            "medium-voltage-electricity": nts.InOut(inflow=0.86, outflow=0.86)
        },
        flow_costs={"medium-voltage-electricity": 0},
        flow_emissions={"medium-voltage-electricity": 0},
        timeseries=None,
    )

    pumped_storage_hv = components.Storage(
        name="Pumped Storage HV",
        input="high-voltage-electricity",
        output="high-voltage-electricity",
        capacity=40000,
        initial_soc=50,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=0),
        flow_rates={"high-voltage-electricity": nts.MinMax(min=0, max=8600)},
        flow_efficiencies={
            "high-voltage-electricity": nts.InOut(inflow=0.86, outflow=0.86)
        },
        flow_costs={"high-voltage-electricity": 0},
        flow_emissions={"high-voltage-electricity": 0},
        timeseries=None,
    )

    # 4. Create the actual energy system:
    es = energy_system.AbstractEnergySystem(
        uid="Energy System Grid Transformers and Storages",
        busses=(
            gas_supply_line,
            low_electricity_line,
            heat_line,
            medium_electricity_line,
            high_electricity_line,
            coal_supply_line,
            biogas_supply_line,
        ),
        sinks=(
            household_demand,
            commercial_demand,
            heat_demand,
            industrial_demand,
            car_charging_station_demand,
        ),
        sources=(
            solar_panel,
            gas_supply,
            onshore_wind_power,
            offshore_wind_power,
            coal_supply,
            solar_thermal,
            biogas_supply,
        ),
        transformers=(
            bhkw_generator,
            power_to_heat,
            gud_generator,
            hkw_generator,
            high_medium_transformator,
            low_medium_transformator,
            medium_low_transformator,
            medium_high_transformator,
            hkw_generator_2,
        ),
        storages=(
            pumped_storage_lv,
            pumped_storage_mv,
            pumped_storage_hv,
        ),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return es


# pylint: enable=too-many-locals
# pylint: enable=duplicate-code
