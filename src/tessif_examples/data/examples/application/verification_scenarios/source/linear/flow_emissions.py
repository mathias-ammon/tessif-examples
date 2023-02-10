import numpy as np
import pandas as pd
import tessif.frused.namedtuples as nts

# flow_emissions
mapping = {
    "sources": {
        "s1": {
            "name": "source_1",
            "outputs": ("electricity",),
            "latitude": 42,
            "longitude": 42,
            "region": "Here",
            "sector": "Power",
            "carrier": "Electricity",
            "component": "source",
            "node_type": "source",
            "accumulated_amounts": {
                "electricity": nts.MinMax(min=0, max=float("+inf"))
            },
            "flow_rates": {"electricity": nts.MinMax(min=0, max=10)},
            "flow_costs": {"electricity": 1},
            "flow_emissions": {"electricity": 0},
            "flow_gradients": {
                "electricity": nts.PositiveNegative(positive=100, negative=100)
            },
            "gradient_costs": {
                "electricity": nts.PositiveNegative(positive=0, negative=0)
            },
            "timeseries": None,
        },
        "s2": {
            "name": "source_2",
            "outputs": ("electricity",),
            "latitude": 42,
            "longitude": 42,
            "region": "Here",
            "sector": "Power",
            "carrier": "Electricity",
            "component": "source",
            "node_type": "source",
            "accumulated_amounts": {
                "electricity": nts.MinMax(min=0, max=float("+inf"))
            },
            "flow_rates": {"electricity": nts.MinMax(min=0, max=10)},
            "flow_costs": {"electricity": 1},
            "flow_emissions": {"electricity": 10},
            "flow_gradients": {
                "electricity": nts.PositiveNegative(positive=100, negative=100)
            },
            "gradient_costs": {
                "electricity": nts.PositiveNegative(positive=0, negative=0)
            },
            "timeseries": None,
        },
    },
    "transformers": {},
    "sinks": {
        "sink": {
            "name": "sink",
            "inputs": ("electricity",),
            "latitude": 42,
            "longitude": 42,
            "region": "Here",
            "sector": "Power",
            "carrier": "Electricity",
            "node_type": "sink",
            "component": "sink",
            "accumulated_amounts": {
                "electricity": nts.MinMax(min=0, max=float("+inf"))
            },
            "flow_rates": {"electricity": nts.MinMax(min=10, max=10)},
        },
    },
    "storages": {},
    "busses": {
        "bus": {
            "name": "central_bus",
            "inputs": (
                "source_1.electricity",
                "source_2.electricity",
            ),
            "outputs": ("sink.electricity",),
            "latitude": 42,
            "longitude": 42,
            "region": "Here",
            "sector": "Power",
            "carrier": "Electricity",
            "node_type": "central_bus",
            "component": "bus",
        },
    },
    "timeframe": {
        "primary": pd.date_range("01/01/2022", periods=10, freq="H"),
    },
    "global_constraints": {
        "primary": {"name": "default", "emissions": 50, "material": float("+inf")},
    },
}
