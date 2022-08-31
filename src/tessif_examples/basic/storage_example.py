# src/tessif_examples/storage_example.py
"""Tessif minimum working example energy system model."""
import tessif.namedtuples as nts
import numpy as np
from pandas import date_range
from tessif.model import components, energy_system



def create_storage_example(directory=None, filename=None):
    """
    Create a small energy system utilizing a storage.

    Return
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    Warning
    -------
    In this example the installed capacity is set to 0, but expandable
    (A common use case). Most, if not any, of the
    :ref:`supported models <SupportedModels>` however, use capacity specific
    values for idle losses and initial as well as final soc constraints.

    Given the initial capacity is 0, this problem is solved by setting the
    initial soc as well as the idle losses to 0, if necessary.

    To avoid this caveat, set the inital capacity to a small value and adjust
    initial soc and idle changes accordingly. This might involve some trial and
    error.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`AutoCompare_Storage` - For simulating and
    comparing this energy system using different supported models.

    Examples
    --------
    Using :func:`create_storage_example` to quickly access a tessif energy
    system to use for doctesting, or trying out this frameworks utilities.

        import tessif.examples.data.tsf.py_hard as coded_examples
        tsf_es = coded_examples.create_storage_example()

        for node in tsf_es.nodes:
            print(node.uid.name)
        Powerline
        Generator
        Demand
        Storage

    Visualize the energy system for better understanding what the output means:

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_storage_es_example(),
            color_group={
                'Powerline': '#009900',
                'Storage': '#cc0033',
                'Demand': '#00ccff',
                'Generator': '#ffD700',
            },
        )
        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)

    .. image:: ../../_static/system_model_graphs/storage_es_example.png
        :align: center
        :alt: Image showing the create_storage_example energy system graph.
    """

    timeframe = np.date_range('7/13/1990', periods=5, freq='H')

    demand = components.Sink(
        name='Demand',
        inputs=('electricity',),
        carrier='electricity',
        node_type='sink',
        flow_rates={'electricity': nts.MinMax(min=0, max=10)},
        timeseries={
            'electricity': nts.MinMax(
                min=np.array([10, 10, 7, 10, 10]),
                max=np.array([10, 10, 7, 10, 10])
            )
        }
    )

    generator = components.Source(
        name='Generator',
        outputs=('electricity',),
        carrier='electricity',
        node_type='source',
        flow_rates={'electricity': nts.MinMax(min=0, max=10)},
        flow_costs={'electricity': 2},
        timeseries={
            'electricity': nts.MinMax(
                min=np.array([19, 19, 19, 0, 0]),
                max=np.array([19, 19, 19, 0, 0])
            )
        }
    )

    powerline = components.Bus(
        name='Powerline',
        inputs=('Generator.electricity', 'Storage.electricity'),
        outputs=('Demand.electricity', 'Storage.electricity',),
        carrier='electricity',
        node_type='bus',
    )

    storage = components.Storage(
        name='Storage',
        input='electricity',
        output='electricity',
        capacity=0,
        initial_soc=0,
        carrier='electricity',
        node_type='storage',
        flow_efficiencies={
             'electricity': nts.InOut(inflow=0.9, outflow=0.9)},
        flow_costs={'electricity': 1},
        flow_emissions={'electricity': 0.5},
        expandable={'capacity': True, 'electricity': False},
        expansion_costs={'capacity': 0, 'electricity': 0},
        expansion_limits={
            'capacity': nts.MinMax(min=0, max=float('+inf')),
            'electricity': nts.MinMax(min=0, max=float('+inf'))},
    )

    storage_es = energy_system.AbstractEnergySystem(
        uid='Storage-Energysystem-Example',
        busses=(powerline,),
        sinks=(demand,),
        sources=(generator,),
        storages=(storage,),
        timeframe=timeframe
    )


    return storage_es


