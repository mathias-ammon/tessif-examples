# src/tessif_examples/chp.py
"""Tessif minimum working example energy system model."""
import tessif.namedtuples as nts
import numpy as np
from pandas import date_range
from tessif.model import components, energy_system

def create_chp(directory=None, filename=None):
    """
    Create a minimal working example using :mod:`tessif's
    model <tessif.model>` optimizing it for costs to demonstrate
    a chp application.

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
        es = tsf_py.create_chp()

        for node in es.nodes:
            print(node.uid)
        Gas Grid
        Powerline
        Heat Grid
        Gas Source
        Backup Power
        Backup Heat
        Power Demand
        Heat Demand
        CHP
    
    Visualize the energy system for better understanding what the output means::

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_chp(),
            color_group={
                'Gas Source': '#336666',
                'Gas Grid': '#336666',
                'CHP': '#006666',
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

    .. image:: ../../_static/system_model_graphs/chp.png
        :align: center
        :alt: Image showing the chp energy system graph
    """

    # 2. Create a simulation time frame of four one-hour timesteps as a
    # :class:`pandas.DatetimeIndex`:
    timeframe = np.date_range('7/13/1990', periods=4, freq='H')

    global_constraints = {'emissions': float('+inf')}

    # 3. Creating the individual energy system components:
    gas_supply = components.Source(
        name='Gas Source',
        outputs=('gas',),
        # Minimum number of arguments required
    )

    gas_grid = components.Bus(
        name='Gas Grid',
        inputs=('Gas Source.gas', ),
        outputs=('CHP.gas',),
        # Minimum number of arguments required
    )

    # conventional power supply is cheaper, but has emissions allocated to it
    chp = components.Transformer(
        name='CHP',
        inputs=('gas',),
        outputs=('electricity', 'heat'),
        conversions={
            ('gas', 'electricity'): 0.3,
            ('gas', 'heat'): 0.2,
        },
        # Minimum number of arguments required
        # flow_rates={
        #     'electricity': (0, 9),
        #     'heat': (0, 6),
        #     'gas': (0, float('+inf'))
        # },
        flow_costs={'electricity': 3, 'heat': 2, 'gas': 0},
        flow_emissions={'electricity': 2, 'heat': 3, 'gas': 0},
    )

    # back up power, expensive
    backup_power = components.Source(
        name='Backup Power',
        outputs=('electricity',),
        flow_costs={'electricity': 10},
    )

    # Power demand needing 10 energy units per time step
    power_demand = components.Sink(
        name='Power Demand',
        inputs=('electricity',),
        # Minimum number of arguments required
        flow_rates={'electricity': nts.MinMax(min=10, max=10)},
    )

    power_line = components.Bus(
        name='Powerline',
        inputs=('Backup Power.electricity', 'CHP.electricity'),
        outputs=('Power Demand.electricity',),
        # Minimum number of arguments required
    )

    # Back up heat source, expensive
    backup_heat = components.Source(
        name='Backup Heat',
        outputs=('heat',),
        flow_costs={'heat': 10},
    )

    # Heat demand needing 10 energy units per time step
    heat_demand = components.Sink(
        name='Heat Demand',
        inputs=('heat',),
        # Minimum number of arguments required
        flow_rates={'heat': nts.MinMax(min=10, max=10)},
    )

    heat_grid = components.Bus(
        name='Heat Grid',
        inputs=('CHP.heat', 'Backup Heat.heat'),
        outputs=('Heat Demand.heat',),
        # Minimum number of arguments required
    )

    # 4. Creating the actual energy system:
    explicit_es = energy_system.AbstractEnergySystem(
        uid='CHP_Example',
        busses=(gas_grid, power_line, heat_grid),
        sinks=(power_demand, heat_demand),
        sources=(gas_supply, backup_power, backup_heat),
        transformers=(chp,),
        timeframe=timeframe,
        global_constraints=global_constraints,
    )


    return explicit_es
