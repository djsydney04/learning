# References and further study

[Primer](../README.md) · [Glossary](glossary.md) · [Practice](practice.md)

The primer's worked examples are written for this repository. The sources
below are original educational materials, hardware specifications, or
maintainers' documentation for checking details and studying further.
You do not need to read them before beginning the primer.

## Digital circuits and architecture

| Source | What to read it for |
| --- | --- |
| [MIT Computation Structures: lecture notes](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/pages/lecture-notes/) | Original lectures spanning digital abstraction, CMOS, sequential circuits, synchronization, processor design, caches, and operating-system mechanisms. |
| [Computation Structures: digital abstraction](https://computationstructures.org/notes/digitalabstraction/notes.html) | The relationship between physical voltage ranges, reliable signaling, and logic values. Complements chapter 1. |
| [Computation Structures: sequential logic](https://computationstructures.org/notes/sequential_logic/notes.html) | Why stored state allows a circuit to perform work across time. Complements chapter 4. |
| [Computation Structures: performance measures](https://computationstructures.org/lectures/performance/performance.html) | Pipeline latency, throughput, and timing budgets. Complements chapters 4 and 7. |
| [Nand to Tetris: hardware projects](https://www.nand2tetris.org/course) | An additional construction-based route from Boolean logic through arithmetic, memory, machine language, and a computer. It uses its own HDL and architecture, rather than SystemVerilog or Tiny8. |
| [Altera Quartus Timing Analyzer: metastability analysis](https://docs.altera.com/r/docs/683243/25.3/quartus-prime-pro-edition-user-guide-timing-analyzer/metastability-analysis) | Practical synchronizer analysis and statistical metastability reliability. Complements chapter 4; exact implementation guidance is target-specific. |
| [RISC-V: Unprivileged Architecture](https://docs.riscv.org/reference/isa/unpriv/unpriv-index.html) | An example of a real, public ISA specification. Compare a software-visible instruction contract with the microarchitecture that implements it. RISC-V encodings do not apply to Tiny8. |

## SystemVerilog, simulation, and synthesis

| Source | What to read it for |
| --- | --- |
| [lowRISC Verilog coding style guide](https://github.com/lowRISC/style-guides/blob/master/VerilogCodingStyle.md) | Practical RTL conventions for assignments, combinational defaults, widths, reset, and state machines. This is a project's style guide rather than the normative language standard. |
| [Icarus Verilog: getting started](https://steveicarus.github.io/iverilog/usage/getting_started.html) | Compilation with `iverilog`, execution with `vvp`, and small simulation examples. |
| [Icarus Verilog: command-line flags](https://steveicarus.github.io/iverilog/usage/command_line_flags.html) | Language-generation flags such as `-g2012` and other compiler options. Selecting a language generation does not guarantee support for every feature of that standard. |
| [Yosys: introduction](https://yosyshq.readthedocs.io/projects/yosys/en/stable/introduction.html) | What synthesis produces and where it fits in an FPGA or ASIC tool flow. Different tools and front ends support different SystemVerilog subsets. |

## This repository is the Tiny8 specification

Tiny8 is a local teaching design. Its opcodes, reset values, state names,
bus conventions, and intended register transfers come from these files:

- [cpu_pkg.sv](../../verilong/cpu/src/cpu_pkg.sv): opcode, state, and ALU-operation names.
- [CPU skeleton](../../verilong/cpu/src/cpu.sv): intended control sequence and reset values.
- [Memory skeleton](../../verilong/cpu/src/memory.sv): edge-triggered writes and combinational reads.
- [PC skeleton](../../verilong/cpu/src/pc.sv): reset, load, increment, and hold priority.
- [Implementation guide](../../verilong/cpu/README.md) and [walkthrough](../../verilong/cpu/walkthrough.md): intended behavior for the student exercise.

The unfinished source is not evidence that the circuit already works.
If you extend the ISA or change memory latency, update the contract,
teaching model, traces, and tests together. The Python model's zero-filled
initial memory and rejection of unknown opcodes are explicit teaching
choices; they do not specify physical RAM power-up state or an illegal-
instruction policy for the hardware.

For GPU organization and programming, read the
[CUDA foundations](../../cuda/foundations/README.md).
