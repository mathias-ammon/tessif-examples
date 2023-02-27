"""Dynamically access tessif-examples paths."""
import inspect
import os

root_dir = os.path.normpath(
    os.path.join(
        inspect.getfile(inspect.currentframe()).split("paths")[0],
        "..",
        "..",
    )
)
"""Tessif-examples's root directory."""

data_dir = os.path.join(root_dir, "src", "tessif_examples", "data")
"""Tessif-examples data directory."""
