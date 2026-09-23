// 256 bytes of RAM. An 8-bit address covers 0x00 through 0xFF.
//
// Two different timings live in one module:
//   write  — sequential: happens on the rising edge of clk, and only if we=1
//   read   — combinational: rdata is whatever sits at ram[addr] right now
//
// What you need to write:
//   1. An array: 256 entries, each 8 bits
//   2. always_ff: if (we) ram[addr] <= wdata
//   3. assign rdata = ram[addr]
//
// The testbench will poke this array directly to load your program, e.g.
//   dut.u_mem.ram[0] = 8'h01;

module memory (
  input  logic       clk,
  input  logic       we,      // write-enable: 1 means "store wdata this clock"
  input  logic [7:0] addr,
  input  logic [7:0] wdata,
  output logic [7:0] rdata
);

  // TODO: declare the RAM array
  // logic [7:0] ram [0:255];

  always_ff @(posedge clk) begin
    // TODO: write ram[addr] when we is high
  end

  // TODO: combinational read
  assign rdata = 8'h00;

endmodule
