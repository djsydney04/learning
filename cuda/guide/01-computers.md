# 1. Bits, instructions, operands, and memory

[← Start](00-start.md) · [Next: C++ →](02-cpp.md)

**Build today:** a mental model for what `c = a + b` asks a computer to do. You need ordinary arithmetic, not electronics knowledge.

## A bit is a distinction

A **bit** stores one of two values, written `0` and `1`. Hardware represents them using physical states such as voltage ranges. Eight bits make one **byte**. We use patterns of bits to represent numbers, instructions, text, and addresses.

For an unsigned binary number, positions have weights 1, 2, 4, 8, and so on, moving right to left:

```text
bits:       0  1  0  1
weights:    8  4  2  1
value:      0 +4 +0 +1 = 5
```

An unsigned byte represents integers from 0 through 255. The bits do not identify their own meaning: `01000001` can represent the number 65 or, under a character encoding, the letter `A`. A program's types and instructions provide the interpretation.

## Storage and calculation are different jobs

**Memory** stores bytes. An **address** identifies a location. Think of a long row of numbered byte slots. On the ordinary byte-addressed systems used here, consecutive addresses differ by one byte.

A **processor** executes instructions. It has arithmetic units for operations such as addition, a way to fetch and decode instructions, and small working storage called **registers**. CPUs also have caches, which keep recently useful data closer to execution units than main memory.

A simplified addition looks like this:

```text
memory                 registers             work
a = 3  -- load ------> r0 = 3
b = 4  -- load ------> r1 = 4
                       r2 = r0 + r1   <------- add
c = 7  <-- store ---- r2 = 7
```

A **load** reads from memory into a register. A **store** writes a value to memory. The addition and the movement of the inputs are separate operations. Real compilers can combine, reorder, or remove operations while preserving required program behavior; this diagram explains the dependencies, not an exact instruction listing for every CPU.

## Operation and operands

An **operation** says what to do. An **operand** is one of the values it works on.

```text
3 + 4
│ │ │
│ │ └── operand: 4
│ └──── operation: addition
└────── operand: 3
```

In `x + 4`, the operands are the current value of `x` and the fixed number `4`. The written number is a **literal constant**. The variable `x` can hold different values; the literal `4` always means four.

At the instruction level, an **immediate operand** is a constant encoded in the instruction itself. Compare this illustrative assembly notation:

```text
ADD r0, r1, #4       r0 receives the value in r1 plus the number 4
ADD r0, r1, r2       r0 receives the value in r1 plus the value in r2
LOAD r0, [r1]       r0 receives a value read from the address stored in r1
```

`#4` means the number four in this example notation. `[r1]` means memory at an address. Exact syntax varies across instruction sets. A constant number and a memory address that happens to be constant are different: reading address 100 does not necessarily produce the number 100.

In C++, `const int n = 4;` means the program cannot assign a new value to `n` through that declaration. It does **not** promise that the machine code uses an immediate instruction. The compiler chooses the representation. Also keep this separate from CUDA's `__constant__` memory space, introduced in [memory](07-memory.md).

## A program is instructions plus data

Your C++ source is text for people and the compiler. The compiled executable contains machine instructions and other information the operating system uses to load and run it. A CPU executes the host program; in CUDA, that host program can request work from a GPU.

The CPU does not directly “understand” a C++ loop. The compiler lowers it into instructions for updating values, comparing a loop index with a bound, and deciding what to execute next. A compiler may also vectorize the loop, handling multiple elements with one machine instruction.

The earlier [tiny CPU guide](../../verilong/cpu/intro.md) goes deeper into how registers, arithmetic circuits, and control logic carry out instructions. You do not need to complete it before proceeding here.

## Integers and floating-point numbers

An **integer** represents a whole number. A **floating-point** format represents numbers using a sign, a significand, and a scale resembling scientific notation. With finite bits, it has finite range and precision. Many fractions, including 0.1, cannot be represented exactly in binary floating point.

Our numerical arrays use C++ `float`, the 32-bit floating-point type on the CUDA systems in this guide. A million floats occupy 4,000,000 bytes before any surrounding bookkeeping. `sizeof(float)` lets a program ask how many bytes one element occupies.

Rounding means two different orders of addition can give slightly different answers. A GPU reduction rearranges additions, so we normally compare with a tolerance:

```text
absolute difference <= absolute tolerance + relative tolerance × |reference|
```

Absolute tolerance helps near zero; relative tolerance scales with the expected value. Tolerance is chosen for a calculation's precision, magnitude, and accumulated error. It is not a way to excuse incorrect indexing. NaN and unexpected infinity should fail these checks.

<details>
<summary>Optional review</summary>

1. Decode binary `1010`.
2. In `y = alpha * x + 2`, identify the inputs of multiplication and addition.
3. If a float array begins at byte address 1000 and each float occupies 4 bytes, where does element 3 begin? Arrays count from zero.
4. Explain why “load the number 4” and “load the number at address 4” are different.

<details>
<summary>Answers</summary>

1. `8 + 2 = 10`.
2. Multiply `alpha` by `x`; add that product to constant `2`. Assignment stores the result in `y`.
3. `1000 + 3 × 4 = 1012`. Element 0 begins at 1000.
4. The first supplies four itself. The second reads bytes whose contents can change.

</details>

Explain an addition using the words operand, load, register, and store. Then explain what changes if one operand is an immediate constant.

</details>
