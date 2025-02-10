from mappings import instruction_type,opcode,registers,funct3,funct7
import sys
from parsing import parse_R,parse_I,parse_B,parse_J,parse_S
from error_handling import error_handling

def tokens(assembly_text):
    instructions=[]
    for line in assembly_text.split('\n'):
        if line:
            line=line.replace(',',' ') #replacing commas,brackets with spaces to split the line
            line=line.replace('(',' ')
            line=line.replace(':',': ')
            line=line.replace(':  ',': ')
            line=line.replace(')','')
            instructions.append(line.split(' '))
    print(instructions) #returning the list of instructions
    return instructions
def check_label(instruction,labels): #checking if the instruction is a new label and adding it to the labels dictionary with the program counter
    global program_counter
    if instruction[0].endswith(':'): #checking if the instruction is a label
        # print(instruction[0][:-1])
        labels[instruction[0][:-1]]=program_counter
        return True
    return False

def offset(instruction,labels,immediate): #calculating the offset for the branch instructions and returning the offset
    global program_counter
    if immediate in labels:
        offset=labels[immediate]-program_counter
        return offset
    return instruction[-1]

def main(open_file,write_file):
    global program_counter #global variable to store the program counter and to be used in other functions
    program_counter=0 #variable to store the program counter
    hault="" #variable to store the hault instruction
    labels=dict() #dictionary to store labels and their program counter

    # assembly_text=open(open_file).read()
    file=open(open_file,'r')
    assembly_text=file.read()

    binary_instructions=[]
    instructions=tokens(assembly_text) #tokenising the assembly text to get the instructions

    # for instruction in instructions: #checking for labels and adding them to the labels dictionary
    #     if check_label(instruction,labels):
    #         instruction.pop(0)
    #         if not instruction:
    #             instructions.remove(instruction)
    #     program_counter+=4

    error_handling(instructions)  # Calls the function that handles syntax errors and stops if there's an error
    
    for instruction in instructions:
        if check_label(instruction, labels):
            instruction.pop(0)
            if not instruction:
                instructions.remove(instruction)
        program_counter += 4

    program_counter=0
    # count = 1
    for instruction in instructions:
        if instruction==['beq','zero','zero','0']: #checking for the hault instruction
            labels['0']=program_counter
            hault=instruction
        if instruction[0] in instruction_type: #checking the instruction type and calling the respective function to parse the instruction
            
            # print(count,end=' ')
            # count+=1
            # print(instruction,end=' ')
            # print(instruction_type[instruction[0]])

            # calling for R type instructions
            instruct=instruction[0]
            if instruction_type[instruct]=='R':
                destination_register=instruction[1]
                source_register_1=instruction[2]
                source_register_2=instruction[3]
                binary_instructions.append(parse_R(instruct,destination_register,source_register_1,source_register_2))
            # calling for I type instructions
            elif instruction_type[instruct]=='I':
                if instruct=='lw':
                    destination_register=instruction[1]
                    source_register=instruction[3]
                    immediate=instruction[2]
                else:
                    destination_register=instruction[1]
                    source_register=instruction[2]
                    immediate=instruction[3]
                binary_instructions.append(parse_I(instruct,destination_register,source_register,immediate))
            # calling for S type instructions
            elif instruction_type[instruct]=='S':
                data_register=instruction[1]
                source_register=instruction[3]
                immediate=instruction[2]
                binary_instructions.append(parse_S(instruct,data_register,immediate,source_register))
            # calling for B type instructions
            elif instruction_type[instruct]=='B':
                source_register_1=instruction[1]
                source_register_2=instruction[2]
                immediate=instruction[3]
                if immediate.isdigit():
                    binary_instructions.append(parse_B(instruct,source_register_1,source_register_2,immediate))
                else:
                    immediate=offset(instruction,labels,immediate)
                    binary_instructions.append(parse_B(instruct,source_register_1,source_register_2,immediate))
            # calling for J type instructions
            elif instruction_type[instruct]=='J':
                destination_register=instruction[1]
                immediate=instruction[2]
                if immediate.isdigit():
                    binary_instructions.append(parse_J(instruct,destination_register,immediate))
                else:
                    immediate=offset(instruction,labels,immediate)
                    binary_instructions.append(parse_J(instruct,destination_register,immediate))
        program_counter+=4
    # if hault=="": #checking if the hault instruction is present
        # binary_instructions.append(parse_I('beq','zero','zero','0'))
    # print(binary_instructions)
    # print(instructions)
    # print(labels)

    file=open(write_file,'w')
    for instruction in binary_instructions:
        file.write(instruction+'\n')
    file.close()

read_file = sys.argv[1]
write_file = sys.argv[2]
main(read_file,write_file)

# # Program testing for the SimpleAssembler
# print("Testing the SimpleAssembler-0\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_0.txt")
# print()
# print("Testing the SimpleAssembler-1\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_1.txt")
# print()
# print("Testing the SimpleAssembler-2\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_2.txt")
# # print("Testing the SimpleAssembler\n")
# # main("automatedTesting/tests/assembly/simpleBin/Ex_test_3.txt")
# print()
# print("Testing the SimpleAssembler-4\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_4.txt")
# print()
# print("Testing the SimpleAssembler-5\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_5.txt")
# print()
# print("Testing the SimpleAssembler-6\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_6.txt")
# print()
# print("Testing the SimpleAssembler-7\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_7.txt")
# print()
# print("Testing the SimpleAssembler-8\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_8.txt")
# print()
# print("Testing the SimpleAssembler-9\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_9.txt")
# print()
# print("Testing the SimpleAssembler-10\n")
# main("automatedTesting/tests/assembly/simpleBin/Ex_test_10.txt")
# print()



