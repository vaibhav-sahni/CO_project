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
                self.registers[0] = 0 ; # hardcoding x0 to 0 
                instruction = self.instructions[self.pc]
                self.log(f"Executing PC={self.pc * 4}: {instruction}")

                if instruction == "00000000000000000000000001100011":  # Virtual halt (beq x0, x0, 0)
                    self.halted = True
                    # self.pc += 1 
                    self.dump_registers(out)
                    self.log("Virtual halt encountered. Dumping memory...")
                    break

                self.decode_and_execute(instruction)
                self.pc += 1  # Increment PC
                self.dump_registers(out)
            self.dump_memory(out)

    def decode_and_execute(self, instruction):
        opcode = instruction[-7:]  # Last 7 bits for opcode
        if opcode == "0110011":  # R-type (add, sub, and, or, srl, slt)
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

    def to_twos_complement(self , value):
        if value < 0:
            return (1 << 32) + value  # Add 2^32 to negative numbers
        return value

    def execute_r_type(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        funct3 = instruction[17:20]
        funct7 = instruction[:7]

        if funct3 == "000" and funct7 == "0000000":  # ADD
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]

            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])

            self.log(f"ADD x{rd} = x{rs1} + x{rs2} -> {self.registers[rd]}")

        elif funct3 == "000" and funct7 == "0100000":  # SUB
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]

            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])

            self.log(f"SUB x{rd} = x{rs1} - x{rs2} -> {self.registers[rd]}")

        elif funct3 == "111" and funct7 == "0000000":  # AND
            self.registers[rd] = self.registers[rs1] & self.registers[rs2]
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"AND x{rd} = x{rs1} & x{rs2} -> {self.registers[rd]}")

        elif funct3 == "110" and funct7 == "0000000":  # OR
            self.registers[rd] = self.registers[rs1] | self.registers[rs2]
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
        
            self.log(f"OR x{rd} = x{rs1} | x{rs2} -> {self.registers[rd]}")

        elif funct3 == "010" and funct7 == "0000000":  # SLT
            self.registers[rd] = 1 if self.registers[rs1] < self.registers[rs2] else 0
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])

            self.log(f"SLT x{rd} = x{rs1} < x{rs2} -> {self.registers[rd]}")

        elif funct3 == "101" and funct7 == "0000000":  # SRL
            self.registers[rd] = self.registers[rs1] >> self.registers[rs2]
            # Convert to two's complement before logging/writing
            self.registers[rd] = self.to_twos_complement(self.registers[rd])

            self.log(f"SRL x{rd} = x{rs1} >> x{rs2} -> {self.registers[rd]}")


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
                self.pc += imm // 4  # Convert byte offset to instruction offset
                self.log(f"BEQ: x{rs1} == x{rs2}, PC updated to {self.pc * 4}")
                self.pc -= 1 

        elif funct3 == "001":  # BNE
            if self.registers[rs1] != self.registers[rs2]:
                self.pc += imm // 4
                self.log(f"BNE: x{rs1} != x{rs2}, PC updated to {self.pc * 4}")
                self.pc -= 1 

        elif funct3 == "100":  # BLT
            if self.registers[rs1] < self.registers[rs2]:
                self.pc += imm // 4
                self.log(f"BLT: x{rs1} < x{rs2}, PC updated to {self.pc * 4}")
                self.pc -= 1
                
    
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
            self.registers[rd] = self.memory[memory_index]
            self.registers[rd] = self.to_twos_complement(self.registers[rd])
            self.log(f"LW x{rd} = memory[x{rs1} + {imm}={addr}] -> {self.registers[rd]}")
        else:
            self.log(f"LW: Invalid memory access at {addr}")

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
            self.log(f"SW memory[x{rs1} + {imm}={addr}] = x{rs2} -> {self.memory[memory_index]}")
        else:
            self.log(f"SW: Invalid memory access at {addr}")

    def execute_addi(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        
        # Correct two's complement conversion
        imm = int(instruction[:12], 2)
        # imm = self.sign_extend(imm, 12)
        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 12)
        
        self.registers[rd] = self.registers[rs1] + imm
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
          self.registers[rd] = self.pc - 4 
          self.pc = (self.registers[rs1] + imm)//4 
          self.log(f"JALR x{rd} = PC + 1; PC = x{rs1} + {imm} -> {self.pc * 4}")
          self.pc = self.pc - 1 

    def execute_jal(self, instruction):
        rd = int(instruction[20:25], 2)    # Destination register (rd)
        imm = (instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + "0")
        imm = int(imm, 2)
        if instruction[0] == "1":  # Sign extension for negative values
            imm -= (1 << 21)

        self.registers[rd] = self.pc*4 + 4

        # Update the program counter
        self.pc += imm // 4 - 1  # Jump and adjust for loop increment
        self.log(f"JAL x{rd} = {self.registers[rd]}, PC updated to {self.pc * 4}")
        # self.pc = self.pc - 1

    def dump_registers(self, file):
        file.write(f"0b{'{:032b}'.format(self.pc * 4)} " + " ".join(f"0b{'{:032b}'.format(reg)}" for reg in self.registers) + "\n")
    # def dump_memory(self, file):
    #     for i in range(32):
    #         addr = f"0x0001{(i * 4):04X}"
    #         file.write(f"{addr}:{"0b{:032b}".format(self.memory[i])}\n")

    def dump_memory(self, file):
        start_addr = 0x00010000  # Starting memory address
        for i in range(32): 
            addr = start_addr + (i * 4)  # Compute actual memory address
            file.write(f"0x{addr:08X}:{self.memory[addr // 4]}\n")  # Get correct memory index
        
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
