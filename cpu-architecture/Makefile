PYTHON ?= python3
IVERILOG ?= iverilog
VVP ?= vvp
DIAGRAM_PYTHON ?= $(PYTHON)

.PHONY: help models check check-docs rtl-demo verify diagrams

help:
	@echo 'Read README.md, then guide/01-bits-and-signals.md'
	@echo 'make models      Run the three Python teaching demonstrations'
	@echo 'make check       Check the models and local documentation links'
	@echo 'make rtl-demo    Simulate the completed two-register SystemVerilog example'
	@echo 'make verify      Run check and rtl-demo (requires Icarus Verilog)'
	@echo 'make diagrams    Regenerate the local PNGs (requires Matplotlib)'

models:
	$(PYTHON) experiments/01_logic.py
	$(PYTHON) experiments/02_clock.py
	$(PYTHON) experiments/03_tiny8.py

check-docs:
	$(PYTHON) scripts/check_docs.py

check: check-docs
	$(PYTHON) -m unittest discover -s tests -v

rtl-demo:
	mkdir -p .build
	$(IVERILOG) -g2012 -s testbench -o .build/pipeline.vvp experiments/04_pipeline.sv
	$(VVP) .build/pipeline.vvp

verify: check rtl-demo

diagrams:
	MPLCONFIGDIR=/tmp/cpu-architecture-mpl $(DIAGRAM_PYTHON) scripts/render_diagrams.py
