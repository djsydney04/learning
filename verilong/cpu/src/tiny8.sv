// Top of the chip: one CPU and one RAM sharing a bus.
//
// You instantiate modules the way you call functions, except the
// connections stay there forever as wires. This file is the wiring.
//
//   cpu.mem_addr  -----> memory.addr
//   cpu.mem_wdata -----> memory.wdata
//   cpu.mem_we    -----> memory.we
//   memory.rdata  -----> cpu.mem_rdata
//
// The dbg_* ports just peek at internal signals so the testbench can print.

module tiny8
  import cpu_pkg::*;
(
  input  logic       clk,
  input  logic       rst,
  output logic       halted,
  output logic [7:0] dbg_pc,
  output logic [7:0] dbg_acc,
  output logic [7:0] dbg_ir,
  output state_t     dbg_state,
  output logic [7:0] dbg_mem_addr,
  output logic       dbg_mem_we
);

  logic [7:0] mem_addr;
  logic [7:0] mem_wdata;
  logic [7:0] mem_rdata;
  logic       mem_we;

  // TODO: instantiate cpu as u_cpu and memory as u_mem.
  // Connect the four bus signals above, plus clk/rst and the dbg ports.
  //
  // The testbench loads programs with dut.u_mem.ram[addr], so the memory
  // instance must be named u_mem.

  cpu u_cpu (
    .clk       (clk),
    .rst       (rst),
    .mem_addr  (mem_addr),
    .mem_wdata (mem_wdata),
    .mem_rdata (mem_rdata),
    .mem_we    (mem_we),
    .halted    (halted),
    .dbg_pc    (dbg_pc),
    .dbg_acc   (dbg_acc),
    .dbg_ir    (dbg_ir),
    .dbg_state (dbg_state)
  );

  memory u_mem (
    .clk   (clk),
    .we    (mem_we),
    .addr  (mem_addr),
    .wdata (mem_wdata),
    .rdata (mem_rdata)
  );

  assign dbg_mem_addr = mem_addr;
  assign dbg_mem_we   = mem_we;

endmodule
