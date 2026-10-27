# Practice: connect the layers

[Primer](../README.md) · [← SystemVerilog](08-systemverilog.md) · [Glossary](glossary.md)

Work these on paper before opening the answers or running a model. You do
not need to fill in the CPU's RTL to do them. The first problems build the
circuits; the later ones ask you to follow the machine those circuits form.

## 1. One pattern, two numbers

Interpret `8'hF8` as unsigned and as signed two's complement. Add `8'h0C`
and keep eight result bits. State the stored result, carry, and signed
overflow. Explain why the two interpretations can use the same adder.

<details>
<summary>Answer</summary>

`F8` is 248 unsigned or −8 signed. `0C` is 12 under either interpretation.
The exact unsigned sum is 260, so the stored byte is `04` with carry 1.
The signed sum is −8 + 12 = 4, which fits, so there is no signed overflow.
The bit addition is identical; interpretation and overflow rules differ.

</details>

## 2. Build a selector from gates

A one-bit mux selects `a` when `s = 0` and `b` when `s = 1`.
Write an expression using only NOT, AND, and OR. Check all eight combinations
of `a`, `b`, and `s`. How would you make it eight bits wide?

<details>
<summary>Answer</summary>

`y = (~s & a) | (s & b)`. With `s = 0`, the second term is zero and the
first passes a. With `s = 1`, the first term is zero and the second passes b.

| a | b | s | y |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 0 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

Use eight copies sharing one select signal, one per bit. In SystemVerilog,
`assign y = s ? b : a;` expresses that selection directly when a, b, and y
are eight-bit vectors. A raw one-bit `~s` is not an eight-bit mask; explicitly
replicate it if writing the wide gate expression.

</details>

## 3. Trace a carry

Add four-bit `1111` and `0001` using full adders from the least significant
bit upward. Record each carry. Why does the four-bit result become zero?

<details>
<summary>Answer</summary>

Bit 0 receives 1, 1, and carry-in 0: sum 0, carry 1. Bits 1, 2, and 3
each receive 1, 0, and carry-in 1: sum 0, carry 1. The full answer is
five-bit `10000`; discarding the final carry leaves `0000`. Zero does not
mean that the exact mathematical sum was zero.

Compare with [the gate-based adder](../experiments/01_logic.py).

</details>

## 4. Pause a pipeline

Two registers update with `first <= input_value; second <= first;` when
enabled, and hold otherwise. Initially both are zero. The next four edges
have input/enable pairs `(6,1)`, `(10,1)`, `(99,0)`, `(2,1)`. Give both
stored values after each edge. Does changing input to 88 between edges
change either stored value?

<details>
<summary>Answer</summary>

After the edges: `(6,0)`, `(10,6)`, `(10,6)`, `(2,10)`.
The disabled edge holds both registers. A change to input between edges
does not itself update them. See [the clock model](../experiments/02_clock.py)
and [RTL example](../experiments/04_pipeline.sv).

</details>

## 5. Check both timing constraints

Assume zero clock skew. A path has maximum clock-to-Q 0.12 ns, maximum
logic delay 0.58 ns, and setup time 0.10 ns. It has minimum clock-to-Q
0.03 ns, minimum logic delay 0.02 ns, and hold time 0.08 ns. Does a 1 ns
period meet the simplified setup and hold checks? Would a 2 ns period
resolve both?

<details>
<summary>Answer</summary>

Setup needs at least `0.12 + 0.58 + 0.10 = 0.80 ns`, so the 1 ns period
passes that simplified check. Hold needs earliest new data at least 0.08 ns
after the edge, but it arrives in `0.03 + 0.02 = 0.05 ns`. Hold fails.
Increasing the period to 2 ns does not change this same-edge minimum-delay
problem. A physical implementation needs a timing fix and analysis with
the actual clock, device, and routing conditions.

</details>

## 6. Address width is not data width

A memory has a 10-bit address and an 8-bit data port. How many byte locations
does it select, and how many bits can it store? If address 7 contains 200,
which number goes on the address bus for a read of that location? Compare
this with Tiny8's memory.

<details>
<summary>Answer</summary>

It selects `2^10 = 1,024` byte locations and stores `1,024 × 8 = 8,192`
bits. Address 7 goes on the address bus; the read data is 200 after the
memory's specified access timing. Tiny8 has eight address bits, selecting
256 byte locations for 2,048 bits total. An address value does not have to
equal the data it selects.

</details>

## 7. Load, add, and store

Tiny8 starts after reset. Memory at hex address `80` contains decimal 41.
At address zero, the program bytes in hex are:

```text
07 80 02 01 06 80 0A
```

Decode the instructions. Give final A, Z, memory[`80`], PC, and active edge
count to reach HALT. At which edge does A first become 41?

<details>
<summary>Answer</summary>

`LDA $80; ADD #1; STA $80; HLT`. A ends at 42, Z at 0, memory[`80`] at 42,
PC at hex `07`. Absolute load takes 5 edges, add 4, store 4, and halt 2,
for 15 edges after reset. A first becomes 41 at edge 5, the load's LOAD
capture edge. The following memory location is not read as another opcode
until that instruction finishes.

Check from the repository root:

```sh
python3 cpu-architecture/experiments/03_tiny8.py --demo load
```

</details>

## 8. Follow a counted loop

Decode this Tiny8 program. Does it halt? What is stored at `80`?
How many times does each jump execute? Explain which operation changes Z.

| Address, hex | Bytes, hex |
| --- | --- |
| `00` | `01 03` |
| `02` | `03 01` |
| `04` | `09 08` |
| `06` | `08 02` |
| `08` | `06 80` |
| `0A` | `0A` |

<details>
<summary>Answer</summary>

The program loads 3, repeatedly subtracts 1, jumps to the store when Z is
set, and otherwise jumps back to subtract. The subtract executes three
times, producing 2, 1, and 0. `JZ` executes three times and is taken only
the third time. `JMP` executes twice. Store writes zero, then HLT stops.
The initial load clears Z; the last subtraction sets it. Neither jump nor
the store changes Z. Total active edges are
`4 + 3×4 + 3×4 + 2×4 + 4 + 2 = 42`.

Check with `python3 cpu-architecture/experiments/03_tiny8.py --demo countdown`
from the repository root.

</details>

## 9. Avoid a misleading benchmark

Two cores run the same program with two million executed instructions.
Core A runs at 1 GHz with average CPI 1.5. Core B runs at 2 GHz with average
CPI 4. Calculate each execution time. Separately, a cache has a 2 ns lookup,
10% miss rate, and 40 ns additional miss penalty. Calculate its simple
average access time. Can you substitute that number directly for CPI?

<details>
<summary>Answer</summary>

Core A: `2,000,000 × 1.5 / 1,000,000,000 = 3 ms`.
Core B: `2,000,000 × 4 / 2,000,000,000 = 4 ms`.
The cache average is `2 + 0.10 × 40 = 6 ns` under the serial-access model.
It is time per memory access, not cycles per instruction. Instructions
make different numbers of accesses, and a processor can overlap some
memory work. The quantities have different units and meanings.

</details>

## 10. Plan a useful CPU check

Someone says, “The simulation printed lots of activity and reached `$finish`,
so the CPU works.” What would you check for the program in chapter 6?
Name an input that would expose replacing bitwise OR with logical OR.
Would those checks prove the CPU can run at a particular clock frequency?

<details>
<summary>Answer</summary>

Require the expected final A = 9, memory[`80`] = 9, PC = `07`, and HALT
within a bounded edge count. To check the intended controller sequence,
compare its intermediate edge trace as well. A printed trace or `$finish`
alone does not assert any of those facts.

For OR, combine `80` with `01`: the expected result is `81`, while logical
OR yields a single 1 that would widen to `01`. Include zero and boundary
values, taken and untaken branches, reset behavior, and memory operations
when you expand the checks. These verify selected functional behavior;
they neither prove all inputs correct nor establish physical timing.

</details>

When these answers feel explainable, continue to the
[Tiny8 implementation guide](../../verilong/cpu/README.md).
