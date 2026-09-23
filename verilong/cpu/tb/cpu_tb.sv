// Testbench = a pretend lab bench. It is NOT synthesizable hardware.
//
// Its job:
//   1. Toggle clk
//   2. Hold rst, then release it
//   3. Stuff machine-code bytes into RAM  (this is your program)
//   4. Let the CPU run until HLT
//   5. Check whatever you care about (A, a memory address, ...)
//
// Loading a program means writing raw bytes into dut.u_mem.ram[address].
// First byte is the opcode (see cpu_pkg.sv). Next byte, if any, is the
// immediate or the address.
//
//   dut.u_mem.ram[0] = LDA_IMM;
//   dut.u_mem.ram[1] = 8'd3;      // A <- 3
//   dut.u_mem.ram[2] = HLT;

`timescale 1ns / 1ps

module cpu_tb;
  import cpu_pkg::*;

  logic       clk;
  logic       rst;
  logic       halted;
  logic [7:0] dbg_pc;
  logic [7:0] dbg_acc;
  logic [7:0] dbg_ir;
  state_t     dbg_state;
  logic [7:0] dbg_mem_addr;
  logic       dbg_mem_we;

  integer cycle;

  tiny8 dut (
    .clk          (clk),
    .rst          (rst),
    .halted       (halted),
    .dbg_pc       (dbg_pc),
    .dbg_acc      (dbg_acc),
    .dbg_ir       (dbg_ir),
    .dbg_state    (dbg_state),
    .dbg_mem_addr (dbg_mem_addr),
    .dbg_mem_we   (dbg_mem_we)
  );

  // Clock: flip every 5 time units -> 10 ns period.
  initial clk = 1'b0;
  always #5 clk = ~clk;

  function automatic string state_name(state_t s);
    case (s)
      S_FETCH:   return "FETCH";
      S_DECODE:  return "DECODE";
      S_OPERAND: return "OPERAND";
      S_EXECUTE: return "EXECUTE";
      S_LOAD:    return "LOAD";
      S_HALT:    return "HALT";
      default:   return "???";
    endcase
  endfunction

  function automatic string op_name(logic [7:0] ir);
    case (ir)
      NOP:     return "NOP";
      LDA_IMM: return "LDA #imm";
      ADD_IMM: return "ADD #imm";
      SUB_IMM: return "SUB #imm";
      AND_IMM: return "AND #imm";
      OR_IMM:  return "OR  #imm";
      STA:     return "STA addr";
      LDA_ABS: return "LDA addr";
      JMP:     return "JMP addr";
      JZ:      return "JZ  addr";
      HLT:     return "HLT";
      default: return "????";
    endcase
  endfunction

  task automatic load_program;
    // TODO: write your machine code into dut.u_mem.ram[ ... ]
    // Use the opcode names from cpu_pkg (LDA_IMM, ADD_IMM, HLT, ...).
  endtask

  initial begin
    $dumpfile("waves/tiny8.vcd");
    $dumpvars(0, cpu_tb);

    cycle = 0;
    rst   = 1'b1;
    load_program();

    // Hold reset across a few clocks, drop it on a falling edge so the
    // first rising edge is a clean FETCH.
    repeat (3) @(posedge clk);
    @(negedge clk);
    rst = 1'b0;
    #1;

    $display("");
    $display(" cycle  state     pc   ir           acc");
    $display("-------------------------------------------");

    while (!halted && cycle < 200) begin
      cycle = cycle + 1;
      $display("%5d  %-8s  %02h   %02h %-9s  %3d",
               cycle,
               state_name(dbg_state),
               dbg_pc,
               dbg_ir,
               op_name(dbg_ir),
               dbg_acc);
      @(posedge clk);
      #1;
    end

    $display("-------------------------------------------");
    $display("");

    // TODO: after HLT, check the results you care about. Examples of
    // the kinds of things you can test (delete these comments and write
    // your own):
    //
    //   if (!halted) $fatal(1, "never halted");
    //   if (dbg_acc !== 8'd??) $fatal(1, "A is wrong");
    //   if (dut.u_mem.ram[8'h80] !== 8'd??) $fatal(1, "mem is wrong");

    $display("halted=%0d  A=%0d  PC=%02h", halted, dbg_acc, dbg_pc);
    $finish;
  end

endmodule
