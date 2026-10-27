#!/usr/bin/env python3
"""Trace the intended Tiny8 FSM, one ideal rising edge at a time.

This is an independent teaching model, not a SystemVerilog simulator or a
verification of verilong/cpu/src/*.sv. The RTL exercises may still be unfinished.
Only the documented opcodes are accepted. An unknown opcode raises a model
error; this is not a definition of hardware behavior for invalid opcodes.
RAM starts at zero for reproducibility, unlike uninitialized physical RAM.
"""

import argparse
from dataclasses import dataclass


NOP, LDA_IMM, ADD_IMM, SUB_IMM, AND_IMM, OR_IMM = range(6)
STA, LDA_ABS, JMP, JZ, HLT = range(6, 11)
OPCODES = (NOP, LDA_IMM, ADD_IMM, SUB_IMM, AND_IMM, OR_IMM,
           STA, LDA_ABS, JMP, JZ, HLT)


@dataclass(frozen=True)
class Snapshot:
    """Register values after an edge, plus the memory bus BEFORE that edge."""

    cycle: int
    previous_state: str
    state: str
    pc: int
    ir: int
    operand: int
    acc: int
    z_flag: int
    mem_addr: int
    mem_rdata: int
    mem_we: bool
    mem_wdata: int


class Tiny8:
    """The specified six-state teaching CPU, with 256 byte-addressed slots."""

    def __init__(self, program=()):
        self.ram = [0] * 256
        self.load(0, program)
        self.reset()

    def load(self, address, values):
        """Place bytes in RAM before execution; loading never wraps addresses."""
        values = list(values)
        if not 0 <= address < 256 or address + len(values) > 256:
            raise ValueError("loaded bytes must fit inside the 256-byte RAM")
        if any(not isinstance(value, int) or not 0 <= value <= 255 for value in values):
            raise ValueError("RAM entries must be integer bytes")
        self.ram[address:address + len(values)] = values

    def reset(self):
        """Clear CPU registers; preserve RAM. Reset is not an instruction edge."""
        self.pc = 0
        self.ir = 0
        self.operand = 0
        self.acc = 0
        self.z_flag = 0  # This contract deliberately resets Z low even though A=0.
        self.state = "FETCH"
        self.cycles = 0

    @property
    def halted(self):
        return self.state == "HALT"

    def bus(self):
        """Return current address, asynchronous read data, write enable, write data."""
        address = self.pc
        if self.state == "LOAD" or (self.state == "EXECUTE" and self.ir in (STA, LDA_ABS)):
            address = self.operand
        write_enable = self.state == "EXECUTE" and self.ir == STA
        return address, self.ram[address], write_enable, self.acc

    def _write_accumulator(self, value):
        self.acc = value & 0xFF
        self.z_flag = int(self.acc == 0)

    def step(self):
        """Apply one rising edge. All decisions use values from before the edge."""
        previous_state = self.state
        address, read_data, write_enable, write_data = self.bus()
        if self.state == "FETCH":
            self.ir = read_data
            self.pc = (self.pc + 1) & 0xFF
            self.state = "DECODE"
        elif self.state == "DECODE":
            if self.ir not in OPCODES:
                raise ValueError(f"teaching model rejects unknown opcode 0x{self.ir:02X}")
            self.state = "HALT" if self.ir == HLT else "EXECUTE" if self.ir == NOP else "OPERAND"
        elif self.state == "OPERAND":
            self.operand = read_data
            self.pc = (self.pc + 1) & 0xFF
            self.state = "EXECUTE"
        elif self.state == "EXECUTE":
            self.state = "FETCH"
            if self.ir == LDA_IMM:
                self._write_accumulator(self.operand)
            elif self.ir == ADD_IMM:
                self._write_accumulator(self.acc + self.operand)
            elif self.ir == SUB_IMM:
                self._write_accumulator(self.acc - self.operand)
            elif self.ir == AND_IMM:
                self._write_accumulator(self.acc & self.operand)
            elif self.ir == OR_IMM:
                self._write_accumulator(self.acc | self.operand)
            elif self.ir == STA:
                self.ram[address] = write_data
            elif self.ir == LDA_ABS:
                self.state = "LOAD"
            elif self.ir == JMP or (self.ir == JZ and self.z_flag):
                self.pc = self.operand
            elif self.ir not in (NOP, JZ):
                raise ValueError(f"invalid EXECUTE opcode 0x{self.ir:02X}")
        elif self.state == "LOAD":
            self._write_accumulator(read_data)
            self.state = "FETCH"
        elif self.state != "HALT":
            raise ValueError(f"unknown model state {self.state!r}")
        self.cycles += 1
        return Snapshot(self.cycles, previous_state, self.state, self.pc, self.ir,
                        self.operand, self.acc, self.z_flag,
                        address, read_data, write_enable, write_data)

    def run(self, max_cycles=200):
        """Return all post-edge snapshots, or fail if the cycle budget expires."""
        if not isinstance(max_cycles, int) or max_cycles < 1:
            raise ValueError("max_cycles must be a positive integer")
        trace = []
        for _ in range(max_cycles):
            if self.halted:
                return trace
            trace.append(self.step())
        if not self.halted:
            raise RuntimeError(f"did not halt within {max_cycles} rising edges")
        return trace


def demo(name):
    """Return a model and the expected (accumulator, RAM[0x80]) result."""
    if name == "add":
        return Tiny8([LDA_IMM, 5, ADD_IMM, 4, STA, 0x80, HLT]), (9, 9)
    if name == "countdown":
        # Addresses: 00 load, 02 subtract, 04 conditional jump, 06 jump, 08 store.
        program = [LDA_IMM, 3, SUB_IMM, 1, JZ, 8, JMP, 2, STA, 0x80, HLT]
        return Tiny8(program), (0, 0)
    if name == "load":
        model = Tiny8([LDA_ABS, 0x80, ADD_IMM, 1, STA, 0x80, HLT])
        model.ram[0x80] = 41
        return model, (42, 42)
    raise ValueError(f"unknown demo {name!r}")


def positive_integer(text):
    value = int(text)
    if value < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", choices=("add", "countdown", "load"), default="add")
    parser.add_argument("--max-cycles", type=positive_integer, default=200)
    args = parser.parse_args()
    model, expected = demo(args.demo)
    print("Intended Tiny8 behavior in Python; this does not run or verify the RTL.")
    print("Registers shown AFTER each edge; addr/read/we show the bus BEFORE it.")
    print("edge | before  -> after   | PC IR OP  A Z | addr read we")
    try:
        trace = model.run(args.max_cycles)
    except (ValueError, RuntimeError) as error:
        parser.exit(1, f"Model error: {error}\n")
    for row in trace:
        print(f"{row.cycle:4} | {row.previous_state:7} -> {row.state:7} | "
              f"{row.pc:02X} {row.ir:02X} {row.operand:02X} {row.acc:02X} {row.z_flag} | "
              f" {row.mem_addr:02X}   {row.mem_rdata:02X}  {int(row.mem_we)}")
    if (model.acc, model.ram[0x80]) != expected:
        parser.exit(1, "Model error: demo result disagrees with its expected values\n")
    print(f"PASS: {args.demo}, {model.cycles} edges, A={model.acc}, RAM[0x80]={model.ram[0x80]}")


if __name__ == "__main__":
    main()
