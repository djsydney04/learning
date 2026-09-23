// ALU = arithmetic logic unit. The box that adds, subtracts, ANDs, and ORs.
//
// There is no clk here. This is always_comb: when a, b, or op change,
// result and zero change in that same moment. Nothing in this file waits
// for a rising edge, and nothing in this file is stored.
//
// In the ADD walkthrough, A is still 0 and the operand has just become 4.
// This box's result wire is already 4. A becomes 4 only later, when cpu.sv
// copies result into the accumulator on a rising edge.
//
//   a       usually the accumulator
//   b       usually the operand byte (the 4 in ADD #4)
//   op      which operation: ALU_ADD, ALU_SUB, ALU_AND, or ALU_OR
//   result  a + b, a - b, a & b, or a | b
//   zero    1 when result is 8'h00, otherwise 0. JZ reads this bit.
//
// What you write:
//   the case that sets result from op
//   the assign that sets zero from result

module alu
  import cpu_pkg::*;
(
  input  logic [7:0] a,       // usually the accumulator
  input  logic [7:0] b,       // usually the instruction's operand byte
  input  alu_op_t    op,
  output logic [7:0] result,
  output logic       zero
);

  always_comb begin
    result = 8'h00;   // default so the file compiles; replace this

    case (op)
    ALU_ADD: result = a + b
    ALU_SUB: result = a - b
    ALU_AND: result = a & b
    ALU_OR:  result = a || b
  end

  // TODO: drive `zero` from `result`
  assign zero = 1'b0;

endmodule
