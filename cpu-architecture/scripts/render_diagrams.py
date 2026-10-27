#!/usr/bin/env python3
"""Regenerate the primer's PNG diagrams (requires Matplotlib).

From the repository root with the existing diagram environment:
MPLCONFIGDIR=/tmp/cpu-architecture-mpl transformer/.venv/bin/python cpu-architecture/scripts/render_diagrams.py

Any Python environment with Matplotlib can render these figures. Reading
the checked-in PNGs and running the teaching models need no Matplotlib.
"""

from draw_circuits import render_all as circuits
from draw_architecture import render_all as architecture


if __name__ == "__main__":
    circuits()
    architecture()
