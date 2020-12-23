import time
import itertools
from collections import deque


def find_destination_index(current_cup, pick_up_cups, cups_list, part=1):
    destination = current_cup - 1
    while True:
        if destination == 0:
            destination = 9 
        if destination not in pick_up_cups:
            break
        else:
            destination = destination - 1
        
    dest_idx = cups_list.index(destination) + 1
    return dest_idx


def calculate_final_state(cups_list):
    iterator = itertools.cycle(cups_list)
    ele = next(iterator)
    while ele != 1:
        ele = next(iterator)
    
    ele = next(iterator)
    final_str = ''
    while ele != 1:
        final_str += str(ele)
        ele = next(iterator)

    return final_str


def main(inp_dat='156794823', moves=100, part=1):
    cups_list = deque(map(int, list(inp_dat)))
    move = 0

    while move != moves:
        move += 1 
        # print(f'-- Move {move} --')
        current_cup = cups_list.popleft()
        # print(f'Cups: ({current_cup}) {" ".join([str(x) for x in cups_list])}')
        pick_up_cups = []
        for _ in range(3):
            pick_up_cups.append(cups_list.popleft())
        # print(f'Pick Up: {", ".join([str(x) for x in pick_up_cups])}')
        insert_index = find_destination_index(current_cup, pick_up_cups, cups_list, part=part)
        # print(f'Destination: {cups_list[insert_index-1]}')
        # print(f'Destination Idx: {insert_index}')
        cups_list.insert(insert_index, pick_up_cups[0])
        cups_list.insert(insert_index+1, pick_up_cups[1])
        cups_list.insert(insert_index+2, pick_up_cups[2])
        cups_list.append(current_cup)

    ans = calculate_final_state(cups_list)
    print(ans)
    return cups_list


def main2(inp_data='156794823', moves=10000000):
    inp_data = list(map(int, list(inp_data)))
    max_val = max(inp_data)
    for i in range(max_val+1, 1000001):
        inp_data.append(i)
    final_state = main(inp_dat=inp_data, moves=moves, part=2)
    idx_one = final_state.index(1)
    num1 = final_state[idx_one+1]
    num2 = final_state[idx_one+2]
    print(num1, num2)
    print(num1*num2)


def testcase():
    main(inp_dat='389125467', moves=10, part=1) # Test Data
    main(inp_dat='389125467', moves=100, part=1) # Test Data


def testcase2():
    # main2(inp_data='389125467', moves=10)
    # main2(inp_data='389125467', moves=100)
    # main2(inp_data='389125467', moves=1000)
    # main2(inp_data='389125467', moves=10000)
    # main2(inp_data='389125467', moves=100000)
    main2(inp_data='389125467', moves=1000000)
    # main2(inp_data='389125467')


if __name__ == '__main__':
    start1 = time.time()
    testcase()
    main(part=1)
    print(f'Part One finished in {time.time()-start1}')

    start2 = time.time()
    # testcase2()
    # main2()
    print(f'Part Two finished in {time.time()-start2}')