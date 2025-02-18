#mappings for all instructions (funct7, funct3, opcode) and registers

funct7={ #only R type have a funct7
    'add': '0000000',
    'sub': '0100000',
    'slt': '0000000',
    'xor': '0000000',
    'srt': '0000000',
    'or': '0000000',
    'and': '0000000',
    'srl': '0000000',
    'sra': '0100000',
    'sll': '0000000',
}

funct3={
    #R type
    'add': '000',
    'sub': '000',
    'slt': '010',
    'srt': '101',
    'or': '110',
    'and': '111',
    'xor': '100',
    'srl': '101',
    'sra': '101',
    'sll': '001',
    
    #I type
    'lw': '010',
    'addi': '000',
    'jalr': '000',
    
    #S type
    'sw':'010',
    
    #B type
    'beq': '000',
    'bge': '101',
    'bne': '001',
    'blt': '100',
    'bltu': '110',
}
instruction_type={
    'add': 'R',
    'sub': 'R',
    'slt': 'R',
    'srt': 'R',
    'or': 'R',
    'and': 'R',
    'xor': 'R',
    'srl': 'R',
    'sra': 'R',
    'sll': 'R',
    'lw': 'I',
    'addi': 'I',
    'jalr': 'I',
    'sw':'S',
    'beq': 'B',
    'bge': 'B',
    'bne': 'B',
    'blt': 'B',
    'bltu':'B',
    'jal':'J',
}

opcode={
    #R type
    'add': '0110011',
    'sub': '0110011',
    'slt': '0110011',
    'srt': '0110011',
    'or': '0110011',
    'and': '0110011',
    'xor': '0110011',
    'srl': '0110011',
    'sra': '0110011',
    'sll': '0110011',
    #I type
    'lw': '0000011',
    'addi': '0010011',
    'jalr': '1100111',
    
    #S type
    'sw':'0100011',
    
    #B type
    'beq': '1100011',
    'bne': '1100011',
    'blt': '1100011',
    'bge': '1100011',
    'bltu': '1100011',
    
    #J type
    'jal':'1101111',
}

registers={
    'zero': '00000', #hard wired zero
    'ra': '00001',  #return address
    'sp': '00010',  #stack pointer
    'gp': '00011',
    'tp': '00100',
    't0': '00101',
    't1': '00110',
    't2': '00111',
    's0': '01000',
    'fp': '01000', #saved register/frame pointer
    's1': '01001',  #saved register
    'a0': '01010',
    'a1': '01011',
    'a2': '01100',
    'a3': '01101',
    'a4': '01110',
    'a5': '01111',
    'a6': '10000',
    'a7': '10001',
    's2': '10010',
    's3': '10011',
    's4': '10100',
    's5': '10101',
    's6': '10110',
    's7': '10111',
    's8': '11000',
    's9': '11001',
    's10': '11010',
    's11': '11011',
    't3': '11100',
    't4': '11101',
    't5': '11110',
    't6': '11111',
}

function_maping={
    
}