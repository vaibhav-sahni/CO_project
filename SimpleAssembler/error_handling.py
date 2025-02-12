import sys
import re
from mappings import instruction_type, registers

def tokens(assembly_text):
    for line in assembly_text.split('\n'):
        tokens = re.findall(r'\w+\[.*?\]|\w+|\(.*?\)|[^\w\s]', line)
    return tokens

def check_syntax_errors(instruction, labels,assembly_text):
    text = tokens(assembly_text)
    if text[0] in instruction_type:
        if instruction_type[text[0]] == "R" or instruction_type[text[0]] == "B":
            if text[2] != ',' or text[4] != ',':
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            if text[-1] == ":":
                raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
            if len(text) != 6:
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            
        elif instruction_type[text[0]] == "I" or instruction_type[text[0]] == "S":
            if text[0] == 'addi':
                if text[2] != ',' or text[4] != ',':
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                if text[-1] == ":":
                    raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
                if len(text) != 6:
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            elif text[0] in ['lw', 'sw']:
                if text[2] != ',' or text[4][0] != '(' or text[4][-1] != ')':
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                if text[-1] == ":":
                    raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
                if len(text) != 5:
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                
        elif instruction_type[text[0]] == "J":
            if text[2] != ',':
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            if text[-1] == ":":
                raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
            if len(text) != 4:
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            
        registers_list = list(registers.keys())
        for reg in instruction[1:]: 
            if reg not in registers_list:
                raise SyntaxError(f"Invalid register: {reg}")
            
    else:
        if text.count(":") != 1 or text[1] != ":":
            raise SyntaxError(f"Invalid label syntax {text[0]}: {assembly_text}")
        if text[0][0].isdigit():
            raise SyntaxError(f"Invalid label name {text[0]}: {assembly_text}")

    if instruction[0] in ['addi', 'lw', 'sw', 'beq']:
        try:
            # Check if immediate is a number and validate size (12-bit immediate for RV32I)
            if instruction[2].lstrip('-').isdigit():
                immediate = int(instruction[2])
                if instruction[0] == 'addi' and not (-2048 <= immediate <= 2047):
                    raise SyntaxError(f"Immediate value out of range for {instruction[0]}: {instruction[2]}")
                elif instruction[0] in ['sw', 'lw'] and not (-2048 <= immediate <= 2047):
                    raise SyntaxError(f"Immediate value out of range for {instruction[0]}: {instruction[2]}")
        except ValueError:
            raise SyntaxError(f"Invalid immediate value: {instruction[2]}")

    return True 

def error_handling(instructions):
    for index, instruction in enumerate(instructions):
        try:
            check_syntax_errors(instruction, labels={})  # Empty labels for now, can be passed as needed
        except SyntaxError as e:
            print(f"Line {index + 1}: {e}")
            sys.exit(1)  # Stop execution on error


print(check_syntax_errors(['label','add', 'ra', 'sp', 'gp'], {},"4label:add ra, sp, gp"))