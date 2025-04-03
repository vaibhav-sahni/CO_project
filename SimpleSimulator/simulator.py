import sys
class RISC_V_Simulator:
    def __init__(self):
        self.registers = [0] * 32  # 32 general-purpose registers
        self.registers[2]=380
        self.memory = [0]*((2**16))  # 32 words (each 32-bit)
        self.pc = 0  # Program counter
        self.halted = False
        self.output_file = "output.txt"
    def load_binary(self, filename):
        with open(filename, "r") as f:
            self.instructions = [line.strip() for line in f.readlines()]

    def execute(self):
        with open(self.output_file, "w") as out:
            while not self.halted and self.pc < len(self.instructions):
                self.registers[0] = 0  
                instruction = self.instructions[self.pc]
                self.log(f"Executing PC={self.pc * 4}: {instruction}")
                if instruction == "00000000000000000000000001100011":  # Virtual halt (beq x0, x0, 0)
                    self.halted = True
                    # self.pc += 1 
                    self.registers[0] = 0  
                    self.dump_registers(out)
                    self.log("Virtual halt encountered. Dumping memory...")
                    break
                self.decode_and_execute(instruction)
                self.pc += 1  # Increment PC
                self.registers[0] = 0 
                self.dump_registers(out)
            self.dump_memory(out)

    def decode_and_execute(self, instruction):
        opcode = instruction[-7:]  # Last 7 bits for opcode
        if opcode == "0110011":  # R-type (add, sub, and, or, srl, slt,mul)
            self.execute_r_type(instruction)
        elif opcode == "0000011":  # lw (load word)
            self.execute_lw(instruction)
        elif opcode == "0100011":  # sw (store word)
            self.execute_sw(instruction)
        elif opcode == "1100011":  # Branch instructions (beq, bne, blt)
            self.execute_b_type(instruction)
        elif opcode == "1101111":  # jal
            self.execute_jal(instruction)
        elif opcode == "1100111":  # jalr
            self.execute_jalr(instruction)
        elif opcode == "0010011":  # addi
            self.execute_addi(instruction)
        elif opcode=="0000000": #rst
            self.execute_rst(instruction) 
        elif opcode=="0001011": #rvrs--> reverse the string of bits
            self.execute_rvrs(instruction)
        else:
            self.log(f"Unknown instruction: {instruction}")
            self.halted = True  # Stop execution on unknown instruction
        # self.dump_registers(out)

    def to_twos_complement(self , value):
        if value < 0:
            return (1 << 32) + value  # Add 2^32 to negative numbers
        return value
    
    def to_signed(self , value):
        return value - (1 << 32) if value & (1 << 31) else value
    
    def execute_r_type(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        funct3 = instruction[17:20]
        funct7 = instruction[:7]
        if funct3 == "000" and funct7 == "0000000":  # ADD
            self.registers[rd] = (self.registers[rs1] + self.registers[rs2]) & 0xFFFFFFFF
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"ADD x{rd} = x{rs1} + x{rs2} -> {self.registers[rd]}")

        elif funct3 == "000" and funct7 == "0100000":  # SUB
            self.registers[rd] = (self.registers[rs1] - self.registers[rs2])  & 0xFFFFFFFF
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"SUB x{rd} = x{rs1} - x{rs2} -> {self.registers[rd]}")

        elif funct3 == "111" and funct7 == "0000000":  # AND
            self.registers[rd] = (self.registers[rs1] & self.registers[rs2]) 
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"AND x{rd} = x{rs1} & x{rs2} -> {self.registers[rd]}")

        elif funct3 == "110" and funct7 == "0000000":  # OR
            self.registers[rd] = self.registers[rs1] | self.registers[rs2]
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
    
            self.log(f"OR x{rd} = x{rs1} | x{rs2} -> {self.registers[rd]}")

        elif funct3 == "010" and funct7 == "0000000":  # SLT
            rs1_value = self.to_signed(self.registers[rs1])
            rs2_value = self.to_signed(self.registers[rs2])
            self.registers[rd] = 1 if rs1_value < rs2_value else 0
            self.log(f"SLT x{rd} = x{rs1} < x{rs2} -> {self.registers[rd]}")
    
        elif funct3 == "101" and funct7 == "0000000":  # SRL
            shift_amount = self.registers[rs2] & 0x1F  # Extract lower 5 bit
            self.registers[rd] = (self.registers[rs1] >> shift_amount) & 0xFFFFFFFF
            self.log(f"SRL x{rd} = x{rs1} >> x{rs2} -> {self.registers[rd]}")

        elif funct3 == "000" and funct7 == "0000001":  # MUL
            self.registers[rd] = (self.registers[rs1] * self.registers[rs2]) & 0xFFFFFFFF # Keep only lower 32 bits
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"MUL x{rd} = x{rs1}*x{rs2} -> {self.registers[rd]}")

        else:
            self.log(f"Unknown R-type instruction: {instruction}")
            self.halted = True
        
        self.registers[0] = 0 

    def execute_rst(self,instruction): #reset instruction reset the registers to initial state
        if(instruction[0:7]=="0000000"):
            for i in range(0, 32):  # Reset all registers except Pc
                self.registers[i] = 0
            self.registers[2]=380
            self.log("Registers reset to initial state.")
        else:
            self.log("Invalid reset instruction.")
            self.halted=True
    
    def execute_rvrs(self, instruction):
        # Opcode = 0001011
        # Funct7 = 0000001
        # Funct3 = 000
        rd = int(instruction[20:25], 2)  # Destination register
        rs1 = int(instruction[12:17], 2)  # Source register
    
        # Get the value from rs1
        value = self.registers[rs1]
    
        reversed_value = 0
        for i in range(32):  
            # Extract bit at position i from original value
            bit = (value >> i) & 1
            # Place it at position (31-i) in the result
            reversed_value |= (bit << (31 - i))
    
        if rd != 0:
            self.registers[rd] = reversed_value
    
        # Convert to two's complement before logging
        self.registers[rd] = self.to_twos_complement(self.registers[rd])
        self.log(f"RVRS x{rd} = reversed(x{rs1}) -> {self.registers[rd]}")
    
    def execute_b_type(self, instruction):
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        funct3 = instruction[17:20]
    # Correct Immediate Extraction (B-type format)
        imm = (instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + "0")
        imm = int(imm, 2)
       

        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 13)
    # Execute branch
        if funct3 == "000":  # BEQ
            if self.registers[rs1] == self.registers[rs2]:
                if(imm==0 or imm//4==0): # Check if immediate is zero --> halt
                    self.halted=True
                    self.log("Virtual halt encountered. Dumping memory...")
                self.pc += imm // 4  # Convert byte offset to instruction offset
                self.log(f"BEQ: x{rs1} == x{rs2}, PC updated to {self.pc * 4}")
                self.pc -= 1 
        elif funct3 == "001":  # BNE
            if self.registers[rs1] != self.registers[rs2]:
                self.pc += imm // 4
                self.log(f"BNE: x{rs1} != x{rs2}, PC updated to {self.pc * 4}")
                self.pc -= 1 
        else:
            self.log(f"Unknown branch instruction: {instruction}")
            self.halted = True  # Stop execution on unknown instruction

    def execute_lw(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)

        imm = int(instruction[:12], 2)
        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 12)

        # Calculate byte-level address
        addr = self.registers[rs1] + imm
        
        # Convert to word index in memory array
        memory_index = addr // 4
        
        if 0 <= memory_index < len(self.memory):
            if rd != 0 : 
                self.registers[rd] = self.memory[memory_index]
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"LW x{rd} = memory[x{rs1} + {imm}={addr}] -> {self.registers[rd]}")
        else:
            self.log(f"LW: Invalid memory access at {addr}")
            self.halted = True  # Stop execution on invalid memory access

    def execute_sw(self, instruction):
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        imm = int(instruction[:7] + instruction[20:25], 2)
        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 12)
        addr = self.registers[rs1] + imm
        memory_index = (addr // 4)
        if 0 <= memory_index < len(self.memory):
            self.memory[memory_index] = self.registers[rs2]
            # self.log(f"SW memory[x{rs1} + {imm}={addr}] = x{rs2} -> {self.memory[memory_index]}")
            self.log(f"Memory[{hex(addr)}] (index {memory_index}) set to {self.memory[memory_index]}")
        else:
            self.log(f"SW: Invalid memory access at {addr}")
            self.halted = True  # Stop execution on invalid memory access

    def execute_addi(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        
        imm = int(instruction[:12], 2)
        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 12)
        if rd != 0 : 
            self.registers[rd] = (self.registers[rs1] + imm)  & 0xFFFFFFFF  # Keep result in 32-bit range
        # Convert to two's complement before logging/writing
        self.registers[rd] = self.to_twos_complement(self.registers[rd])
        self.log(f"ADDI x{rd} = x{rs1} + {imm} -> {self.registers[rd]}")

    def execute_jalr(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        imm = int(instruction[:12], 2)
 
        # sign extending the immediate 
        if instruction[0] == "1":  # Sign extension for negative values
             imm -= (1 << 12)

        if rd != 0 : 
            self.registers[rd] = (self.pc*4) + 4 
        
        self.pc = (self.registers[rs1] + imm)//4 
        self.log(f"JALR x{rd} = PC + 1; PC = x{rs1} + {imm} -> {self.pc * 4}")
        self.pc = self.pc - 1 

    
    def execute_jal(self, instruction):
        rd = int(instruction[20:25], 2)    # Destination register (rd)
        imm = (instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0")
        imm = int(imm, 2)
        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 21)

        if rd!= 0 : 
            self.registers[rd] = self.pc*4 + 4

        # Update the program counter
        self.pc += imm // 4 - 1  # Jump and adjust for loop increment
        self.log(f"JAL x{rd} = {self.registers[rd]}, PC updated to {self.pc * 4}")
        # self.pc = self.pc - 1

    def dump_registers(self, file):
        file.write(f"0b{'{:032b}'.format(self.pc * 4)} " + " ".join(f"0b{'{:032b}'.format(reg)}" for reg in self.registers) + "\n")
    
    def dump_memory(self, file):
        start_addr = 0x00010000  # Starting memory address
        for i in range(32): 
            addr = start_addr + (i * 4)  # Compute actual memory address
            file.write(f"0x{addr:08X}:0b{self.memory[addr // 4]:032b}\n")  # Binary format with 32 bits
    def log(self, message):
        print(message)   

read_filepath = sys.argv[1]
write_filepath = sys.argv[2]
def main(read_filepath, write_filepath): 
    simulator = RISC_V_Simulator()
    simulator.output_file = write_filepath
    simulator.load_binary(read_filepath)
    simulator.execute()
main(read_filepath, write_filepath)
