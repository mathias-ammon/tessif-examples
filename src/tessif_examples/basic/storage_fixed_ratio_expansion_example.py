# src/tessif_examples/storage_fixed_expansion_example.py
"""Tessif minimum working example energy system model."""
import numpy as np
import pandas as pd
import tessif.namedtuples as nts
from pandas import date_range
from tessif.model import components, energy_system


def create_storage_fixed_ratio_expansion_example(directory=None, filename=None):
    """
     Create a small energy system utilizing an expandable storage with a fixed
     capacity to outflow ratio.

     Return
     ------
     es: :class:`tessif.model.energy_system.AbstractEnergySystem`
         Tessif energy system.

     Warning
     -------
     In this example the installed capacity is set to 1, but expandable.
     The flow rate to 0.1. By enabling both expandables (capacity and flow rate)
     as well as fixing their ratios the installed capacity result will be
     much higher than needed. Or in other words, the flow rate will determine
     the amount of installed capacity.

     References
     ----------
     :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
     a Tessif energy system.

     :ref:`AutoCompare_Storage` - For simulating and
     comparing this energy system using different supported models.

     Examples
     --------
     Using :func:`create_storage_fixed_ratio_expansion_example` to quickly
     access a tessif energy system to use for doctesting, or trying out this
     frameworks utilities.

         import tessif.examples.data.tsf.py_hard as coded_examples
         tsf_es = coded_examples.create_storage_fixed_ratio_expansion_example()

         for node in tsf_es.nodes:
             print(node.uid.name)
         Powerline
         Generator
         Demand
         Storage

     Transform the tessif energy system into oemof and pypsa:

         # Import the model transformation utilities:
         from tessif.transform.es2es import (
             ppsa as tsf2pypsa,
             omf as tsf2omf,
         )

         # Do the transformation:
         oemof_es = tsf2omf.transform(tsf_es)
         pypsa_es = tsf2pypsa.transform(tsf_es)

     Do some examplary checks on the flow conversions:

         # oemof:
         for node in oemof_es.nodes:
             if node.label.name == 'Storage':
             print(node.inflow_conversion_factor[0])
             print(node.outflow_conversion_factor[0])
     0.95
     0.89

         # pypsa:
         print(pypsa_es.storage_units['efficiency_store']['Storage'])
     0.95
         print(pypsa_es.storage_units['efficiency_dispatch']['Storage'])
     0.89

     Simulate the transformed energy system:

         # Import the simulation utility:
         import tessif.simulate

         # Optimize the energy systems:
         optimized_oemof_es = tessif.simulate.omf_from_es(oemof_es)
         optimized_pypsa_es = tessif.simulate.ppsa_from_es(pypsa_es)

     Do some post processing:

         # Import the post processing utilities:
         from tessif.transform.es2mapping import (
             ppsa as post_process_pypsa,
             omf as post_process_oemof,
         )

         # Conduct the post processing:
         oemof_load_results = post_process_oemof.LoadResultier(
             optimized_oemof_es)
         pypsa_load_results = post_process_pypsa.LoadResultier(
             optimized_pypsa_es)

     Check if the load results are the same as in the example above:

         # oemof:
         oemof_loads = post_process_oemof.LoadResultier(optimized_oemof_es)
         print(oemof_loads.node_load['Powerline'])
     Powerline            Generator  Storage  Demand  Storage
     1990-07-13 00:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 01:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 02:00:00      -19.0     -0.0     7.0     12.0
     1990-07-13 03:00:00       -0.0    -10.0    10.0      0.0
     1990-07-13 04:00:00       -0.0    -10.0    10.0      0.0

         # pypsa:
         pypsa_loads = post_process_pypsa.LoadResultier(optimized_pypsa_es)
         print(pypsa_loads.node_load['Powerline'])
     Powerline            Generator  Storage  Demand  Storage
     1990-07-13 00:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 01:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 02:00:00      -19.0     -0.0     7.0     12.0
     1990-07-13 03:00:00       -0.0    -10.0    10.0      0.0
     1990-07-13 04:00:00       -0.0    -10.0    10.0      0.0

     Check the installed capacity:

         # oemof:
         oemof_capacities = post_process_oemof.CapacityResultier(
             optimized_oemof_es)
         print(oemof_capacities.node_installed_capacity['Storage'])
     120.0

         # pypsa:
         pypsa_capacities = post_process_pypsa.CapacityResultier(
             optimized_pypsa_es)
         print(pypsa_capacities.node_installed_capacity['Storage'])
     120.0

     The integrated global results or high priority resutls:

         # oemof:
         oemof_hps = post_process_oemof.IntegratedGlobalResultier(
             optimized_oemof_es)
         for key, result in oemof_hps.global_results.items():
             if 'emissions' not in key:
                 print(f'{key}: {result}')
     costs (sim): 258.0
     opex (ppcd): 20.0
     capex (ppcd): 238.0

         # pypsa:
         pypsa_hps = post_process_pypsa.IntegratedGlobalResultier(
             optimized_pypsa_es)
         for key, result in pypsa_hps.global_results.items():
             if 'emissions' not in key:
                 print(f'{key}: {result}')
     costs (sim): 258.0
     opex (ppcd): 20.0
     capex (ppcd): 238.0

     And to check the state of charge results:

         # oemof:
         oemof_socs = post_process_oemof.StorageResultier(optimized_oemof_es)
         print(oemof_socs.node_soc['Storage'])
     1990-07-13 00:00:00     8.550000
     1990-07-13 01:00:00    17.100000
     1990-07-13 02:00:00    28.500000
     1990-07-13 03:00:00    17.264045
     1990-07-13 04:00:00     6.028090
     Freq: H, Name: Storage, dtype: float64

         # pypsa:
         pypsa_socs = post_process_pypsa.StorageResultier(optimized_pypsa_es)
         print(pypsa_socs.node_soc['Storage'])
     1990-07-13 00:00:00     8.550000
     1990-07-13 01:00:00    17.100000
     1990-07-13 02:00:00    28.500000
     1990-07-13 03:00:00    17.264045
     1990-07-13 04:00:00     6.028090
     Freq: H, Name: Storage, dtype: float64

     Visualize the energy system for better understanding what the output means:

    from tessif-visualize import dcgraph as dcv

         app = dcv.draw_generic_graph(
             energy_system=create_storage_fixed_ratio_expansion_example(),
             color_group={'Powerline': '#009900',
                 'Storage': '#cc0033',
                 'Demand': '#00ccff',
                 'Generator': '#ffD700',
             },
         )

         # Serve interactive drawing to http://127.0.0.1:8050/
         app.run_server(debug=False)

         .. image:: ../images/storage_es_example.png
             :align: center
             :alt: Image showing the create_storage_example energy system graph.

     Reparameterize the storage component usinng one of tessif's
     :attr:`hooks <tessif.frused.hooks.tsf.reparameterize_components>`, to
     unbind capacity and flow rate expansion:

         from tessif.frused.hooks.tsf import reparameterize_components
         reparameterized_es = reparameterize_components(
             es=tsf_es,
             components={
                 'Storage': {
                     'fixed_expansion_ratios': {'electricity': False},
                 },
             },
         )

     Redo the transformations and simulations:

         # Transformation:
         oemof_es = tsf2omf.transform(reparameterized_es)
         pypsa_es = tsf2pypsa.transform(reparameterized_es)

         # Optimization/Simulation:
         optimized_oemof_es = tessif.simulate.omf_from_es(oemof_es)
         optimized_pypsa_es = tessif.simulate.ppsa_from_es(pypsa_es)

     Recheck installed capacities socs and loads:

     Installed capacity:

         # oemof:
         oemof_capacities = post_process_oemof.CapacityResultier(
             optimized_oemof_es)
         print(oemof_capacities.node_installed_capacity['Storage'])
     28.5

         # pypsa:
         pypsa_capacities = post_process_pypsa.CapacityResultier(
             optimized_pypsa_es)
         print(pypsa_capacities.node_installed_capacity['Storage'])
     120.0

     Note
     ----
     Note how oemof is able to unbind these values, whereas pypsa is not.


     Integrated global results or high priority resutls:

         # oemof:
         oemof_hps = post_process_oemof.IntegratedGlobalResultier(
             optimized_oemof_es)
         for key, result in oemof_hps.global_results.items():
             if 'emissions' not in key:
                 print(f'{key}: {result}')
     costs (sim): 75.0
     opex (ppcd): 20.0
     capex (ppcd): 55.0

         # pypsa:
         pypsa_hps = post_process_pypsa.IntegratedGlobalResultier(
             optimized_pypsa_es)
         for key, result in pypsa_hps.global_results.items():
             if 'emissions' not in key:
                 print(f'{key}: {result}')
     costs (sim): 258.0
     opex (ppcd): 20.0
     capex (ppcd): 238.0

     Note
     ----
     Note how PyPSA still calculates higher capex for the storage expansion,
     since cpacity and power ratio are fixed.

     State of charge results:

         # oemof:
         oemof_socs = post_process_oemof.StorageResultier(optimized_oemof_es)
         print(oemof_socs.node_soc['Storage'])
     1990-07-13 00:00:00     8.550000
     1990-07-13 01:00:00    17.100000
     1990-07-13 02:00:00    28.500000
     1990-07-13 03:00:00    17.264045
     1990-07-13 04:00:00     6.028090
     Freq: H, Name: Storage, dtype: float64

         # pypsa:
         pypsa_socs = post_process_pypsa.StorageResultier(optimized_pypsa_es)
         print(pypsa_socs.node_soc['Storage'])
     1990-07-13 00:00:00     8.550000
     1990-07-13 01:00:00    17.100000
     1990-07-13 02:00:00    28.500000
     1990-07-13 03:00:00    17.264045
     1990-07-13 04:00:00     6.028090
     Freq: H, Name: Storage, dtype: float64

     Loads:

         # oemof:
         oemof_loads = post_process_oemof.LoadResultier(optimized_oemof_es)
         print(oemof_loads.node_load['Powerline'])
     Powerline            Generator  Storage  Demand  Storage
     1990-07-13 00:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 01:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 02:00:00      -19.0     -0.0     7.0     12.0
     1990-07-13 03:00:00       -0.0    -10.0    10.0      0.0
     1990-07-13 04:00:00       -0.0    -10.0    10.0      0.0

         # pypsa:
         pypsa_loads = post_process_pypsa.LoadResultier(optimized_pypsa_es)
         print(pypsa_loads.node_load['Powerline'])
     Powerline            Generator  Storage  Demand  Storage
     1990-07-13 00:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 01:00:00      -19.0     -0.0    10.0      9.0
     1990-07-13 02:00:00      -19.0     -0.0     7.0     12.0
     1990-07-13 03:00:00       -0.0    -10.0    10.0      0.0
     1990-07-13 04:00:00       -0.0    -10.0    10.0      0.0
    """

    timeframe = pd.date_range("7/13/1990", periods=5, freq="H")

    demand = components.Sink(
        name="Demand",
        inputs=("electricity",),
        carrier="electricity",
        node_type="sink",
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([10, 10, 7, 10, 10]), max=np.array([10, 10, 7, 10, 10])
            )
        },
    )

    generator = components.Source(
        name="Generator",
        outputs=("electricity",),
        carrier="electricity",
        node_type="source",
        flow_rates={"electricity": nts.MinMax(min=0, max=10)},
        flow_costs={"electricity": 0},
        timeseries={
            "electricity": nts.MinMax(
                min=np.array([19, 19, 19, 0, 0]), max=np.array([19, 19, 19, 0, 0])
            )
        },
    )

    powerline = components.Bus(
        name="Powerline",
        inputs=("Generator.electricity", "Storage.electricity"),
        outputs=(
            "Demand.electricity",
            "Storage.electricity",
        ),
        carrier="electricity",
        node_type="bus",
    )

    storage = components.Storage(
        name="Storage",
        input="electricity",
        output="electricity",
        capacity=1,
        initial_soc=0,
        carrier="electricity",
        node_type="storage",
        flow_rates={"electricity": nts.MinMax(min=0, max=0.1)},
        flow_efficiencies={"electricity": nts.InOut(inflow=0.95, outflow=0.89)},
        flow_costs={"electricity": 1},
        flow_emissions={"electricity": 0.5},
        expandable={"capacity": True, "electricity": True},
        fixed_expansion_ratios={"electricity": True},
        expansion_costs={"capacity": 2, "electricity": 0},
        expansion_limits={
            "capacity": nts.MinMax(min=1, max=float("+inf")),
            "electricity": nts.MinMax(min=0.1, max=float("+inf")),
        },
    )

    # energy dissipation parameterization
    # storage = components.Storage(
    #     name='Storage',
    #     input='electricity',
    #     output='electricity',
    #     capacity=1,
    #     initial_soc=0,
    #     carrier='electricity',
    #     node_type='storage',
    #     flow_rates={'electricity': nts.MinMax(min=0, max=0.9)},
    #     flow_efficiencies={
    #          'electricity': nts.InOut(inflow=0.8, outflow=0.9)},
    #     flow_costs={'electricity': 3},
    #     flow_emissions={'electricity': 0.5},
    #     expandable={'capacity': True, 'electricity': True},
    #     fixed_expansion_ratios={'electricity': True},
    #     expansion_costs={'capacity': 5, 'electricity': 0},
    #     expansion_limits={
    #         'capacity': nts.MinMax(min=1, max=float('+inf')),
    #         'electricity': nts.MinMax(min=0.9, max=float('+inf'))},
    # )

    storage_es = energy_system.AbstractEnergySystem(
        uid="Storage-Energysystem-Example",
        busses=(powerline,),
        sinks=(demand,),
        sources=(generator,),
        storages=(storage,),
        timeframe=timeframe,
    )

    return storage_es
