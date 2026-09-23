// Shared names used by every other file.
//
// A package is just a namespace. Other modules do `import cpu_pkg::*;`
// so they can write LDA_IMM or S_FETCH instead of raw numbers.
//
// You can add opcodes here later (XOR, a second register, OUT, ...).
// If you add one, you will also have to handle it in the ALU and/or CPU.

package cpu_pkg;

  // First byte of every instruction. Second byte (when needed) is either
  // a constant (#imm) or a memory address.
  typedef enum logic [7:0] {
    NOP     = 8'h00,  // do nothing, then fetch the next instruction
    LDA_IMM = 8'h01,  // A = the following byte
    ADD_IMM = 8'h02,  // A = A + the following byte
    SUB_IMM = 8'h03,  // A = A - the following byte
    AND_IMM = 8'h04,  // A = A & the following byte
    OR_IMM  = 8'h05,  // A = A | the following byte
    STA     = 8'h06,  // mem[following byte] = A
    LDA_ABS = 8'h07,  // A = mem[following byte]
    JMP     = 8'h08,  // PC = following byte (always jump)
    JZ      = 8'h09,  // if Z flag is set, PC = following byte
    HLT     = 8'h0A   // freeze the machine
  } opcode_t;

  // Control unit states. The CPU is in exactly one of these each clock.
  typedef enum logic [2:0] {
    S_FETCH,    // put PC on the address bus; capture mem[PC] as the opcode
    S_DECODE,   // look at the opcode: halt, need a 2nd byte, or execute now
    S_OPERAND,  // put PC on the address bus; capture mem[PC] as the operand
    S_EXECUTE,  // do the instruction (ALU / store / jump)
    S_LOAD,     // extra read cycle used only by LDA_ABS
    S_HALT
  } state_t;

  // Which operation the ALU should perform this cycle.
  typedef enum logic [1:0] {
    ALU_ADD = 2'b00,
    ALU_SUB = 2'b01,
    ALU_AND = 2'b10,
    ALU_OR  = 2'b11
  } alu_op_t;

endpackage
