import sys
import re
from mappings import instruction_type, registers

# Error handling function for syntax errors
def check_syntax_errors(instruction, labels):
    # Check for invalid instruction mnemonics
    if instruction[0] not in instruction_type:
        raise SyntaxError(f"Invalid instruction: {instruction[0]}")

    # Check for wrong number of operands (should be 4 operands for most instructions)
    if len(instruction) < 4:
        raise SyntaxError(f"Missing operand(s) in instruction: {instruction}")
    elif len(instruction) > 4:
        raise SyntaxError(f"Extra operand(s) in instruction: {instruction}")

    # Check for invalid register name (invalid or out of range for RV32I)
    registers_list = list(registers.keys())
    for reg in instruction[1:]:  # Check registers in the operands (ignoring instruction mnemonic)
        if reg not in registers_list:
            raise SyntaxError(f"Invalid register: {reg}")

    # Check for invalid immediate values (for I and S types)
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

    # Check label formatting error
    if instruction[0].endswith(":"):  # Checking if instruction contains a label
        label = instruction[0][:-1]
        if label[0].isdigit():  # Label cannot start with a number
            raise SyntaxError(f"Label cannot start with a number: {label}")
        if label != label.lower():  # Labels are case-sensitive
            raise SyntaxError(f"Case-sensitive error with label: {label}")

    # Check for unexpected tokens (extra symbols, missing commas, invalid characters)
    if not re.match(r"^[a-zA-Z0-9_,()\s]+$", ' '.join(instruction)):
        raise SyntaxError(f"Unexpected tokens in instruction: {instruction}")

    return True  # If no errors, return True indicating valid syntax

# Function to check if an instruction has syntax errors (alternative method)
def syntax_error(instruction):
    if not instruction:
        return "Error: Empty instruction found."
    
    opcode = instruction[0]
    if opcode not in instruction_type:
        return f"Error: Unsupported instruction '{opcode}'."
    
    instr_type = instruction_type[opcode]
    num_operands = len(instruction) - 1
    
    # Expected operand count for each type
    expected_operands = {
        'R': 3, 'I': 3, 'S': 3, 'B': 3, 'J': 2
    }
    
    if instr_type in expected_operands and num_operands != expected_operands[instr_type]:
        return f"Error: Incorrect number of operands for {instr_type}-type instruction '{' '.join(instruction)}'. Expected {expected_operands[instr_type]}, got {num_operands}."
    
    # Check register validity (except for labels)
    for operand in instruction[1:]:
        if operand.startswith('x') and operand not in registers:
            return f"Error: Invalid register '{operand}' in instruction '{' '.join(instruction)}'."
    
    return None  # No errors

# Main error handling function to iterate over instructions
def error_handling(instructions):
    # Iterate over all instructions and check for syntax errors
    for index, instruction in enumerate(instructions):
        try:
            check_syntax_errors(instruction, labels={})  # Empty labels for now, can be passed as needed
        except SyntaxError as e:
            print(f"Line {index + 1}: {e}")
            sys.exit(1)  # Stop execution on error


