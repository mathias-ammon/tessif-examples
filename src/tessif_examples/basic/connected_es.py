# src/tessif_examples/conected_es.py
"""Tessif minimum working example energy system model."""
import tessif.namedtuples as nts
import numpy as np
from pandas import date_range
from tessif.model import components, energy_system


def create_connected_es(directory=None, filename=None):
    """
    Create a minimal working example using :mod:`tessif's
    model <tessif.model>` connecting to seperate energy systems using a
    :class:`tessif.model.components.Connector` object. Effectively creating
    a `transs hipment problem
    <https://en.wikipedia.org/wiki/Transshipment_problem>`_.

    Return
    ------
    :class:`tessif.model.energy_system.AbstractEnergySystem`
        Tessif energy system.

    References
    ----------
    :ref:`Models_Tessif_mwe` - For a step by step explanation on how to create
    a Tessif energy system.

    :ref:`AutoCompare_Transshipment` - For simulating and
    comparing this energy system using different supported models.

    :meth:`tessif.model.energy_system.AbstractEnergySystem.connect` - For the
    built in mehtod of tessif's energy systems.

    :ref:`Examples_Application_Computational` - For a comprehensive example
    on how to connect energy systems and how this can be used to measure
    computational scalability.

    Examples
    --------
    Visualize the energy system for better understanding what the output means:

        from tessif-visualize import dcgraph as dcv

        app = dcv.draw_generic_graph(
            energy_system=create_connected_es(),
            color_group={
                'connector': '#9999ff',
                'bus-01': '#cc0033',
                'bus-02': '#00ccff',
            },
        )

        # Serve interactive drawing to http://127.0.0.1:8050/
        app.run_server(debug=False)


    .. image:: ../../_static/system_model_graphs/connected_es.png
        :align: center
        :alt: Image showing the connected_es energy system graph
    """

    timeframe = np.date_range('7/13/1990', periods=3, freq='H')

    s1 = components.Sink(
        name='sink-01',
        inputs=('electricity',),
        flow_rates={'electricity': nts.MinMax(min=0, max=15)},
        timeseries={'electricity': nts.MinMax(
            min=np.array([0, 15, 10]), max=np.array([0, 15, 10]))})

    so1 = components.Source(
        name='source-01',
        outputs=('electricity',),
        flow_rates={'electricity': nts.MinMax(min=0, max=10)},
        flow_costs={'electricity': 1},
        flow_emissions={'electricity': 0.8})

    mb1 = components.Bus(
        name='bus-01',
        inputs=('source-01.electricity',),
        outputs=('sink-01.electricity',),
    )

    s2 = components.Sink(
        name='sink-02',
        inputs=('electricity',),
        flow_rates={'electricity': nts.MinMax(min=0, max=15)},
        timeseries={'electricity': nts.MinMax(
            min=np.array([15, 0, 10]), max=np.array([15, 0, 10]))})

    so2 = components.Source(
        name='source-02',
        outputs=('electricity',),
        flow_rates={'electricity': nts.MinMax(min=0, max=10)},
        flow_costs={'electricity': 1},
        flow_emissions={'electricity': 1.2})

    mb2 = components.Bus(
        name='bus-02',
        inputs=('source-02.electricity',),
        outputs=('sink-02.electricity',),
    )

    c = components.Connector(
        name='connector',
        interfaces=('bus-01', 'bus-02'),
        conversions={('bus-01', 'bus-02'): 0.9,
                     ('bus-02', 'bus-01'): 0.8})

    connected_es = energy_system.AbstractEnergySystem(
        uid='Connected-Energy-Systems-Example',
        busses=(mb1, mb2),
        sinks=(s1, s2,),
        sources=(so1, so2),
        connectors=(c,),
        timeframe=timeframe
    )

    
    return connected_es

