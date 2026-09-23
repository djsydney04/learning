# Tiny8 — you write the microprocessor

The files are a skeleton. Ports, types, and comments are here. The behavior
is yours.

New to how processors work? Read [`intro.md`](intro.md) first. It explains
the fetch–decode–execute loop, the clock, and Tiny8's datapath with diagrams.

---

## What this actually is

Yes. This is designing a CPU at a low level.

You are not writing a program that *runs on* a processor. You are describing
the processor itself: the registers, the adder, the wires to memory, and the
little state machine that fetches the next instruction.


Three layers people mix up:

| Layer | What it is | Example |
| --- | --- | --- |
| Software | Instructions a CPU already understands | `A = A + 4` in C, or bytes `02 04` in RAM |
| This project (RTL) | The hardware that *makes those instructions mean something* | flip-flops for A and PC, an ALU, a fetch/decode/execute FSM |
| Transistors / gates | What an FPGA or chip turns your RTL into | AND gates, adders, D flip-flops |

**RTL** means Register Transfer Level. You say things like “on the rising
clock, copy memory data into IR and add 1 to PC.” A simulator (and later a
synthesis tool) turns that into hardware.

A laptop CPU is the same idea, scaled up: more registers, a pipeline, caches,
out-of-order execution. Tiny8 is the same loop those chips still do, stripped
to the bones.

```
software you will write     →  bytes sitting in RAM
                                    ↓
you are building this       →  CPU that reads those bytes and does work
                                    ↓
the chip tools build this   →  gates and flip-flops
```

SystemVerilog looks a bit like C, but it is not a program that runs top to
bottom. It is a *description of hardware that all exists at once*.

Think of a printed circuit board, not a recipe. When you power the board,
the adder is adding, the decoder is decoding, and the RAM is sitting there
with voltages on its pins — **at the same time**. The source file does not
mean “first do the ALU, then do the decoder.” It means “here is an ALU
*and* here is a decoder, both soldered down.”

Nothing takes turns unless you *build* turn-taking. That is what the
FETCH / DECODE / EXECUTE state machine is: extra flip-flops whose value
says “this clock I am fetching, next clock I am decoding.”

### `always_comb` — gates, always live, no clock

Combinational logic has **no memory**. It is just wires and gates.

```
always_comb begin
  result = a + b;
end
```

The moment `a` or `b` changes, `result` changes. There is no “wait for the
clock.” There is no stored old value. If you froze time and poked `a`,
`result` would already be the new sum.

In this CPU, that is:

- the ALU (`a + b`, `a & b`, …)
- the decoder (looking at the opcode and lighting up flags)
- the memory-address mux (“should the bus show PC, or the operand?”)

A light with a switch is combinational: the switch position *is* the
output. Let go of the idea of “running this line.” The gates are just
there.

### `always_ff @(posedge clk)` — flip-flops, update on the clock

Sequential logic **remembers**. A flip-flop holds a number until you tell
it to take a new one. The “tell it” moment is the rising edge of `clk`.

```
always_ff @(posedge clk) begin
  acc <= alu_result;
end
```

Between clock edges, `acc` does not care that `alu_result` is wiggling.
On the edge, it samples `alu_result` and holds that snapshot.

In this CPU, that is A, PC, IR, the FSM state, and RAM writes. Those are
the machine’s memory of “who I am right now.”

`posedge clk` means “only when the clock goes 0 → 1.” That is the heartbeat.
One heartbeat = one small step of the CPU.

`<=` is a **non-blocking** assignment. Read it as: “schedule this update
for the end of the clock edge.” Every `<=` in the block uses the *old*
values, then they all change together. So this is safe and normal:

```
always_ff @(posedge clk) begin
  ir    <= mem_rdata;   // both use the values from BEFORE this edge
  state <= S_DECODE;
end
```

IR and state update as a pair. You do not get a half-updated CPU.

### `pc <= pc + 1` is a circuit, not a later line of code

In C, `pc = pc + 1` means “when the CPU reaches this line, add one.”

In `always_ff`, the same-looking text means you **drew this**:

```
          +---+
   pc --- | +1| ----+
          +---+     |
                    |   at posedge clk
                    v
                 [ PC register ]
                    |
                    +---- pc (the 8 wires coming out)
```

There is a register named PC. Sitting on its input is a little incrementer
(combinational +1). Every rising clock, PC eats whatever is on that input
and becomes “old PC + 1.”

The incrementer is always adding. The register only *listens* on the clock
edge. That pairing — combinational cloud into a flip-flop — is most of
digital design. The whole CPU is that idea repeated: ALU (comb) into A
(ff), decoder (comb) into the next-state mux into `state` (ff), address
mux (comb) into RAM, and so on.

---

## How SystemVerilog works

SystemVerilog (SV) is a **hardware description language**. You are drawing a
circuit with text. The file does not “run.” It *is* the chip.

### It is not C

In C, lines happen one after another:

```
x = 1;
x = x + 1;   // later, x becomes 2
```

In SystemVerilog, most blocks are **always on**, in parallel, like chips on a
board. The ALU is adding at the same time the decoder is looking at the
opcode and the memory is sitting there with data on its pins. Nothing waits
its turn unless you *build* a state machine that takes turns (that is the
FETCH / DECODE / EXECUTE FSM).

### The only two kinds of hardware you will write

**Combinational** — `always_comb` or `assign`

Wires and gates. No memory. Change the inputs, the output changes
immediately (in the same simulated instant).

```
assign zero = (result == 8'h00);
```

That is a bunch of XNOR/AND gates that light up when `result` is all zeros.

**Sequential** — `always_ff @(posedge clk)`

Flip-flops. They hold a value until the next rising clock.

```
always_ff @(posedge clk) begin
  acc <= alu_result;
end
```

That is a register named `acc`. The `<=` is a **non-blocking** assignment:
“when this clock edge finishes, acc becomes whatever alu_result is now.”
Every `<=` in that block updates together. That is why a whole CPU can step
once per clock.

If you use `=` inside `always_ff` you are usually doing it wrong for
hardware. Use `<=` for registers, `=` inside `always_comb`.

### Modules are chips, ports are pins

```
module alu (
  input  logic [7:0] a,
  input  logic [7:0] b,
  output logic [7:0] result
);
```

A **module** is a box. **Ports** are the wires sticking out of it. You
**instantiate** a module to solder it onto a larger box (`cpu` instantiates
`alu`, `tiny8` instantiates `cpu` and `memory`).

`logic [7:0]` is an 8-bit bus — eight wires side by side.

### Two different uses of the same language

| Kind of file | Synthesizable? | Job |
| --- | --- | --- |
| `src/*.sv` | Yes (the real hardware) | What would become gates on an FPGA or ASIC |
| `tb/*.sv` | No | Fake lab bench: clock, reset, poke RAM, print, `$finish` |

`initial`, `#5`, `$display`, `$finish` are simulation-only. They do not turn
into silicon. `always_ff` / `always_comb` in `src/` do.

### What `make sim` is doing

Icarus Verilog does **not** burn a chip. It *pretends* time is passing:

1. Build a giant pile of wires and flip-flops from your modules
2. Toggle `clk` every 5 ns (the testbench does that)
3. Each rising edge, sequential blocks update
4. Combinational blocks settle
5. Print PC, A, state so you can see the machine walk

Later, a **synthesis** tool (not this project yet) would turn the same
`src/` files into a bitstream for an FPGA. Same description, two uses:
simulate to see if the circuit is right, synthesize to make a physical one.

### The picture

```
you type SystemVerilog
        ↓
   RTL description     ← you are here (designing the hardware)
        ↓
   simulator (make sim)     or     synthesis (FPGA / ASIC)
        ↓                              ↓
   waveforms / PASS              real gates on a chip
```

So yes: you are building a CPU by designing the actual hardware. The
language is how you draw that hardware precisely enough that a tool can
simulate it or build it.

---

## How a CPU works (the only loop that matters)

A clocked machine that repeats:

1. **Fetch** the next instruction byte from memory
2. **Decode** what that byte means
3. **Execute** it

Tiny8 is an **accumulator** machine. One general-purpose register, **A**.
Almost every instruction reads or writes A.

| Name | What it is |
| --- | --- |
| **A** | The accumulator. Your only GP register. |
| **PC** | Program counter. Address of the next byte to fetch. |
| **IR** | Instruction register. The opcode you just fetched. |
| **Z** | Zero flag. 1 if the last write to A produced 0. `JZ` looks at this. |
| **operand** | The second instruction byte (a constant, or an address). |

```
          +-----------+          +--------+
   PC --> |   CPU     | <------> |  RAM   |  256 bytes
          |  A, Z, IR |          | 0..255 |
          +-----------+          +--------+
                |
              ALU  (+ - & |)
```

Every clock the CPU is in **exactly one** state:

```
FETCH  →  DECODE  →  OPERAND  →  EXECUTE  →  FETCH  →  ...
                         ↓
                       HALT
```

- **FETCH** — put PC on the address bus, copy `mem[PC]` into IR, then PC += 1
- **DECODE** — look at IR. Halt? Need a second byte? Or execute now (NOP)?
- **OPERAND** — read that second byte, then PC += 1
- **EXECUTE** — do the work (load A, add, store, jump)
- **LOAD** — extra memory read, only for `LDA addr`
- **HALT** — freeze

RAM holds both the program and the data. The testbench pokes bytes into
`dut.u_mem.ram[...]`. That *is* your program. The CPU then walks those bytes.

That is a real microprocessor. It is tiny (8-bit, one register, no pipeline),
but the job is the same as a “real” CPU: turn a stream of instruction bytes
into register updates and memory reads/writes.

---

## What each file is for

Work in this order. Each file tells you what to fill in.

| Order | File | You write |
| --- | --- | --- |
| 1 | `src/alu.sv` | `result` and `zero` from `a`, `b`, `op` |
| 2 | `tb/alu_tb.sv` | a few ALU tests; run with `make sim-alu` |
| 3 | `src/memory.sv` | 256-byte array, clocked write, combinational read |
| 4 | `src/decoder.sv` | opcode → `needs_operand`, `is_alu`, `alu_op`, `is_halt` |
| 5 | `src/pc.sv` | program counter: reset, increment, load (jump) |
| 6 | `src/cpu.sv` | FSM, A / IR / operand, memory-bus mux, PC control |
| 7 | `tb/cpu_tb.sv` | your program in `load_program`, then checks |

Leave these alone unless you are adding instructions:

| File | Role |
| --- | --- |
| `src/cpu_pkg.sv` | Opcode numbers and FSM state names |
| `src/tiny8.sv` | Wires the CPU to RAM. Memory instance is `u_mem` so the testbench can do `dut.u_mem.ram[addr]` |
| `Makefile` | `make sim` and `make sim-alu` |

---

## Instruction set (the contract)

First byte = opcode. Optional second byte = constant or address.

| Byte | Name | You make this do |
| --- | --- | --- |
| `00` | `NOP` | nothing, then fetch again |
| `01` | `LDA #imm` | `A = imm` |
| `02` | `ADD #imm` | `A = A + imm` |
| `03` | `SUB #imm` | `A = A - imm` |
| `04` | `AND #imm` | `A = A & imm` |
| `05` | `OR  #imm` | `A = A \| imm` |
| `06` | `STA addr` | `mem[addr] = A` |
| `07` | `LDA addr` | `A = mem[addr]` |
| `08` | `JMP addr` | `PC = addr` |
| `09` | `JZ  addr` | if Z is set, `PC = addr` |
| `0A` | `HLT` | stay in `S_HALT` |

Those opcodes are just numbers you chose. `01` means “load A” only because
your DECODE/EXECUTE logic treats `01` that way. That is what “designing an
instruction set” is.

---

## Simulate

From this folder (`verilong/cpu`):

```bash
make sim-alu   # ALU only
make sim       # whole CPU
```

Until the CPU and a program exist, the full sim will sit in `FETCH` or never
halt. That is expected.

A waveform file lands in `waves/tiny8.vcd` if you later want GTKWave.

---

## Suggested build order

1. ALU, then `make sim-alu`.
2. Memory, decoder, program counter — each is one idea.
3. CPU reset + `FETCH` + `DECODE` + `HLT`.
4. `LDA #imm` so you can put a number in A and see it in the trace.
5. `ADD` / `SUB` through the ALU.
6. `STA`, then `JMP` / `JZ`, then `LDA addr`.
7. Write a program in `load_program` and assert the results you want.
