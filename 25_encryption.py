import time


def find_loop_size(key_num, sbj_num=7):
    value = 1
    loop_count = 0
    while value != key_num:
        value = value * sbj_num
        value = value % 20201227
        loop_count += 1 
    return loop_count


def find_encryption_key(public_key, loop_size):
    val = 1
    for _ in range(loop_size):
        val = val * public_key
        val = val % 20201227

    return val

def main(inp_data=[335121, 363891]):
    loop1 = find_loop_size(inp_data[0])
    loop2 = find_loop_size(inp_data[1])
    print(find_encryption_key(inp_data[1], loop1))
    print(find_encryption_key(inp_data[0], loop2))

if __name__ == '__main__':
    start1 = time.time()
    main(inp_data=[5764801, 17807724]) # Test Case
    # main()
    print(f'Part One finished in {time.time() - start1}')