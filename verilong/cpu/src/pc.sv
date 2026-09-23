// Program counter.
//
// A register that holds "which memory address do I fetch next?"
// Three things can happen on a clock:
//   rst  -> value becomes 0
//   inc  -> value becomes value + 1     (after reading a program byte)
//   load -> value becomes load_data     (JMP / JZ)
//
// If load and inc are both 1, load wins (a jump replaces the increment).

module pc (
  input  logic       clk,
  input  logic       rst,
  input  logic       inc,
  input  logic       load,
  input  logic [7:0] load_data,
  output logic [7:0] value
);

  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      value <= 8'h00;
    end else begin
      // TODO:
      //   if (load) value <= load_data
      //   else if (inc) value <= value + 1
    end
  end

endmodule
