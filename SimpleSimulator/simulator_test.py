"""
First we have to check the opcode and determine what type of instruction it is.
After we know that, we know the format its in, and have to reverse engineer it from parsing.py
"""
class RISC_V_Simulator:
    def __init__(self):
        self.registers = [0] * 32  # 32 general-purpose registers
        self.memory = [0] * 32  # 32 words (each 32-bit)
        self.pc = 0  # Program counter
        self.halted = False
        self.output_file = "output.txt"

    def load_binary(self, filename):
        with open(filename, "r") as f:
            self.instructions = [line.strip() for line in f.readlines()]

    def execute(self):
        with open(self.output_file, "w") as out:
            while not self.halted and self.pc < len(self.instructions):
                instruction = self.instructions[self.pc]
                self.log(f"Executing PC={self.pc * 4}: {instruction}")

                if instruction == "00000000000000000000000001100011":  # Virtual halt (beq x0, x0, 0)
                    self.halted = True
                    self.log("Virtual halt encountered. Dumping memory...")
                    break

                self.decode_and_execute(instruction)
                self.pc += 1  # Increment PC
                self.dump_registers(out)

            self.dump_memory(out)

    def decode_and_execute(self, instruction):
        opcode = instruction[-7:]  # Last 7 bits for opcode
        if opcode == "0110011":  # R-type (add, sub, and, or, xor, sll, srl, sra, slt)
            self.execute_r_type(instruction)
        elif opcode == "0000011":  # lw (load word)
            self.execute_lw(instruction)
        elif opcode == "0100011":  # sw (store word)
            self.execute_sw(instruction)
        elif opcode == "1100011":  # Branch instructions (beq, bne, blt, bge)
            self.execute_branch(instruction)
        elif opcode == "1101111":  # jal
            self.execute_jal(instruction)
        elif opcode == "1100111":  # jalr
            self.execute_jalr(instruction)
        elif opcode == "0010011":  # addi
            self.execute_addi(instruction)
        else:
            self.log(f"Unknown instruction: {instruction}")

    def execute_r_type(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        funct3 = instruction[17:20]
        funct7 = instruction[:7]

        if funct3 == "000" and funct7 == "0000000":  # ADD
            self.registers[rd] = self.registers[rs1] + self.registers[rs2]
            self.log(f"ADD x{rd} = x{rs1} + x{rs2} -> {self.registers[rd]}")
        elif funct3 == "000" and funct7 == "0100000":  # SUB
            self.registers[rd] = self.registers[rs1] - self.registers[rs2]
            self.log(f"SUB x{rd} = x{rs1} - x{rs2} -> {self.registers[rd]}")
        else:
            self.log(f"Unsupported R-type instruction: {instruction}")

    def execute_lw(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        imm = int(instruction[:12], 2)
        address = (self.registers[rs1] + imm) // 4
        self.registers[rd] = self.memory[address]
        self.log(f"LW x{rd} = MEM[{address}] -> {self.registers[rd]}")

    def execute_sw(self, instruction):
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        imm = int(instruction[:7] + instruction[20:25], 2)
        address = (self.registers[rs1] + imm) // 4
        self.memory[address] = self.registers[rs2]
        self.log(f"SW MEM[{address}] = x{rs2} -> {self.memory[address]}")

    def execute_branch(self, instruction):
        rs1 = int(instruction[12:17], 2)
        rs2 = int(instruction[7:12], 2)
        imm = int(instruction[:7] + instruction[20:25], 2)

        if instruction[17:20] == "000":  # BEQ
            if self.registers[rs1] == self.registers[rs2]:
                self.pc += imm - 1  # Adjust PC
                self.log(f"BEQ x{rs1} == x{rs2}, PC -> {self.pc * 4}")

    def execute_jal(self, instruction):
        rd = int(instruction[20:25], 2)
        imm = int(instruction[:20], 2)
        self.registers[rd] = self.pc * 4 + 4
        self.pc += imm - 1
        self.log(f"JAL x{rd} = {self.registers[rd]}, PC -> {self.pc * 4}")

    def execute_jalr(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        imm = int(instruction[:12], 2)
        self.registers[rd] = self.pc * 4 + 4
        self.pc = (self.registers[rs1] + imm) // 4 - 1
        self.log(f"JALR x{rd} = {self.registers[rd]}, PC -> {self.pc * 4}")

    def execute_addi(self, instruction):
        rd = int(instruction[20:25], 2)
        rs1 = int(instruction[12:17], 2)
        imm = int(instruction[:12], 2)
        self.registers[rd] = self.registers[rs1] + imm
        self.log(f"ADDI x{rd} = x{rs1} + {imm} -> {self.registers[rd]}")

    def dump_registers(self, file):
        file.write(f"{self.pc * 4} " + " ".join(map(str, self.registers)) + "\n")

    def dump_memory(self, file):
        for i in range(32):
            addr = f"0x{(i * 4):08X}"
            file.write(f"{addr}:{bin(self.memory[i])}\n")

    def log(self, message):
        print(message)

# Running the simulator
sim = RISC_V_Simulator()
sim.load_binary("binary_code.txt")
sim.execute()
