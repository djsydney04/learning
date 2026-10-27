# Digital circuits and computer architecture, from the beginning

[SystemVerilog section](../verilong/README.md) · [Start with bits →](guide/01-bits-and-signals.md)

Before describing a CPU in SystemVerilog, it helps to understand what the
description is trying to build. This primer starts with voltages and bits,
builds up gates and clocked storage, then connects those pieces into the
Tiny8 processor in this repository. No prior electronics or architecture
course is assumed. You need only basic arithmetic to start.

The central idea is **computation plus state**. A circuit computes values
from its inputs. Storage remembers selected values. Connecting the two
lets a finite piece of hardware carry out a sequence of operations.

## The route

| Read in order | What you should be able to explain afterward |
| --- | --- |
| [1. Bits and signals](guide/01-bits-and-signals.md) | How voltage represents a bit, how binary and hex encode numbers, and why an 8-bit sum can wrap. |
| [2. Gates and Boolean logic](guide/02-gates-and-boolean-logic.md) | How truth tables describe circuits, and how bitwise operations differ from logical tests. |
| [3. Combinational circuits](guide/03-combinational-circuits.md) | How gates become muxes, decoders, adders, comparisons, and an ALU. |
| [4. State and the clock](guide/04-state-and-clock.md) | How registers remember, why updates use old values, how an FSM sequences work, and why timing matters. |
| [5. Memory and buses](guide/05-memory-and-buses.md) | How an address selects data, how reads and writes differ, and how CPU and RAM communicate. |
| [6. CPU architecture](guide/06-cpu-architecture.md) | How instruction bytes cause register transfers, traced through Tiny8 one edge at a time. |
| [7. Modern processors](guide/07-modern-processors.md) | How pipelines, caches, prediction, and parallelism improve performance while preserving the instruction contract. |
| [8. Reading and writing SystemVerilog](guide/08-systemverilog.md) | How the circuits map to modules, expressions, combinational blocks, clocked blocks, and testbenches. |

Use the [glossary](guide/glossary.md) when a term is unfamiliar. Each chapter
has questions with folded answers. The [practice problems](guide/practice.md)
combine ideas across chapters; the [references](guide/references.md) point to
original course materials and tool documentation for further study.

Twelve local diagrams accompany the explanations: voltage and bits, binary
overflow, gates and selectors, adders and the ALU, register feedback, clock
sampling, memory buses, Tiny8's datapath, instruction edges, pipelines,
memory hierarchy, and the RTL tool flow. Follow the labeled signals and
predict the next value before reading the surrounding explanation.

Read chapters 1–5 before opening the CPU exercise. Chapter 6 is the bridge
to that exercise. Chapter 7 adds context for laptop and server CPUs; you can
return to it after building Tiny8. Chapter 8 translates the hardware ideas
into the language you will use.

## Try the ideas without a hardware toolchain

From the **repository root**, run:

```sh
python3 cpu-architecture/experiments/01_logic.py
python3 cpu-architecture/experiments/02_clock.py
python3 cpu-architecture/experiments/03_tiny8.py
```

These require Python 3.10 or newer and no extra packages. First predict the
output on paper. The programs show gates and a ripple adder, simultaneous
register updates, and the intended Tiny8 instruction cycle.

The Python programs are **teaching models**, executed by your existing CPU.
They do not simulate the `.sv` files, validate your CPU implementation, or
model propagation delays and metastability. In particular, a successful
Tiny8 model run says what the exercise is aiming for, not that its RTL is
finished.

For an actual SystemVerilog simulation of a small, completed two-register
circuit, see [chapter 8](guide/08-systemverilog.md). It needs Icarus Verilog
(`iverilog` and `vvp`), but no FPGA or physical board.

## Connect this to the CPU project

After the primer, continue in this order:

1. [Tiny8 introduction](../verilong/cpu/intro.md): identify the components in its diagrams.
2. [One instruction, slowly](../verilong/cpu/walkthrough.md): predict each row before reading it.
3. [Tiny8 implementation guide](../verilong/cpu/README.md): implement the existing student exercises.

The Tiny8 source contains unfinished student work. The primer explains its
intended contract without filling in those exercises. Its 8-bit accumulator,
256-byte memory, asynchronous memory reads, and multicycle controller are
specific design choices, not rules every CPU follows.

## Check the primer

From the repository root:

```sh
make -C cpu-architecture check
make -C cpu-architecture rtl-demo
make -C cpu-architecture verify
```

`check` checks the Python models and local documentation links. `rtl-demo`
checks the completed SystemVerilog example. `verify` runs both. These
commands do not build or modify the unfinished Tiny8 source. See
[verification notes](examples/RESULTS.md) for what was actually checked.

## Regenerate the diagrams

The PNGs are checked in, so viewing the lessons requires no extra software.
Their [drawing scripts](scripts/render_diagrams.py) use Matplotlib and keep
the hardware connections, numbers, and timing examples reproducible.
With Matplotlib installed in your Python environment, run from the
repository root:

```sh
MPLCONFIGDIR=/tmp/cpu-architecture-mpl python3 cpu-architecture/scripts/render_diagrams.py
```

You can also run `make -C cpu-architecture diagrams`. Select another Python
environment with `DIAGRAM_PYTHON` if needed. Rendering is separate from
`make verify`; the models and RTL demonstration do not require Matplotlib.
