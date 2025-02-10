import sys
from mappings import instruction_type, registers

def syntax_error(instruction):
    #Checks for syntax errors in an instruction.

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

def error_handling(instructions):
  
   # Iterates over all instructions and checks for syntax errors.
    
    for index, instruction in enumerate(instructions):
        error = syntax_error(instruction)
        if error:
            print(f"Line {index + 1}: {error}")
            sys.exit(1)  # Stop execution on error

