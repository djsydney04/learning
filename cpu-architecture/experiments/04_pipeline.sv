`timescale 1ns/1ps

// Completed primer example. This is independent of the Tiny8 exercises.
module pipeline_pair (
  input  logic       clk,
  input  logic       rst,
  input  logic       enable,
  input  logic [7:0] data_in,
  output logic [7:0] stage1,
  output logic [7:0] stage2
);
  always_ff @(posedge clk) begin
    if (rst) begin
      stage1 <= 8'h00;
      stage2 <= 8'h00;
    end else if (enable) begin
      stage1 <= data_in;
      stage2 <= stage1;
    end
  end
endmodule

module testbench;
  logic clk = 1'b0;
  logic rst = 1'b1;
  logic enable = 1'b0;
  logic [7:0] data_in = 8'h00;
  logic [7:0] stage1, stage2;

  pipeline_pair dut (
    .clk(clk), .rst(rst), .enable(enable), .data_in(data_in),
    .stage1(stage1), .stage2(stage2)
  );

  always #5 clk = ~clk;

  task automatic check(input logic [7:0] expected1, expected2);
    begin
      if (stage1 !== expected1 || stage2 !== expected2)
        $fatal(1, "expected stages %0d,%0d; got %0d,%0d",
               expected1, expected2, stage1, stage2);
      $display("data=%0d enable=%b rst=%b -> stage1=%0d stage2=%0d",
               data_in, enable, rst, stage1, stage2);
    end
  endtask

  initial begin
    $dumpfile(".build/pipeline.vcd");
    $dumpvars(0, testbench);

    @(posedge clk); #1; check(0, 0);
    @(negedge clk); rst = 0; enable = 1; data_in = 5;
    @(posedge clk); #1; check(5, 0);
    @(negedge clk); data_in = 9;
    @(posedge clk); #1; check(9, 5);
    @(negedge clk); enable = 0; data_in = 12;
    @(posedge clk); #1; check(9, 5);
    @(negedge clk); enable = 1;
    @(posedge clk); #1; check(12, 9);
    @(negedge clk); rst = 1;
    @(posedge clk); #1; check(0, 0);

    $display("PASS: pipeline register transfers, hold, and reset");
    $finish;
  end

  initial begin
    #200;
    $fatal(1, "testbench timeout");
  end
endmodule
