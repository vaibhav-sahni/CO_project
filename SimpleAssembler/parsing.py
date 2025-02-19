#functions to parse instructions and return binary

from mappings import opcode,registers,funct3,funct7

def parse_R(inst,rd, rs1,rs2):
    # print(f'{funct7[inst]} ' + f'{registers[rs1]} ' + f'{registers[rs2]} ' + f'{funct3[inst]} ' + f'{registers[rd]} ' + f'{opcode[inst]} ')
    return funct7[inst] + registers[rs2] + registers[rs1] + funct3[inst] + registers[rd] + opcode[inst]
def parse_I(inst,rd,rs1,imm):
    imm_bin = format(int(imm) & 0xFFF, "012b") #formatting the imm value into 2's complement binary
    return imm_bin + registers[rs1] + funct3[inst] + registers[rd] + opcode[inst]

def parse_S(inst, data_register,imm,rs):
    imm_bin = format(int(imm) & 0xFFF, "012b")
    imm_1 = imm_bin[:7]
    imm_2 = imm_bin[7:]
    return imm_1 + registers[data_register] + registers[rs] + funct3[inst] + imm_2 + opcode[inst]

def parse_B(inst,rs1,rs2,imm):
    imm_bin = format(int(imm) & 0x1FFF, "013b")
    imm_parts = imm_bin[0] + imm_bin[2:8] + imm_bin[8:12] + imm_bin[1]
    return imm_parts[:7] + registers[rs2] + registers[rs1] + funct3[inst] + imm_parts[7:] + opcode[inst]

def parse_J(inst,rd,imm):
    imm_bin = format(int(imm) & 0x1FFFFF, "021b")
    imm_parts = imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9]
    return imm_parts + registers[rd] + opcode[inst]

