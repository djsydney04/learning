# How a processor works

A processor does one thing. It reads a number from memory, treats that number
as an instruction, carries it out, and moves on to the next one. Everything a
computer does, from a calculator to a web browser, is that loop running
billions of times a second.

This guide builds up that loop from the basics, then shows how Tiny8, the CPU
in this folder, implements it. Read it before `README.md`, which covers what
you will write.

---

## 1. Where this sits

![Layers of a computer, from software down to transistors](docs/img/01_layers.png)

A computer is built in layers. Each layer hides the details of the one below.

- **Software** is what most programmers write. A compiler turns it into
instructions.
- The **instruction set architecture (ISA)** is the contract between software
and hardware. It says which bytes mean which operation. In Tiny8, the bytes
`02 04` mean "add 4 to the accumulator, called A."
- The **microarchitecture** is the hardware that keeps that contract: the
registers, the adder, and the logic that steps through instructions. You
describe it in SystemVerilog, at what is called the register-transfer level
(RTL).
- A **synthesis** tool turns RTL into **logic gates and flip-flops**, which are
made of **transistors**.

This project lives in the highlighted layer. You pick the instruction set (it
is in `src/cpu_pkg.sv`), then build the hardware that carries it out.

---

## 2. The parts of a computer

![CPU with control unit, registers, and ALU, connected to memory by address, data, and write signals](docs/img/02_computer.png)

Nearly every processor has the same three parts inside.

**Registers** are a few tiny, fast storage slots inside the CPU. Tiny8 has
three that matter:


| Name   | Stands for           | What it holds                                                                                                                                                                              |
| ------ | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **PC** | program counter      | The address of the next byte to read. After a read it usually becomes the next address, one higher. A jump replaces it with some other address, which is how the CPU skips ahead or loops. |
| **IR** | instruction register | The opcode, the byte that names the instruction, being carried out right now.                                                                                                              |
| **A**  | accumulator          | The one number the CPU is working on. Loads put a value here, adds change it, and stores copy it out to memory.                                                                            |


The **ALU** (arithmetic logic unit) does the math: add, subtract, AND, OR. It
takes inputs from registers and hands back a result.

The **control unit** is the conductor. It looks at the current instruction
and, on each clock, decides which registers load a new value, which operation
the ALU does, and whether memory is read or written.

Outside the CPU is **memory**, a long row of numbered slots. A **byte** is one
slot: 8 bits, so a number from 0 to 255. An **address** is the number of a
slot, starting at 0. The CPU talks to memory over three sets of wires. The
**address** says which byte. The **data** carries the byte in or out. **Write**
says whether this is a store.

Real computers also have input and output devices, like a keyboard or a
screen. Tiny8 has none. The testbench looks into memory instead.

---

## 3. Instructions are just numbers

![Memory as a column of bytes, showing opcodes, operands, and data](docs/img/03_instruction_encoding.png)

Memory holds nothing but bytes. A byte becomes an instruction only because PC
points at it and the CPU reads it as one.

A Tiny8 instruction is one or two bytes:

- The first byte is the **opcode**, short for operation code. It is a number
that names the instruction. The CPU never sees the letters `LDA` or `ADD`.
It sees `01` or `02` and treats that number as the operation.
- The second byte, if there is one, is the **operand**. Depending on the opcode
it is either a constant (`#nn`) or an address (`$80`) that points at another
byte in memory.


| Opcode | Name       | What it does                                                     |
| ------ | ---------- | ---------------------------------------------------------------- |
| `00`   | `NOP`      | Do nothing, then fetch the next instruction.                     |
| `01`   | `LDA #nn`  | Load the accumulator: `A` becomes the constant in the next byte. |
| `02`   | `ADD #nn`  | Add the next byte to `A`.                                        |
| `03`   | `SUB #nn`  | Subtract the next byte from `A`.                                 |
| `04`   | `AND #nn`  | Bitwise AND of `A` and the next byte.                            |
| `05`   | `OR #nn`   | Bitwise OR of `A` and the next byte.                             |
| `06`   | `STA addr` | Store `A` into memory at the address in the next byte.           |
| `07`   | `LDA addr` | Load `A` from memory at the address in the next byte.            |
| `08`   | `JMP addr` | Jump: set PC to the address in the next byte.                    |
| `09`   | `JZ addr`  | Jump to that address only if the zero flag is set.               |
| `0A`   | `HLT`      | Halt. The CPU stays stopped.                                     |


`#nn` means the operand is a constant, also called an **immediate**. `addr`
means the operand is a memory address. `LDA` is "load accumulator," `STA` is
"store accumulator," `JMP` is "jump," `JZ` is "jump if zero," and `HLT` is
"halt." `NOP` is "no operation." **AND** and **OR** work bit by bit: each bit
of A is combined with the matching bit of the operand, and the other bits are
left alone.

The **zero flag (Z)** is a single bit that turns on when the last value written
into A was 0, and off otherwise. `JZ` reads that bit to decide whether to jump.

Programs and data share the same memory. This is called the stored-program, or
von Neumann, design, and nearly every computer uses it. It also means that if
PC ever wanders into your data, the CPU will happily try to run it.

---

## 4. The fetch–decode–execute cycle

![Fetch, decode, and execute arranged in a loop](docs/img/04_fetch_decode_execute.png)

This is the loop every processor runs.

1. **Fetch.** Put PC on the address wires, read the byte that comes back, and
  store it in IR. Add 1 to PC so it points at the next byte.
2. **Decode.** Look at the opcode in IR and work out what it needs. Another
  byte? The ALU? A memory write? A jump?
3. **Execute.** Do it. Put a result in A, write A to memory, or load a new
  value into PC.

Then go back to fetch. PC already moved forward, so the next fetch picks up
the next instruction. A jump is nothing more than writing a new value into
PC, so the next fetch happens somewhere else.

---

## 5. The clock

![Clock waveform with a combinational signal and a register sampling it on rising edges](docs/img/06_clock.png)

Every wire in this CPU is either 0 or 1. Most wires change only because some
other wire changed. **clk** is a wire with a different job. It flips on a
steady beat, 0 then 1 then 0 then 1, whether or not the CPU is busy. That beat
is the **clock**.

Drawn against time, it is a square wave. Time moves to the right.

```
clk    ___     ___     ___
    __|   |___|   |___|   |___
       ^       ^       ^
     rises   rises   rises
```

An **edge** is one corner of that wave: the instant the wire changes value.

- A **rising edge** is the corner that goes up. The wire was 0 and becomes 1.
  Those are the upward lines in the picture. SystemVerilog calls this
  `posedge`, short for positive edge.
- A **falling edge** is the corner that goes down. The wire was 1 and becomes
  0. Tiny8 ignores falling edges. Its registers change only on a rise.

You do not check the clock the way a program checks a variable. A flip-flop
is built to notice the rise by itself. At that instant it copies its input.
Until the next rise it holds that copy and ignores the input, even if the
input keeps changing.

In simulation, nothing physical is ticking. The testbench in `tb/cpu_tb.sv`
is what flips the wire:

```systemverilog
initial clk = 0;
always #5 clk = ~clk;
```

`clk` starts at 0. `#5` means "wait 5 nanoseconds." `~clk` turns 0 into 1, or
1 into 0. So the wire flips every 5 ns. The first flip is a rise (0 to 1).
The next is a fall (1 to 0). A rise comes every 10 ns.

`@(posedge clk)` means "wait until that rise." The testbench prints one line,
then does exactly that:

```systemverilog
@(posedge clk);
```

Each line of `make sim` is one rising edge. Open `waves/tiny8.vcd` and `clk`
is the square wave. Each upward corner is a rise.

In the diagram, `alu_result` is not a register. It changes whenever its inputs
change: 5, then 9, then 4, then 6. `acc` is a register. On each rise it copies
whatever `alu_result` is at that instant, then holds it. The 9 showed up and
went away between two rises, so `acc` never stored it.

That is why a clock exists. The gates can wiggle and then settle between
rises, and only the settled value gets stored.

The gap between rises is also the CPU's speed. It has to be long enough for
the slowest chain of gates to finish, or a register would store a
half-finished result. A 3 GHz processor is one whose slowest path settles in
under a third of a nanosecond.

---

## 6. Two kinds of hardware

![Combinational logic next to a clocked register, and the pc <= pc + 1 feedback loop](docs/img/05_comb_vs_seq.png)

The clock only matters for one of the two kinds of circuit. SystemVerilog has
a different spelling for each. None of these is a function you call. Each one
is hardware that is present the whole time the chip is on.

### `assign` — a wire that is always equal to something

```systemverilog
assign sum = a + b;
```

There is a wire named `sum`, tied to an adder. When `a` or `b` changes, `sum`
changes with it, in that same moment. This line does not run later. It is a
connection. The `=` means "this wire is," not "set this variable when we get
here."

### `always_comb` — the same kind of circuit, when you need `if` or `case`

```systemverilog
always_comb begin
  sum = a + b;
end
```

**always** means the block is active the whole time. **comb** means
combinational: gates, and no memory. The output depends only on the inputs
right now. Change an input and the output follows. There is no `clk` here.

`assign` and `always_comb` build the same kind of hardware. Use `assign` for
one connection. Use `always_comb` when the connection needs `if` or `case`,
the way the decoder looks at an opcode and decides what it is. The ALU, the
decoder, and the muxes are this kind. Inside the block, `=` still means "this
wire is."

### `always_ff` — a register that stores a value when the clock rises

```systemverilog
always_ff @(posedge clk) begin
  pc <= pc + 1;
end
```

**ff** means flip-flop, the cell that remembers one value. `@(posedge clk)`
means "pay attention only when `clk` rises."

Between rises, `pc` stays what it was. On a rise, it stores the new value.
The `<=` is not "less than or equal." Inside `always_ff` it means "on this
rise, store this." Every `<=` in the block stores on that same rise, and each
one uses the values from before the rise. The CPU does not update halfway.

Read `pc <= pc + 1` as a picture, not as a later line of code. A register
named PC has a +1 adder sitting on its input. The adder is always adding.
The register listens only when `clk` rises, so PC goes up by one per rise.

| | Combinational | Sequential |
| --- | --- | --- |
| SystemVerilog | `assign`, `always_comb` | `always_ff @(posedge clk)` |
| Memory | none | holds a value until the next rise |
| When it changes | as soon as an input changes | only when `clk` goes from 0 to 1 |
| In Tiny8 | ALU, decoder, muxes | PC, IR, A, Z, the FSM state |

Most of a CPU is that pairing repeated. Combinational logic computes the next
value, and a register stores it on the next rise.

---

## 7. Datapath and control: Tiny8 up close

![Tiny8 datapath with PC, memory, IR, decoder, operand, ALU, A, Z, muxes, and control signals](docs/img/07_tiny8_datapath.png)

A CPU design splits into two halves.

- The **datapath** is where numbers flow: registers, the ALU, memory, and the
wires between them.
- The **control** is the FSM at the top. It never touches the numbers. Each
clock it sets the orange signals: which input each mux passes through, which
registers load, and whether memory writes.

Things to trace in the picture:

- **Muxes** (the trapezoids) are switches that pick one of several inputs. The
address mux picks PC while reading the program, or the operand when an
instruction reads or writes data. The A mux picks whether A gets the
operand, the ALU result, or a byte loaded from memory.
- Memory's `rdata` (the byte just read) goes to three places: IR during fetch,
the operand register during the operand step, and A during a load. The
control signals decide which one actually stores it.
- The operand also goes several places: the ALU, the A mux, the address mux
(for `STA` and `LDA addr`), and PC as a jump target.
- A feeds the ALU and memory's `wdata` (the byte to write). That is how `STA`
stores it.
- Z remembers whether the last value written into A was zero. The FSM reads it
to decide whether `JZ` jumps.

Where each block lives:


| Block                                 | File             | Kind                        |
| ------------------------------------- | ---------------- | --------------------------- |
| PC                                    | `src/pc.sv`      | register                    |
| Memory                                | `src/memory.sv`  | memory                      |
| Decoder                               | `src/decoder.sv` | combinational               |
| ALU                                   | `src/alu.sv`     | combinational               |
| IR, operand, A, Z, muxes, control FSM | `src/cpu.sv`     | registers and combinational |
| CPU wired to memory                   | `src/tiny8.sv`   | wiring only                 |


---

## 8. The control FSM

![Tiny8 state machine with FETCH, DECODE, OPERAND, EXECUTE, LOAD, and HALT](docs/img/08_tiny8_fsm.png)

A **finite state machine** (FSM) is a register that holds "which step am I
on," plus combinational logic that picks the next step. Tiny8's FSM has six
states, and each one lasts one clock.

- **FETCH** loads the opcode into IR and moves PC forward.
- **DECODE** looks at the opcode. `HLT` goes to HALT. An instruction with a
second byte goes to OPERAND. `NOP` goes straight to EXECUTE.
- **OPERAND** loads the second byte and moves PC forward again.
- **EXECUTE** does the work, then usually goes back to FETCH.
- **LOAD** is an extra clock used only by `LDA addr`. EXECUTE points the
address at the operand, and LOAD copies the byte that comes back into A.
With Tiny8's simple memory you could squeeze both into EXECUTE. Keeping them
apart gives each state one job.
- **HALT** stays put forever. The testbench watches for it to know the program
finished.

---

## 9. One instruction, clock by clock

![ADD #nn traced across FETCH, DECODE, OPERAND, and EXECUTE](docs/img/09_one_instruction.png)

This traces one `ADD #nn` stored at addresses n and n + 1. It takes four
clocks.

Nothing gets stored in the middle of a column. Everything in the bottom row
happens at the rising edge that ends that column, all at once. Read the
columns left to right and you are watching the FSM, the address mux, memory,
and the registers work together. When `make sim` prints its cycle-by-cycle
trace, this is what it is showing you.

---

## 10. How real CPUs go faster

Tiny8 is a multi-cycle design: one instruction at a time, several clocks each.
Real processors keep the same fetch–decode–execute idea and add tricks on top.

- **Pipelining** overlaps instructions. While one executes, the next is
decoding and the one after that is being fetched, like an assembly line.
- **More registers.** A register file with 16 or 32 registers means far fewer
trips to memory than a single accumulator.
- **Caches** are small, fast memories next to the CPU that keep recently used
bytes close, because main memory is slow.
- **Branch prediction** guesses which way a jump will go, so the pipeline does
not have to stop and wait.
- **Superscalar and out-of-order execution** run several instructions per
clock and reorder them when they do not depend on each other.

Every one of these is a change to the microarchitecture. The ISA, and the
software written for it, can stay the same.

---

## Words you will see


| Term                    | Meaning                                                                                                                 |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **CPU**                 | The processor. It fetches instructions and carries them out.                                                            |
| **Memory**              | A long row of bytes, shared by the program and its data.                                                                |
| **Byte**                | One memory slot. 8 bits, a number from 0 to 255.                                                                        |
| **Address**             | The number of a byte in memory. Address 0 is the first byte.                                                            |
| **PC**                  | Program counter. The address of the next byte to fetch.                                                                 |
| **IR**                  | Instruction register. Holds the opcode being carried out.                                                               |
| **A**                   | Accumulator. Tiny8's one working number.                                                                                |
| **Z**                   | Zero flag. On when the last value written into A was 0.                                                                 |
| **ALU**                 | Arithmetic logic unit. Adds, subtracts, ANDs, and ORs.                                                                  |
| **Opcode**              | Operation code. The first byte of an instruction: a number that says what to do, such as `01` for load or `02` for add. |
| **Operand**             | The optional second byte: a constant (`#nn`) or an address.                                                             |
| **Immediate**           | An operand that is the number itself, not an address.                                                                   |
| **clk**                 | The clock wire. It flips 0, 1, 0, 1 on a steady beat. Registers update only when it goes from 0 to 1.                   |
| **Edge**                | The instant a wire changes. A rising edge is 0 to 1. A falling edge is 1 to 0.                                          |
| **Rising edge**         | The upward corner of the clock, when `clk` goes from 0 to 1. Also called `posedge`.                                     |
| **assign**              | One wire, always equal to an expression. No clock and no memory. `assign sum = a + b` ties `sum` to an adder.           |
| **always_comb**         | Combinational logic as a block: always active, no clock. Same kind of hardware as `assign`, used when you need `if`.    |
| **always_ff**           | A register. `always_ff @(posedge clk)` stores a new value only on a rising edge. `<=` inside it means "store this."     |
| **Register**            | A group of flip-flops that holds a value between clocks.                                                                |
| **Flip-flop**           | A one-bit memory cell that updates on the rising edge.                                                                  |
| **Combinational logic** | Gates with no memory. The output follows the inputs immediately.                                                        |
| **Sequential logic**    | Flip-flops. The output changes only on a clock edge.                                                                    |
| **Mux**                 | Multiplexer. A switch that passes one of several inputs through.                                                        |
| **Bus**                 | A group of wires that carries one value, such as an 8-bit address.                                                      |
| **Datapath**            | The registers, ALU, memory, and wires that the numbers flow through.                                                    |
| **Control unit**        | The logic that, each clock, decides what the datapath should do.                                                        |
| **FSM**                 | Finite state machine. A register that holds the current step, plus logic that picks the next one.                       |
| **ISA**                 | Instruction set architecture. The list of opcodes and what each one must do.                                            |
| **RTL**                 | Register-transfer level. Hardware described as registers and the logic between them.                                    |
| **Synthesis**           | Turning RTL into gates for an FPGA or a chip.                                                                           |
| **Testbench**           | Simulation-only code that drives the design and checks the result.                                                      |


---

## Next

Open [walkthrough.md](walkthrough.md) next. It follows one `ADD #4` through
every rise of the clock, with the value in PC, IR, and A after each one.
[README.md](README.md) is the file-by-file plan for when that story is clear.

The diagrams are drawn by [utils/make_diagrams.py](../../utils/make_diagrams.py)
at the repo root. If you change the design, you can edit that script and redraw them.