// ALU = Arithmetic Logic Unit.
//
// This block has NO clock. It is combinational: when a, b, or op change,
// result and zero change in the same instant.
//
// The CPU decides when those outputs matter. It only copies `result` into
// the accumulator inside an always_ff (on a clock edge).
//
// What you need to write:
//   result = a + b, a - b, a & b, or a | b, depending on op
//   zero   = 1 when result is 0x00, else 0

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

    // TODO: case (op)
    //   ALU_ADD: result = ...
    //   ALU_SUB: result = ...
    //   ALU_AND: result = ...
    //   ALU_OR:  result = ...
  end

  // TODO: drive `zero` from `result`
  assign zero = 1'b0;

endmodule
