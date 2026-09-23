// Isolated ALU test. You can run this before the CPU exists:
//
//   make sim-alu
//
// Drive a, b, and op, then check result and zero.

`timescale 1ns / 1ps

module alu_tb;
  import cpu_pkg::*;

  logic [7:0] a;
  logic [7:0] b;
  alu_op_t    op;
  logic [7:0] result;
  logic       zero;

  alu dut (
    .a      (a),
    .b      (b),
    .op     (op),
    .result (result),
    .zero   (zero)
  );

  initial begin
    a  = 8'h00;
    b  = 8'h00;
    op = ALU_ADD;
    #1;

    // TODO: set a, b, op, wait a moment (#1), then check result / zero.
    //
    //   a  = 8'd7;
    //   b  = 8'd4;
    //   op = ALU_ADD;
    //   #1;
    //   if (result !== 8'd11) $fatal(1, "ADD is wrong");

    $display("ALU  a=%0d  b=%0d  result=%0d  zero=%0d", a, b, result, zero);
    $finish;
  end

endmodule
