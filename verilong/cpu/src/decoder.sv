// Combinational instruction decoder.
//
// Input:  the opcode sitting in IR
// Output: facts the FSM needs, with no clock
//
//   needs_operand  1 if this instruction has a second byte
//   is_alu         1 if EXECUTE should copy the ALU result into A
//   alu_op         which ALU operation (only matters when is_alu is 1)
//   is_halt        1 if DECODE should go to S_HALT

module decoder
  import cpu_pkg::*;
(
  input  opcode_t opcode,
  output logic    needs_operand,
  output logic    is_alu,
  output alu_op_t alu_op,
  output logic    is_halt
);

  always_comb begin
    needs_operand = 1'b0;
    is_alu        = 1'b0;
    alu_op        = ALU_ADD;
    is_halt       = 1'b0;

    // TODO: case (opcode)
    //   HLT:     is_halt = 1
    //   NOP:     nothing
    //   LDA_IMM, STA, LDA_ABS, JMP, JZ: needs_operand = 1
    //   ADD_IMM / SUB_IMM / AND_IMM / OR_IMM:
    //     needs_operand = 1, is_alu = 1, alu_op = the matching ALU_* 
  end

endmodule
