"""Check teaching-model claims against arithmetic and hand-derived traces.

These tests check the Python examples only. Passing does not validate any
SystemVerilog implementation or physical timing constraint.
"""

import importlib.util
from pathlib import Path
import sys
import unittest


EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENTS / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


logic = load_module("foundation_logic", "01_logic.py")
clock = load_module("foundation_clock", "02_clock.py")
cpu = load_module("foundation_tiny8", "03_tiny8.py")


class LogicTests(unittest.TestCase):
    def test_full_adder_truth_table(self):
        expected = ((0, 0), (1, 0), (1, 0), (0, 1),
                    (1, 0), (0, 1), (0, 1), (1, 1))
        for inputs, output in zip(((a, b, c) for a in (0, 1)
                                  for b in (0, 1) for c in (0, 1)), expected):
            with self.subTest(inputs=inputs):
                self.assertEqual(logic.full_adder(*inputs), output)

    def test_every_pair_of_eight_bit_operands(self):
        # Compare the gate-based implementation with integer arithmetic,
        # not with a second copy of its carry equations.
        for a in range(256):
            for b in range(256):
                result, carry = logic.ripple_add(a, b)
                self.assertEqual((result, carry), ((a + b) % 256, (a + b) // 256))

    def test_reject_invalid_inputs(self):
        for args in ((-1, 0), (256, 0), (0, 256), (0, 0, 0)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                logic.ripple_add(*args)
        with self.assertRaises(ValueError):
            logic.full_adder(1, 2, 0)


class ClockTests(unittest.TestCase):
    def test_second_stage_receives_old_first_stage(self):
        model = clock.Pipeline()
        self.assertEqual(model.tick(5), (5, 0))
        self.assertEqual(model.tick(9), (9, 5))
        self.assertEqual(model.tick(7, enable=False), (9, 5))
        self.assertEqual(model.tick(4), (4, 9))

    def test_reset_clears_both_stages(self):
        model = clock.Pipeline()
        model.tick(255)
        model.tick(128)
        model.reset()
        self.assertEqual((model.stage1, model.stage2), (0, 0))
        self.assertEqual(model.tick(6), (6, 0))


class Tiny8Tests(unittest.TestCase):
    def test_add_demo_matches_hand_derived_edges(self):
        model, _ = cpu.demo("add")
        trace = model.run()
        # Each tuple is the post-edge state, PC, IR, operand, A, and Z.
        expected = [
            ("DECODE", 1, 1, 0, 0, 0),
            ("OPERAND", 1, 1, 0, 0, 0),
            ("EXECUTE", 2, 1, 5, 0, 0),
            ("FETCH", 2, 1, 5, 5, 0),
            ("DECODE", 3, 2, 5, 5, 0),
            ("OPERAND", 3, 2, 5, 5, 0),
            ("EXECUTE", 4, 2, 4, 5, 0),
            ("FETCH", 4, 2, 4, 9, 0),
            ("DECODE", 5, 6, 4, 9, 0),
            ("OPERAND", 5, 6, 4, 9, 0),
            ("EXECUTE", 6, 6, 128, 9, 0),
            ("FETCH", 6, 6, 128, 9, 0),
            ("DECODE", 7, 10, 128, 9, 0),
            ("HALT", 7, 10, 128, 9, 0),
        ]
        actual = [(row.state, row.pc, row.ir, row.operand, row.acc, row.z_flag)
                  for row in trace]
        self.assertEqual(actual, expected)
        self.assertEqual(model.ram[128], 9)
        self.assertEqual([row.cycle for row in trace if row.mem_we], [12])
        self.assertEqual((trace[11].mem_addr, trace[11].mem_wdata), (128, 9))

    def test_alu_operations_and_zero_flag(self):
        for opcode, a, operand, result in (
            (cpu.ADD_IMM, 250, 10, 4),
            (cpu.ADD_IMM, 255, 1, 0),
            (cpu.SUB_IMM, 0, 1, 255),
            (cpu.SUB_IMM, 7, 7, 0),
            (cpu.AND_IMM, 0xA5, 0x0F, 0x05),
            (cpu.AND_IMM, 0xF0, 0x0F, 0),
            (cpu.OR_IMM, 0x80, 0x01, 0x81),
            (cpu.OR_IMM, 0, 0, 0),
        ):
            with self.subTest(opcode=opcode, a=a, operand=operand):
                model = cpu.Tiny8([opcode, operand, cpu.HLT])
                model.acc = a
                model.run()
                self.assertEqual(model.acc, result)
                self.assertEqual(model.z_flag, int(result == 0))

    def test_memory_load_has_extra_edge_and_preserves_address_value(self):
        model = cpu.Tiny8([cpu.LDA_ABS, 128, cpu.HLT])
        model.ram[128] = 41
        trace = model.run()
        self.assertEqual([row.state for row in trace],
                         ["DECODE", "OPERAND", "EXECUTE", "LOAD", "FETCH", "DECODE", "HALT"])
        self.assertEqual(trace[3].acc, 0)  # EXECUTE prepares the load, not the accumulator.
        self.assertEqual(trace[4].acc, 41)
        self.assertEqual((trace[4].mem_addr, trace[4].mem_rdata), (128, 41))
        self.assertEqual(model.ram[128], 41)
        self.assertEqual(model.z_flag, 0)

    def test_memory_zero_load_sets_zero_flag(self):
        model = cpu.Tiny8([cpu.LDA_IMM, 9, cpu.LDA_ABS, 128, cpu.HLT])
        model.run()
        self.assertEqual((model.acc, model.z_flag), (0, 1))

    def test_branch_taken_and_not_taken(self):
        for initial, expected, edges in ((0, 0, 10), (1, 99, 14)):
            with self.subTest(initial=initial):
                model = cpu.Tiny8([cpu.LDA_IMM, initial, cpu.JZ, 6,
                                   cpu.LDA_IMM, 99, cpu.HLT])
                model.run()
                self.assertEqual((model.acc, model.pc, model.cycles), (expected, 7, edges))

    def test_store_nop_and_jumps_preserve_zero_flag(self):
        # The branch skips LDA #99 only if all intervening instructions preserve Z.
        program = [cpu.LDA_IMM, 0, cpu.STA, 128, cpu.NOP, cpu.JZ, 9,
                   cpu.LDA_IMM, 99, cpu.HLT]
        model = cpu.Tiny8(program)
        trace = model.run()
        self.assertEqual((model.acc, model.z_flag), (0, 1))
        self.assertTrue(all(row.z_flag == 1 for row in trace[3:]))
        model = cpu.Tiny8([cpu.LDA_IMM, 0, cpu.JMP, 6, cpu.LDA_IMM, 99, cpu.HLT])
        model.run()
        self.assertEqual((model.acc, model.z_flag), (0, 1))

    def test_reset_initial_zero_flag_is_low_and_ram_survives_reset(self):
        model = cpu.Tiny8([cpu.JZ, 4, cpu.LDA_IMM, 9, cpu.HLT])
        self.assertEqual((model.acc, model.z_flag), (0, 0))
        model.run()
        self.assertEqual(model.acc, 9)  # Reset A=0 alone does not make JZ taken.
        model.ram[128] = 77
        model.reset()
        self.assertEqual((model.pc, model.ir, model.operand, model.acc,
                          model.z_flag, model.state, model.cycles),
                         (0, 0, 0, 0, 0, "FETCH", 0))
        self.assertEqual(model.ram[128], 77)

    def test_program_counter_wraps_after_fetch_and_operand(self):
        model = cpu.Tiny8([0x9A, cpu.HLT])
        model.ram[255] = cpu.LDA_IMM
        model.pc = 255
        trace = model.run()
        self.assertEqual(trace[0].pc, 0)
        self.assertEqual((model.acc, model.pc), (0x9A, 2))
        model = cpu.Tiny8([cpu.HLT])
        model.ram[254:256] = [cpu.LDA_IMM, 33]
        model.pc = 254
        trace = model.run()
        self.assertEqual(trace[2].pc, 0)
        self.assertEqual((model.acc, model.pc), (33, 1))

    def test_halt_preserves_state_on_later_edges(self):
        model = cpu.Tiny8([cpu.HLT])
        self.assertEqual(len(model.run()), 2)
        before = (model.pc, model.ir, model.operand, model.acc, model.z_flag)
        row = model.step()
        self.assertEqual(row.state, "HALT")
        self.assertEqual((model.pc, model.ir, model.operand, model.acc, model.z_flag), before)

    def test_all_three_demo_outcomes(self):
        for name, edges, expected in (("add", 14, (9, 9)),
                                      ("countdown", 42, (0, 0)),
                                      ("load", 15, (42, 42))):
            with self.subTest(name=name):
                model, _ = cpu.demo(name)
                model.run()
                self.assertEqual((model.acc, model.ram[128]), expected)
                self.assertEqual(model.cycles, edges)

    def test_loop_exhausts_budget_and_unknown_opcode_is_model_error(self):
        with self.assertRaisesRegex(RuntimeError, "did not halt"):
            cpu.Tiny8([cpu.JMP, 0]).run(20)
        with self.assertRaisesRegex(ValueError, "unknown opcode"):
            cpu.Tiny8([0xFF]).run()
        with self.assertRaises(ValueError):
            cpu.Tiny8([cpu.HLT]).run(0)


if __name__ == "__main__":
    unittest.main()
