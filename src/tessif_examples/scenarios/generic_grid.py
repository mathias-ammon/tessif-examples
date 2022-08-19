# src/tessif_examples/scenarios/generic_grid.py
# pylint: disable=too-many-locals
# pylint: disable=duplicate-code
# pylint: disable=too-many-lines
"""Generic grid tessif energy system model example."""
import numpy as np
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_generic_grid():
    """Create a generic grid tessif energy system model.

    Returns
    -------
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
    Use :func:`create_grid_es` to quickly access a tessif energy system
    to use for doctesting, or trying out this framework's utilities::

        es = create_generic_grid()

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
        Battery
        Heat Storage
        Pumped Storage
        Low Voltage Transformator
        High Voltage Transformator

    Visualize the energy system for better understanding what the output means::

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_generic_grid(),
            color_group={
                'Coal Supply': '#666666',
                'Coal Supply Line': '#666666',
                'HKW': '#b30000',
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
                'Battery': '#ffe34d',
                'Car charging Station': '#669999',
                'Low Voltage Powerline': '#ffcc00',
                'Medium Voltage Powerline': '#ffcc00',
                'High Voltage Powerline': '#ffcc00',
                'High Voltage Transformator': 'yellow',
                'Low Voltage Transformator': 'yellow',
                'Pumped Storage': '#0000cc',
            },
            title='Generic Grid Example Energy System Graph',
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/generic_grid.png
        :align: center
        :alt: Image showing the generic grid energy system graph.
    """
    timeframe = date_range("7/13/1990", periods=3, freq="H")

    global_constraints = {
        "name": "default",
        "emissions": float("+inf"),
        "resources": float("+inf"),
    }

    solar_panel = components.Source(
        name="Solar Panel",
        outputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="Electricity",
        node_type="Renewable",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=1000)},
        flow_rates={"electricity": nts.MinMax(min=0, max=25)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={"electricity": nts.PositiveNegative(positive=42, negative=42)},
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([12, 22, 7]), max=np.array([12, 22, 7])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 5},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
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
        accumulated_amounts={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        # max=100)},   float('+inf'))},
        flow_rates={"fuel": nts.MinMax(min=0, max=1000)},
        flow_costs={"fuel": 10},
        flow_emissions={"fuel": 3},
        flow_gradients={"fuel": nts.PositiveNegative(positive=1000, negative=1000)},
        gradient_costs={"fuel": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"fuel": False},
        expansion_costs={"fuel": 5},
        expansion_limits={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        milp={"fuel": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
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
        accumulated_amounts={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        # max=100)},   float('+inf'))},
        flow_rates={"fuel": nts.MinMax(min=0, max=1000)},
        flow_costs={"fuel": 0},  # flow_costs={'fuel': 8},
        flow_emissions={"fuel": 0},  # flow_emissions={'fuel': 3},
        flow_gradients={"fuel": nts.PositiveNegative(positive=1000, negative=1000)},
        gradient_costs={"fuel": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"fuel": False},
        expansion_costs={"fuel": 5},
        expansion_limits={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        milp={"fuel": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    bhkw_generator = components.Transformer(
        name="BHKW",
        inputs=("fuel",),
        outputs=("electricity", "heat"),
        conversions={("fuel", "electricity"): 0.35, ("fuel", "heat"): 0.55},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=100),
            "electricity": nts.MinMax(min=0, max=30),
            "heat": nts.MinMax(min=0, max=100),
        },
        flow_costs={"fuel": 0, "electricity": 10, "heat": 5},
        flow_emissions={"fuel": 0, "electricity": 10, "heat": 5},
        flow_gradients={
            "fuel": nts.PositiveNegative(positive=100, negative=100),
            "electricity": nts.PositiveNegative(positive=30, negative=30),
            "heat": nts.PositiveNegative(positive=100, negative=100),
        },
        gradient_costs={
            "fuel": nts.PositiveNegative(positive=0, negative=0),
            "electricity": nts.PositiveNegative(positive=0, negative=0),
            "heat": nts.PositiveNegative(positive=0, negative=0),
        },
        timeseries=None,
        expandable={"fuel": False, "electricity": False, "heat": False},
        expansion_costs={"fuel": 0, "electricity": 0, "heat": 0},
        expansion_limits={
            "fuel": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
            "heat": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False, "fuel": False, "heat": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=9),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    household_demand = components.Sink(
        name="Household Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"electricity": nts.MinMax(min=190, max=190)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=200, negative=200)
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"electricity": False},
        expansion_costs={"electricity": 0},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=2, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=8),
        costs_for_being_active=0
        # Total number of arguments to specify sink object
    )

    commercial_demand = components.Sink(
        name="Commercial Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"electricity": nts.MinMax(min=0, max=200)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=200, negative=200)
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([80, 20, 130]), max=np.array([80, 20, 130])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 0},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=2, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=8),
        costs_for_being_active=0
        # Total number of arguments to specify sink object
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
        accumulated_amounts={"heat": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"heat": nts.MinMax(min=300, max=500)},
        flow_costs={"heat": 0},
        flow_emissions={"heat": 0},
        flow_gradients={"heat": nts.PositiveNegative(positive=500, negative=500)},
        gradient_costs={"heat": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "heat": nts.MinMax(
                min=np.array([340, 300, 380]), max=np.array([340, 300, 380])
            )
        },
        expandable={"heat": False},
        expansion_costs={"heat": 0},
        expansion_limits={"heat": nts.MinMax(min=0, max=float("+inf"))},
        milp={"heat": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=2, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=8),
        costs_for_being_active=0
        # Total number of arguments to specify sink object
    )

    battery_storage = components.Storage(
        name="Battery",
        input="electricity",
        output="electricity",
        capacity=20,
        initial_soc=10,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=1),
        flow_rates={"electricity": nts.MinMax(min=0, max=30)},
        flow_efficiencies={"electricity": nts.InOut(inflow=1, outflow=1)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(
                positive=float("+inf"), negative=float("+inf")
            )
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"capacity": False, "electricity": False},
        expansion_costs={"capacity": 2, "electricity": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=2),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=42),
        costs_for_being_active=0
        # Total number of arguments to specify source object
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
            "BHKW.electricity",
            "Battery.electricity",
            "Solar Panel.electricity",
        ),
        outputs=(
            "Household Demand.electricity",
            "Commercial Demand.electricity",
            "Battery.electricity",
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
        inputs=(
            "BHKW.heat",
            "Solar Thermal.heat",
            "Heat Storage.heat",
            "Power to Heat.heat",
            "HKW.heat",
        ),
        outputs=("District Heating Demand.heat", "Heat Storage.heat"),
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
        outputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="Electricity",
        node_type="Renewable",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=2000)},
        flow_rates={"electricity": nts.MinMax(min=0, max=100)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=100, negative=100)
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([60, 80, 34]), max=np.array([60, 80, 34])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 8},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
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
        accumulated_amounts={"heat": nts.MinMax(min=0, max=1000)},
        flow_rates={"heat": nts.MinMax(min=0, max=50)},
        flow_costs={"heat": 0},
        flow_emissions={"heat": 0},
        flow_gradients={"heat": nts.PositiveNegative(positive=42, negative=42)},
        gradient_costs={"heat": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "heat": nts.MinMax(min=np.array([24, 44, 14]), max=np.array([24, 44, 14]))
        },
        expandable={"heat": False},
        expansion_costs={"heat": 4},
        expansion_limits={"heat": nts.MinMax(min=0, max=float("+inf"))},
        milp={"heat": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    industrial_demand = components.Sink(
        name="Industrial Demand",
        inputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"electricity": nts.MinMax(min=0, max=400)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=400, negative=400)
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([160, 160, 120]), max=np.array([160, 160, 120])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 0},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=2, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=8),
        costs_for_being_active=0
        # Total number of arguments to specify sink object
    )

    car_charging_station_demand = components.Sink(
        name="Car charging Station",
        inputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="demand",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        flow_rates={"electricity": nts.MinMax(min=0, max=1000)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=1000, negative=1000)
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([0, 0, 100]), max=np.array([0, 0, 100])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 0},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=2, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=8),
        costs_for_being_active=0
        # Total number of arguments to specify sink object
    )

    power_to_heat = components.Transformer(
        name="Power to Heat",
        inputs=("electricity",),
        outputs=("heat",),
        conversions={("electricity", "heat"): 1.00},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="coupled",
        carrier="Hot Water",
        node_type="transformer",
        flow_rates={
            "electricity": nts.MinMax(min=0, max=100),
            "heat": nts.MinMax(min=0, max=100),
        },
        flow_costs={"electricity": 0, "heat": 1},
        flow_emissions={"electricity": 0, "heat": 1},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=100, negative=100),
            "heat": nts.PositiveNegative(positive=100, negative=100),
        },
        gradient_costs={
            "electricity": nts.PositiveNegative(positive=0, negative=0),
            "heat": nts.PositiveNegative(positive=0, negative=0),
        },
        timeseries=None,
        expandable={"electricity": False, "heat": False},
        expansion_costs={"electricity": 0, "heat": 0},
        expansion_limits={
            "electricity": nts.MinMax(min=0, max=float("+inf")),
            "heat": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False, "fuel": False, "heat": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=0),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=9),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    heat_storage = components.Storage(
        name="Heat Storage",
        input="heat",
        output="heat",
        capacity=50,
        initial_soc=10,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Heat",
        carrier="Hot Water",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=0.15),
        flow_rates={"heat": nts.MinMax(min=0, max=50)},
        flow_efficiencies={"heat": nts.InOut(inflow=0.95, outflow=0.95)},
        flow_costs={"heat": 0},
        flow_emissions={"heat": 0},
        flow_gradients={
            "heat": nts.PositiveNegative(positive=float("+inf"), negative=float("+inf"))
        },
        gradient_costs={"heat": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"capacity": False, "heat": False},
        expansion_costs={"capacity": 2, "heat": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=0, max=float("+inf")),
            "heat": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"heat": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=2),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=42),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    medium_electricity_line = components.Bus(
        name="Medium Voltage Powerline",
        inputs=("Onshore Wind Power.electricity",),
        outputs=(
            "Car charging Station.electricity",
            "Industrial Demand.electricity",
            "Power to Heat.electricity",
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

    low_medium_transformator = components.Connector(
        name="Low Voltage Transformator",
        interfaces=(str(medium_electricity_line.uid), str(low_electricity_line.uid)),
        conversions={
            (str(medium_electricity_line.uid), str(low_electricity_line.uid)): 1,
            (
                str(low_electricity_line.uid),
                str(medium_electricity_line.uid),
            ): 1,
        },
        timeseries=None,
        node_type="connector",
        sector="power",
    )

    # High Voltage

    offshore_wind_power = components.Source(
        name="Offshore Wind Power",
        outputs=("electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="Electricity",
        node_type="Renewable",
        accumulated_amounts={"electricity": nts.MinMax(min=0, max=4000)},
        flow_rates={"electricity": nts.MinMax(min=0, max=200)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(positive=200, negative=200)
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([120, 140, 70]), max=np.array([120, 140, 70])
            )
        },
        expandable={"electricity": False},
        expansion_costs={"electricity": 9},
        expansion_limits={"electricity": nts.MinMax(min=0, max=float("+inf"))},
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
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
        accumulated_amounts={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        # max=100)},   float('+inf'))},
        flow_rates={"fuel": nts.MinMax(min=0, max=500)},
        flow_costs={"fuel": 8},
        flow_emissions={"fuel": 5},
        flow_gradients={"fuel": nts.PositiveNegative(positive=500, negative=500)},
        gradient_costs={"fuel": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"fuel": False},
        expansion_costs={"fuel": 5},
        expansion_limits={"fuel": nts.MinMax(min=0, max=float("+inf"))},
        milp={"fuel": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=1, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=10),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    hkw_generator = components.Transformer(
        name="HKW",
        inputs=("fuel",),
        outputs=("electricity", "heat"),
        conversions={("fuel", "electricity"): 0.35, ("fuel", "heat"): 0.53},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Coupled",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=500),
            "electricity": nts.MinMax(min=0, max=500),
            "heat": nts.MinMax(min=0, max=500),
        },
        flow_costs={"fuel": 0, "electricity": 5, "heat": 5},
        flow_emissions={"fuel": 0, "electricity": 5, "heat": 5},
        flow_gradients={
            "fuel": nts.PositiveNegative(positive=500, negative=500),
            "electricity": nts.PositiveNegative(positive=500, negative=500),
            "heat": nts.PositiveNegative(positive=500, negative=500),
        },
        gradient_costs={
            "fuel": nts.PositiveNegative(positive=0, negative=0),
            "electricity": nts.PositiveNegative(positive=0, negative=0),
            "heat": nts.PositiveNegative(positive=0, negative=0),
        },
        timeseries=None,
        expandable={"fuel": False, "electricity": False, "heat": False},
        expansion_costs={"fuel": 0, "electricity": 0, "heat": 0},
        expansion_limits={
            "fuel": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
            "heat": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False, "fuel": False, "heat": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=1),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=9),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    gud_generator = components.Transformer(
        name="GuD",
        inputs=("fuel",),
        outputs=("electricity",),
        conversions={("fuel", "electricity"): 0.6},
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="transformer",
        flow_rates={
            "fuel": nts.MinMax(min=0, max=500),
            "electricity": nts.MinMax(min=0, max=500),
        },
        flow_costs={"fuel": 0, "electricity": 5},
        flow_emissions={"fuel": 0, "electricity": 5},
        flow_gradients={
            "fuel": nts.PositiveNegative(positive=500, negative=500),
            "electricity": nts.PositiveNegative(positive=500, negative=500),
        },
        gradient_costs={
            "fuel": nts.PositiveNegative(positive=0, negative=0),
            "electricity": nts.PositiveNegative(positive=0, negative=0),
        },
        timeseries=None,
        expandable={"fuel": False, "electricity": False},
        expansion_costs={"fuel": 0, "electricity": 0},
        expansion_limits={
            "fuel": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False, "fuel": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=2),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=9),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    pumped_storage = components.Storage(
        name="Pumped Storage",
        input="electricity",
        output="electricity",
        capacity=400,
        initial_soc=50,
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="storage",
        idle_changes=nts.PositiveNegative(positive=0, negative=0),
        flow_rates={"electricity": nts.MinMax(min=0, max=100)},
        flow_efficiencies={"electricity": nts.InOut(inflow=0.9, outflow=0.9)},
        flow_costs={"electricity": 0},
        flow_emissions={"electricity": 0},
        flow_gradients={
            "electricity": nts.PositiveNegative(
                positive=float("+inf"), negative=float("+inf")
            )
        },
        gradient_costs={"electricity": nts.PositiveNegative(positive=0, negative=0)},
        timeseries=None,
        expandable={"capacity": False, "electricity": False},
        expansion_costs={"capacity": 2, "electricity": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=0, max=float("+inf")),
            "electricity": nts.MinMax(min=0, max=float("+inf")),
        },
        milp={"electricity": False},
        initial_status=True,
        status_inertia=nts.OnOff(on=0, off=2),
        status_changing_costs=nts.OnOff(on=0, off=0),
        number_of_status_changes=nts.OnOff(on=float("+inf"), off=42),
        costs_for_being_active=0
        # Total number of arguments to specify source object
    )

    coal_supply_line = components.Bus(
        name="Coal Supply Line",
        inputs=("Coal Supply.fuel",),
        outputs=("HKW.fuel",),
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
            "Offshore Wind Power.electricity",
            "Pumped Storage.electricity",
            "GuD.electricity",
            "HKW.electricity",
        ),
        outputs=("Pumped Storage.electricity",),
        # Minimum number of arguments required
        latitude=42,
        longitude=42,
        region="Here",
        sector="Power",
        carrier="electricity",
        node_type="bus",
        # Total number of arguments to specify bus object
    )

    high_medium_transformator = components.Connector(
        name="High Voltage Transformator",
        interfaces=(str(medium_electricity_line.uid), str(high_electricity_line.uid)),
        conversions={
            (str(medium_electricity_line.uid), str(high_electricity_line.uid)): 1,
            (
                str(high_electricity_line.uid),
                str(medium_electricity_line.uid),
            ): 1,
        },
        timeseries=None,
        node_type="connector",
        sector="coupled",
    )

    # Building the Energysystem

    esys = energy_system.AbstractEnergySystem(
        uid="Generic_Grid",
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
        transformers=(bhkw_generator, power_to_heat, gud_generator, hkw_generator),
        storages=(battery_storage, heat_storage, pumped_storage),
        connectors=(low_medium_transformator, high_medium_transformator),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )

    return esys


# pylint: enable=too-many-locals
# pylint: enable=duplicate-code
