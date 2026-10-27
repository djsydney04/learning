#!/usr/bin/env python3
"""Truth tables and a ripple adder, using only Python's standard library.

This is a mathematical model of two-state logic. It does not simulate the
SystemVerilog exercises, propagation delays, unknown values, or electricity.
"""


def full_adder(a, b, carry_in):
    """Return (sum bit, carry out) for three one-bit inputs."""
    if any(bit not in (0, 1) for bit in (a, b, carry_in)):
        raise ValueError("full_adder inputs must be 0 or 1")
    partial_sum = a ^ b
    return partial_sum ^ carry_in, (a & b) | (partial_sum & carry_in)


def ripple_add(a, b, width=8):
    """Connect full adders from bit 0 upward; return (low bits, final carry)."""
    if not isinstance(width, int) or width < 1:
        raise ValueError("width must be a positive integer")
    if not (0 <= a < 1 << width and 0 <= b < 1 << width):
        raise ValueError("inputs must fit the requested unsigned width")
    result = 0
    carry = 0
    for position in range(width):
        bit, carry = full_adder((a >> position) & 1, (b >> position) & 1, carry)
        result |= bit << position
    return result, carry


def main():
    print("Two-state logic model; no SystemVerilog or physical timing is simulated.\n")
    print("a b | AND OR XOR NAND")
    for a in (0, 1):
        for b in (0, 1):
            print(f"{a} {b} |  {a & b}   {a | b}   {a ^ b}    {1 - (a & b)}")

    a, b = 250, 10
    print(f"\nEight full adders connected by carry wires: {a} + {b}")
    print(f"a = {a:08b}; b = {b:08b}")
    print("bit | a b carry-in | sum carry-out")
    carry = 0
    for position in range(8):
        bit_a, bit_b = (a >> position) & 1, (b >> position) & 1
        bit_sum, next_carry = full_adder(bit_a, bit_b, carry)
        print(f" {position}  | {bit_a} {bit_b}    {carry}     |  {bit_sum}      {next_carry}")
        carry = next_carry
    result, carry = ripple_add(a, b)
    print(f"Stored eight-bit result: {result:08b} = {result}; carry out = {carry}")
    print("The mathematical sum is 260. Keeping eight bits gives 260 modulo 256 = 4.")
    print("Carry out detects unsigned overflow here; signed overflow is a different test.")


if __name__ == "__main__":
    main()
