# Circuit and architecture glossary

[Primer](../README.md) · [Practice](practice.md) · [References](references.md)

Read the linked chapter for the explanation and example. The definitions
here are reminders, not prerequisites you must memorize.

## Signals and logic

| Term | Meaning | Read |
| --- | --- | --- |
| Bit | One binary value, 0 or 1. | [1](01-bits-and-signals.md) |
| Digital abstraction | Interpreting continuous physical signals as discrete logic values under specified electrical and timing conditions. | [1](01-bits-and-signals.md) |
| Noise margin | Separation between guaranteed output levels and acceptable input levels that tolerates some disturbance. | [1](01-bits-and-signals.md) |
| Transistor | Electrically controlled device used to build switching and storage circuits. | [1](01-bits-and-signals.md) |
| CMOS | Complementary transistor technology commonly used to implement digital circuits. | [1](01-bits-and-signals.md) |
| Bus / vector | Several related signals treated as a group, such as eight data bits. | [1](01-bits-and-signals.md) |
| Byte | Eight bits; one addressed memory location in Tiny8. | [1](01-bits-and-signals.md) |
| Hexadecimal | Base-16 notation; each digit represents four bits. | [1](01-bits-and-signals.md) |
| Two's complement | Signed-integer encoding with a negative weight for the most significant bit. | [1](01-bits-and-signals.md) |
| Carry | The extra bit carried beyond an addition's selected width. | [1](01-bits-and-signals.md) |
| Signed overflow | An exact signed result falls outside the representable signed range. | [1](01-bits-and-signals.md) |
| Sign extension | Widening a two's-complement pattern by repeating its sign bit. | [1](01-bits-and-signals.md) |
| Logic gate | Circuit implementing a Boolean function. | [2](02-gates-and-boolean-logic.md) |
| Truth table | The output for every combination of discrete input values. | [2](02-gates-and-boolean-logic.md) |
| Bitwise operation | A separate Boolean operation at each corresponding bit position. | [2](02-gates-and-boolean-logic.md) |
| Reduction | Combining the bits of one vector into one result bit. | [2](02-gates-and-boolean-logic.md) |
| Combinational circuit | Circuit whose settled outputs depend on current inputs, without remembered state. | [3](03-combinational-circuits.md) |
| Mux | Multiplexer: selects one input value to pass to an output. | [3](03-combinational-circuits.md) |
| Decoder | Recognizes an encoded input and produces corresponding selections or control facts. | [3](03-combinational-circuits.md) |
| Full adder | Adds two input bits and a carry-in, producing sum and carry-out. | [3](03-combinational-circuits.md) |
| ALU | Arithmetic logic unit: selects among arithmetic and bitwise results. | [3](03-combinational-circuits.md) |
| Propagation delay | Time for an input change to produce a valid settled output. | [4](04-state-and-clock.md) |
| Glitch | A transient output change caused, for example, by unequal path delays. | [2](02-gates-and-boolean-logic.md) |

## State and memory

| Term | Meaning | Read |
| --- | --- | --- |
| State | Stored information through which a circuit's history affects its future behavior. | [4](04-state-and-clock.md) |
| Latch | Storage element transparent while its controlling level is active. | [4](04-state-and-clock.md) |
| Flip-flop | Storage element sampling data around a designated clock edge. | [4](04-state-and-clock.md) |
| Register | A group of stored bits used as one value. | [4](04-state-and-clock.md) |
| Clock period | Time between corresponding successive clock edges. | [4](04-state-and-clock.md) |
| Enable | Control selecting whether a register updates or holds. | [4](04-state-and-clock.md) |
| Reset | Mechanism establishing specified starting register values. | [4](04-state-and-clock.md) |
| FSM | Finite state machine: stored current state plus next-state and output logic. | [4](04-state-and-clock.md) |
| Moore / Mealy | FSM output depending only on state / on state and current inputs. | [4](04-state-and-clock.md) |
| Setup / hold | Input-stability requirements before / after a sampling edge. | [4](04-state-and-clock.md) |
| Clock skew | Difference in arrival time of related clock edges at different registers. | [4](04-state-and-clock.md) |
| Metastability | Analog behavior in which a storage element takes time to resolve to a valid level. | [4](04-state-and-clock.md) |
| Clock domain | Logic coordinated by a particular clock and its timing relationship. | [4](04-state-and-clock.md) |
| Synchronizer | Circuit reducing the probability that metastability propagates across a suitable asynchronous transfer. | [4](04-state-and-clock.md) |
| Address | Identifier selecting a memory location; distinct from its contents. | [5](05-memory-and-buses.md) |
| Write enable | Control requesting a memory write at the specified write event. | [5](05-memory-and-buses.md) |
| Asynchronous read | Read data follows address selection without a read clock edge, after access delay. | [5](05-memory-and-buses.md) |
| Synchronous read | A read operation governed by a clocked interface with specified latency. | [5](05-memory-and-buses.md) |
| SRAM / DRAM | Volatile memory using stable storage cells / charge storage requiring refresh. | [5](05-memory-and-buses.md) |
| Endianness | Order in which the bytes of a multibyte value occupy addressed locations. | [5](05-memory-and-buses.md) |

## Processors and RTL

| Term | Meaning | Read |
| --- | --- | --- |
| Core | An instruction-executing engine inside a processor. | [6](06-cpu-architecture.md) |
| ISA | Instruction set architecture: the software-visible instruction contract. | [6](06-cpu-architecture.md) |
| Microarchitecture | Circuit organization implementing an ISA. | [6](06-cpu-architecture.md) |
| Opcode | Encoded instruction operation. Tiny8 stores it in the first instruction byte. | [6](06-cpu-architecture.md) |
| Immediate | A value supplied as part of an instruction, rather than fetched through a data address. | [6](06-cpu-architecture.md) |
| Accumulator, A | Tiny8's main working register. | [6](06-cpu-architecture.md) |
| PC | Program counter: in Tiny8, the address of the next program byte to fetch. | [6](06-cpu-architecture.md) |
| IR | Instruction register: in Tiny8, the stored opcode. | [6](06-cpu-architecture.md) |
| Z | Stored zero flag; normally updated from the new accumulator value in Tiny8, with an explicit reset exception. | [6](06-cpu-architecture.md) |
| Datapath | Registers, arithmetic, and connections through which values are transferred and transformed. | [6](06-cpu-architecture.md) |
| Control unit | Logic selecting the datapath's actions. | [6](06-cpu-architecture.md) |
| Pipeline | Stages that overlap work on different items or instructions. | [7](07-modern-processors.md) |
| Hazard | Dependency or resource conflict that prevents an assumed pipeline step. | [7](07-modern-processors.md) |
| Forwarding | Routing an available result directly to its consumer before normal register-file write/read. | [7](07-modern-processors.md) |
| CPI | Average cycles per instruction over a specified execution. | [7](07-modern-processors.md) |
| Cache | Storage of memory blocks intended to make subsequent accesses cheaper. | [7](07-modern-processors.md) |
| Locality | Tendency to reuse recent values or access nearby locations. | [7](07-modern-processors.md) |
| Speculation | Doing work before knowing whether it will be needed or permitted to commit. | [7](07-modern-processors.md) |
| Retirement | Making a completed instruction's results architecturally committed. | [7](07-modern-processors.md) |
| RTL | Register-transfer level: a description of state and the logic governing transfers between storage elements. | [8](08-systemverilog.md) |
| Module / port | A component description / one of its connection points. | [8](08-systemverilog.md) |
| Elaboration | Resolving instances, parameters, and connections into the design hierarchy used by a tool. | [8](08-systemverilog.md) |
| Synthesis | Translating supported design descriptions into a circuit netlist. | [8](08-systemverilog.md) |
| FPGA / ASIC | Configurable hardware / a chip manufactured for a particular design. | [8](08-systemverilog.md) |
| Testbench | Simulation environment that supplies inputs and observes or checks behavior. | [8](08-systemverilog.md) |
| VCD | Value Change Dump: a waveform-file format recording signal changes over simulation time. | [8](08-systemverilog.md) |
