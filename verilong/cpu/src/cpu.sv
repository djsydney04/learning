// The microprocessor itself: pieces wired together + the control FSM.
//
// High-level idea
// ---------------
// Software is just bytes in RAM. Each clock the CPU is in one state.
// Together the states walk an instruction:
//
//   FETCH    read opcode from mem[PC], then increment PC
//   DECODE   decide: HLT? needs a second byte? or go execute (NOP)
//   OPERAND  read that second byte from mem[PC], then increment PC
//   EXECUTE  do the work
//   LOAD     only for LDA_ABS: A = mem[operand]  (operand is an address)
//   HALT     stay here
//
// Pieces you implement in other files, then use here
// --------------------------------------------------
//   alu      already instantiated — you choose nothing here except
//            trusting decoder.alu_op
//   decoder  turns IR into needs_operand / is_alu / alu_op / is_halt
//   pc       the program-counter register (inc, load, reset)
//
// Registers that still live in this file
// --------------------------------------
//   acc      the accumulator, A
//   ir       instruction register — the opcode we fetched
//   operand  the second instruction byte
//   z_flag   1 if the last write to A produced 0
//   state    which FSM state we are in
//
// Memory bus you drive
// --------------------
//   FETCH / OPERAND  -> addr = pc
//   STA              -> addr = operand, we = 1
//   LDA_ABS / LOAD   -> addr = operand
//
// Suggested order
// ---------------
//   1. decoder + pc modules
//   2. Reset + FETCH + DECODE + HLT
//   3. OPERAND + LDA_IMM
//   4. ALU ops via is_alu / alu_result
//   5. STA, then JMP / JZ (pc_load), then LDA_ABS

module cpu
  import cpu_pkg::*;
(
  input  logic       clk,
  input  logic       rst,

  output logic [7:0] mem_addr,
  output logic [7:0] mem_wdata,
  input  logic [7:0] mem_rdata,
  output logic       mem_we,

  output logic       halted,
  output logic [7:0] dbg_pc,
  output logic [7:0] dbg_acc,
  output logic [7:0] dbg_ir,
  output state_t     dbg_state
);

  logic [7:0] acc;
  logic [7:0] ir;
  logic [7:0] operand;
  logic       z_flag;
  state_t     state;

  opcode_t opcode;
  assign opcode = opcode_t'(ir);

  // ---- decoder: opcode -> flags the FSM uses ----
  logic    needs_operand;
  logic    is_alu;
  alu_op_t alu_op;
  logic    is_halt;

  decoder u_decoder (
    .opcode        (opcode),
    .needs_operand (needs_operand),
    .is_alu        (is_alu),
    .alu_op        (alu_op),
    .is_halt       (is_halt)
  );

  // ---- ALU: A and operand in, result out ----
  logic [7:0] alu_result;
  logic       alu_zero;

  alu u_alu (
    .a      (acc),
    .b      (operand),
    .op     (alu_op),
    .result (alu_result),
    .zero   (alu_zero)
  );

  // ---- program counter ----
  logic       pc_inc;
  logic       pc_load;
  logic [7:0] pc;

  pc u_pc (
    .clk       (clk),
    .rst       (rst),
    .inc       (pc_inc),
    .load      (pc_load),
    .load_data (operand),
    .value     (pc)
  );

  // Drive pc_inc / pc_load from the current state.
  always_comb begin
    pc_inc  = 1'b0;
    pc_load = 1'b0;

    // TODO:
    //   FETCH or OPERAND -> pc_inc = 1
    //   EXECUTE + JMP    -> pc_load = 1
    //   EXECUTE + JZ and z_flag -> pc_load = 1
  end

  // Memory bus.
  always_comb begin
    mem_addr  = pc;
    mem_wdata = acc;
    mem_we    = 1'b0;

    // TODO:
    //   FETCH / OPERAND : addr = pc
    //   STA             : addr = operand, we = 1
    //   LDA_ABS / LOAD  : addr = operand
  end

  assign halted    = (state == S_HALT);
  assign dbg_pc    = pc;
  assign dbg_acc   = acc;
  assign dbg_ir    = ir;
  assign dbg_state = state;

  always_ff @(posedge clk or posedge rst) begin
    if (rst) begin
      acc     <= 8'h00;
      ir      <= 8'h00;
      operand <= 8'h00;
      z_flag  <= 1'b0;
      state   <= S_FETCH;
    end else begin

      // TODO: case (state)
      //
      // S_FETCH:
      //   ir    <= mem_rdata
      //   state <= S_DECODE
      //   (PC increments by itself if you set pc_inc)
      //
      // S_DECODE:
      //   is_halt        -> S_HALT
      //   needs_operand  -> S_OPERAND
      //   else           -> S_EXECUTE
      //
      // S_OPERAND:
      //   operand <= mem_rdata
      //   state   <= S_EXECUTE
      //
      // S_EXECUTE: case (opcode)
      //   NOP      -> FETCH
      //   LDA_IMM  -> acc <= operand; update z_flag
      //   is_alu   -> acc <= alu_result; z_flag <= alu_zero
      //   STA      -> FETCH  (write is already on the bus)
      //   LDA_ABS  -> S_LOAD
      //   JMP / JZ -> FETCH  (PC load is already driven above)
      //
      // S_LOAD:
      //   acc <= mem_rdata; update z_flag; FETCH
      //
      // S_HALT:
      //   stay

    end
  end

endmodule
