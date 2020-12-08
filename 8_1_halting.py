def main():
    file_name = 'Day_8/8_test.txt'
    file_name = 'Day_8/8_input.txt'

    with open(file_name, 'r') as f:
        instructions = f.readlines()

    acc = 0
    line = 0
    transversed_line = []
    while True:
        cmd, number = instructions[line].strip().split()
        if line in transversed_line:
            break
        transversed_line.append(line)
        if cmd == 'nop':
            line = line + 1
        elif cmd == 'acc':
            acc = acc + int(number)
            line = line + 1
        elif cmd == 'jmp':
            line = line + int(number)

    print(acc)


if __name__ == '__main__':
    main()
