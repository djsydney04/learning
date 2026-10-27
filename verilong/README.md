# SystemVerilog

Start with the circuit you want to build, then learn how to describe it.
This path assumes no prior digital-electronics or CPU-architecture course.

| Path | What it is |
| --- | --- |
| [Digital circuits and computer architecture](../cpu-architecture/README.md) | Eight chapters: signals and bits, gates, combinational logic, clocked state, memory, CPU execution, modern processors, and SystemVerilog. Includes worked examples and self-check questions. |
| [Tiny8 introduction](cpu/intro.md) | A visual tour of the particular processor you will build. |
| [One instruction, slowly](cpu/walkthrough.md) | An ADD traced through each rising edge. |
| [Tiny8 implementation guide](cpu/README.md) | The existing CPU exercises: you write the RTL. |

## Start here

Read [bits and signals](../cpu-architecture/guide/01-bits-and-signals.md), then follow
the chapters in order. By the time you reach Tiny8, `PC`, mux, register,
ALU, and clock edge should name concrete circuit ideas.

Try the dependency-free teaching models from the repository root:

```sh
python3 cpu-architecture/experiments/01_logic.py
python3 cpu-architecture/experiments/02_clock.py
python3 cpu-architecture/experiments/03_tiny8.py
```

The Python models illustrate intended behavior; they do not run or verify
your SystemVerilog. The primer also includes a completed
[SystemVerilog example](../cpu-architecture/guide/08-systemverilog.md) for learning
simulation independently of the unfinished CPU.

Once you reach the CPU project, follow its [implementation guide](cpu/README.md).
Its simulation targets are exercises and require your implementation.
