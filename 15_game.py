import time


def main(starting_nums='1,0,18,10,19,6', end=2020):
    starting_list = list(map(int, starting_nums.split(',')))

    num_pos_old = {}
    num_stream = []
    for turn, num in enumerate(starting_list, start=1):
        num_pos_old[num] = turn
        num_stream.append(num)
    
    num_stream.append(0)
    turn = len(num_stream)

    while turn < end:
        try:
            num_stream.append(len(num_stream) - num_pos_old[num_stream[-1]])
        except:
            num_stream.append(0)
        num_pos_old[num_stream[-2]] = len(num_stream) - 1
        turn = turn + 1
    print(num_stream[-1])


if __name__ == '__main__':
    start1 = time.time()
    # Test Cases
    # main('0,3,6')
    # main('1,3,2')
    # main('2,1,3')
    # main('1,2,3')
    # main('2,3,1')
    # main('3,2,1')
    # main('3,1,2')
    main()
    print(f'Part One finished in {time.time() - start1}')

    start2 = time.time()
    # Test Cases
    # main('0,3,6', end=30000000)
    # main('1,3,2', end=30000000)
    # main('2,1,3', end=30000000)
    # main('1,2,3', end=30000000)
    # main('2,3,1', end=30000000)
    # main('3,2,1', end=30000000)
    # main('3,1,2', end=30000000)
    main(end=30000000)
    # Runs in ~25 seconds
    print(f'Part Two finished in {time.time() - start2}')