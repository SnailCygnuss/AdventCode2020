import time
import itertools


def mask_char(mask_char, text_char):
    # Compare each char
    if mask_char == 'X':
        return text_char
    else:
        return mask_char


def mask_function(mask, text):
    return ''.join(list(map(mask_char, iter(mask), iter(text))))


def main():
    file_name = 'Day_14/14_test.txt'
    file_name = 'Day_14/14_input.txt'

    mem = {}
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('mask'):
                mask = line.strip().split()[2]
            else:
                addr, _, text = line.strip().split()
                addr_loc = int(addr.split('[')[1][:-1])
                text = format(int(text), '036b')
                mem[addr_loc] = mask_function(mask, text)
    
    sum_addr = sum([int(x, 2) for x in mem.values()])
    print(sum_addr)


def mask_char2(mask_char, text_char):
    if mask_char == '0':
        return text_char
    elif mask_char == '1':
        return '1'
    elif mask_char == 'X':
        return 'X'


def mask_function2(mask, text):
    masked_address = list(map(mask_char2, iter(mask), iter(text)))
    floats = masked_address.count('X')
    new_addresses = []
    for x_replace in itertools.product('01', repeat=floats):
        masked_address1 = ''.join(masked_address)
        for val in x_replace:
            masked_address1 = masked_address1.replace('X', val, 1)
        new_addresses.append(int(masked_address1, 2))
    return new_addresses


def main2():
    file_name = 'Day_14/14_test2.txt'
    file_name = 'Day_14/14_input.txt'

    mem = {}
    with open(file_name, 'r') as f:
        for line in f:
            if line.startswith('mask'):
                mask = line.strip().split()[2]
            else:
                addr, _, value = line.strip().split()
                addr_loc = int(addr.split('[')[1][:-1])
                text = format(int(addr_loc), '036b')
                value = int(value)
                addr_locs = mask_function2(mask, text)
                mem.update((zip(addr_locs, itertools.repeat(value))))
    print(sum(mem.values()))


if __name__ == '__main__':
    start1 = time.time()
    main()
    print(f'Part One finished in {time.time() - start1}')

    start2 = time.time()
    main2()
    print(f'Part Two finished in {time.time() - start2}')