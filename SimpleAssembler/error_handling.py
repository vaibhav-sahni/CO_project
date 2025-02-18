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
            if len(instruction) != 4:
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}") 
            if text[2] != ',' or text[4] != ',':
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            if text[-1] == ":":
                raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
            if len(text) != 6:
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            if instruction_type[text[0]] =="B" and (int(text[-1]) > 2047 or int(text[-1]) < -2048):
                raise SyntaxError(f"Immediate value out of range for {text[0]}: {text[-1]}")
            
        elif instruction_type[text[0]] == "I" or instruction_type[text[0]] == "S":
            if text[0] == 'addi' or text[0] == 'jalr':
                if text[2] != ',' or text[4] != ',':
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                if text[-1] == ":":
                    raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
                if len(text) != 6:
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                if int(text[5]) > 2047 or int(text[5]) < -2048:
                    raise SyntaxError(f"Immediate value out of range for {text[0]}: {text[5]}")

            elif text[0] in ['lw', 'sw']:
                if text[2] != ',' or text[4][0] != '(' or text[4][-1] != ')':
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                if text[-1] == ":":
                    raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
                if len(text) != 5:
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                try:
                    if int(text[3]) > 2047 or int(text[3]) < -2048:
                        raise SyntaxError(f"Immediate value out of range for {text[0]}: {text[3]}")
                except ValueError:
                    raise SyntaxError(f"Invalid immediate value for {text[0]}: {text[3]}")
                
        elif instruction_type[text[0]] == "J":
            if text[2] != ',':
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            if text[-1] == ":":
                raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
            if len(text) != 4:
                raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
            if int(text[3]) > 1048575 or int(text[3]) < -1048576:
                raise SyntaxError(f"Immediate value out of range for {text[0]}: {text[3]}")
            
        registers_list = list(registers.keys())
        reges = [i.strip('()') for i in instruction[1:] if i.isalnum() and not i.isdigit()]
        for reg in reges: 
            if reg not in registers_list:
                raise SyntaxError(f"Invalid register: {reg}")
            
    else:
        if text.count(":") != 1 or text[1] != ":":
            raise SyntaxError(f"Invalid label syntax {text[0]}: {assembly_text}")
        if text[0][0].isdigit():
            raise SyntaxError(f"Invalid label name {text[0]}: {assembly_text}")
        if text[0] in labels:
            raise SyntaxError(f"Duplicate label found: {text[0]}")

    return True 

def instriction_specific_errors(assembly_text,label):
    text = tokens(assembly_text)
    if ":" in text:
        text = text[text.index(":")+1:]
    if not label:
        if text[0] == "lw":
            if not text[3].isdigit():
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "addi":
            if not text[-1].isdigit():
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "jalr":
            if not text[-1].isdigit():
                raise SyntaxError(f"Invalid immediate value {text[0]}: {assembly_text}")
        if text[0] == "sw":
            if not text[3].isdigit():
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "beq" or text[0] == "bne":
            if not text[-1].isdigit():
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "jal":
            if not text[-1].isdigit():
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
    else:
        if text[0] == "lw":
            if text[3] not in label:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "addi":
            if text[-1] not in label:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "jalr":
            if text[-1] not in label:
                raise SyntaxError(f"Invalid immediate value {text[0]}: {assembly_text}")
        if text[0] == "sw":
            if text[3] not in label:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "beq" or text[0] == "bne":
            if text[-1] not in label:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "jal":
            if text[-1] not in label:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")

def check_valid_file(file_name):
    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_name}")
    file.close()
    return True

def error_handling(file_name,instructions):
    check_valid_file(file_name)
    for index, instruction in enumerate(instructions):
        try:
            check_syntax_errors(instruction, labels={})  # Empty labels for now, can be passed as needed
        except SyntaxError as e:
            print(f"Line {index + 1}: {e}")
            sys.exit(1)  # Stop execution on error


print(check_syntax_errors(['add','s2','s2','s3'], {},"add s2,s2,s3"))