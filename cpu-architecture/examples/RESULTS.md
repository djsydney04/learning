# Primer verification

[Primer](../README.md)

Checks run on October 27, 2026. All commands below start at the repository
root and leave the student CPU source untouched.

| Command | Result and scope |
| --- | --- |
| `make -C cpu-architecture check` | Local Markdown links, linked headings, table structure, code fences, answer panels, and 16 Python model tests. |
| `make -C cpu-architecture models` | Logic, register-update, and default Tiny8 demonstrations execute successfully. |
| `python3 cpu-architecture/experiments/03_tiny8.py --demo countdown` | Model reaches HALT after 42 active edges, with A = 0 and memory[`80`] = 0. |
| `python3 cpu-architecture/experiments/03_tiny8.py --demo load` | Model reaches HALT after 15 active edges, with A = 42 and memory[`80`] = 42. |
| `make -C cpu-architecture rtl-demo` | Icarus compiles and runs the completed two-register example; checks old-value transfers, enable hold, and reset. |

## Diagram checks

The twelve local PNG diagrams were generated with Matplotlib 3.11.2 and
visually inspected for readable labels, signal direction, arithmetic, and
clock-edge alignment. Their drawing code lives in
[scripts/render_diagrams.py](../scripts/render_diagrams.py). Regenerate
them from the repository root with a Python environment containing
Matplotlib:

```sh
MPLCONFIGDIR=/tmp/cpu-architecture-mpl python3 cpu-architecture/scripts/render_diagrams.py
```

The figures are teaching diagrams, not measured waveforms or physical
layout/timing reports. The sampling waveform omits physical delays; the
pipeline is a hypothetical five-stage machine, not Tiny8's multicycle
controller. Viewing the PNGs and running `make verify` need no Matplotlib.

## Scope

The Python checks compare every pair of 8-bit unsigned adder operands
against integer arithmetic, verify a hand-derived 14-edge Tiny8 trace,
and exercise opcode results, flags, taken and untaken branches, memory
timing, wraparound, reset, halt, and bounded nontermination.

The RTL demo is a separate completed component, not a completed Tiny8 CPU.
The Python models neither execute nor verify the student `.sv` files.
No FPGA synthesis, placement, routing, physical timing, or board behavior
has been validated by these checks.
