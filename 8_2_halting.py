def check_loop(instructions_list):
    acc = 0
    line = 0
    transversed_line = []
    infinite_loop = False
    instructions_list_len = len(instructions_list)
    while True:
        if line >= instructions_list_len:
            break
        cmd, number = instructions_list[line].strip().split()
        if line in transversed_line:
            infinite_loop = True
            break
        transversed_line.append(line)
        if cmd == 'nop':
            line = line + 1
        elif cmd == 'acc':
            acc = acc + int(number)
            line = line + 1
        elif cmd == 'jmp':
            line = line + int(number)

    return infinite_loop, acc


def main():
    file_name = 'Day_8/8_test.txt'
    file_name = 'Day_8/8_input.txt'

    with open(file_name, 'r') as f:
        instructions = f.readlines()
    
    is_loop = True
    acc_val = 0
    for line_no, instruction in enumerate(instructions):
        cmd, _ = instruction.strip().split()
        if cmd == 'nop':
            new_instructions = instructions.copy()
            new_instructions[line_no] = new_instructions[line_no].replace('nop', 'jmp')
            is_loop, acc_val = check_loop(new_instructions)
        elif cmd == 'jmp':
            new_instructions = instructions.copy()
            new_instructions[line_no] = new_instructions[line_no].replace('jmp', 'nop')
            is_loop, acc_val = check_loop(new_instructions)
        if not is_loop:
            changed_line = line_no
            break
    
    print(acc_val, changed_line)


if __name__ == '__main__':
    main()
