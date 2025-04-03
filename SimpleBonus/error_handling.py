import sys
import re
from mappings import instruction_type, registers

def tokenization(assembly_text):
    tokens = []
    for line in assembly_text.split('\n'):
        tokenization = re.findall(r'\w+-\w+|\w+\[.*?\]|\w+|\(.*?\)|[^\w\s]', line)
        tokens.extend(tokenization)

    for i in range(len(tokens)-1):
        if tokens[i] == "-":
            tokens[i] = tokens[i] + tokens[i+1]
            tokens.pop(i+1)
    return tokens

def check_syntax_errors(instruction, labels,assembly_text):
    text = tokenization(assembly_text)
    if len(assembly_text) == 0:
        return True
    else:
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
                if instruction_type[text[0]] =="B":
                    if text[-1] not in labels and text[-1].isnumeric() == False:
                        raise SyntaxError(f"Invalid label found: {text[-1]}")
                    elif text[-1].isnumeric() and (int(text[-1]) > 2047 or int(text[-1]) < -2048):
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
                    
            elif instruction_type[text[0]] == "J":
                if text[2] != ',':
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                if text[-1] == ":":
                    raise SyntaxError(f"Invalid label location {text[0]}: {assembly_text}")
                if len(text) != 4:
                    raise SyntaxError(f"Invalid syntax for {text[0]}: {assembly_text}")
                
            if instruction_type[text[0]] == "R":
                if instruction[1] not in registers:
                    raise SyntaxError(f"Invalid register name {text[1]}: {assembly_text}")
                if instruction[2] not in registers:
                    raise SyntaxError(f"Invalid register name {text[2]}: {assembly_text}")
                if instruction[3] not in registers:
                    raise SyntaxError(f"Invalid register name {text[3]}: {assembly_text}")
            
            if instruction_type[text[0]] == "B":
                if instruction[1] not in registers:
                    raise SyntaxError(f"Invalid register name {text[1]}: {assembly_text}")
                if instruction[2] not in registers:
                    raise SyntaxError(f"Invalid register name {text[2]}: {assembly_text}")
                
            if instruction_type[text[0]] == "J":
                if instruction[1] not in registers:
                    raise SyntaxError(f"Invalid register name {text[1]}: {assembly_text}")
            
            if text[0] == "jalr":
                if instruction[1] not in registers:
                    raise SyntaxError(f"Invalid register name {text[1]}: {assembly_text}")
                if instruction[2] not in registers:
                    raise SyntaxError(f"Invalid register name {text[3]}: {assembly_text}")
                
            if text[0] == 'lw':
                if text[1] not in registers:
                    raise SyntaxError(f"Invalid register name {text[1]}: {assembly_text}")
                if text[4].strip("()") not in registers:
                    raise SyntaxError(f"Invalid register name {text[4]}: {assembly_text}")
            if text[0] == 'addi':
                if text[1] not in registers:
                    raise SyntaxError(f"Invalid register name {text[1]}: {assembly_text}")
                if text[3] not in registers:
                    raise SyntaxError(f"Invalid register name {text[3]}: {assembly_text}")
                
        else:
            if text.count(":") != 1 or text[1] != ":":
                raise SyntaxError(f"Invalid label syntax {text[0]}: {assembly_text}")
            if text[0][0].isdigit():
                raise SyntaxError(f"Invalid label name {text[0]}: {assembly_text}")
        return True 

def instructionSpecificError(assembly_text,label):
    text = tokenization(assembly_text)
    if ":" in text:
        text = text[text.index(":")+1:]
    if text[-1] not in label:
        if text[0] == "lw":
            try:
                if not int(text[3]) >= -2048 and int(text[3]) <= 2047:
                    raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
            except ValueError:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "addi":
            try:
                if not int(text[-1]) >= -2048 and int(text[-1]) <= 2047:
                    raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
            except ValueError:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "jalr":
            try:
                if not int(text[-1])>=-2048 and int(text[-1])<=2047:
                    raise SyntaxError(f"Invalid immediate value {text[0]}: {assembly_text}")
            except ValueError:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "sw":
            try:
                if not int(text[3]) >= -2048 and int(text[3]) <= 2047:
                    raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
            except ValueError:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "beq" or text[0] == "bne":
            try:
                if not int(text[-1]) >= -2048 and int(text[-1]) <= 2047:
                    raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
            except ValueError:
                raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
        if text[0] == "jal":
            try:
                if not int(text[-1]) >= -1048576 and int(text[-1]) <= 1048575:
                    raise SyntaxError(f"Invalid immediate value found {text[0]}: {assembly_text}")
            except ValueError:
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

def check_virtual_halt(file_name):
    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_name}")
    assembly_text = file.read()
    text = tokenization(assembly_text)
    if text[-1] != "hlt":
        raise SyntaxError(f"Missing halt instruction")
    file.close()
    return True