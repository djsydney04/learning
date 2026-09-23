# Icarus Verilog: compile the chip + testbench, then run the simulation.
#
#   make sim      full CPU + your program in tb/cpu_tb.sv
#   make sim-alu  ALU alone, using tb/alu_tb.sv
#   make clean    delete waves/
#
# -g2012 turns on SystemVerilog (always_ff, logic, enums, packages).

IVERILOG ?= iverilog
VVP      ?= vvp
WAVEDIR  := waves

# Package first so the other files can import it.
SRC := \
	src/cpu_pkg.sv \
	src/alu.sv \
	src/decoder.sv \
	src/pc.sv \
	src/memory.sv \
	src/cpu.sv \
	src/tiny8.sv

TB     := tb/cpu_tb.sv
ALU_TB := tb/alu_tb.sv

.PHONY: sim sim-alu waves clean

sim: $(WAVEDIR)
	$(IVERILOG) -g2012 -o $(WAVEDIR)/tiny8.vvp $(SRC) $(TB)
	$(VVP) $(WAVEDIR)/tiny8.vvp

sim-alu: $(WAVEDIR)
	$(IVERILOG) -g2012 -o $(WAVEDIR)/alu.vvp src/cpu_pkg.sv src/alu.sv $(ALU_TB)
	$(VVP) $(WAVEDIR)/alu.vvp

$(WAVEDIR):
	mkdir -p $(WAVEDIR)

clean:
	rm -rf $(WAVEDIR)
