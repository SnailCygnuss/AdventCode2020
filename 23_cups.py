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


def main2(inp_data='156794823', moves=10_000_000):
    inp_data = list(map(int, list(inp_data)))
    max_val = max(inp_data)
    for i in range(max_val+1, 1000001):
        inp_data.append(i)
    
    next_data = {}
    for num, nxt in zip(inp_data, inp_data[1:]):
        next_data[num] = nxt
    # Assign the last num to first
    next_data[inp_data[-1]] = inp_data[0]
    
    first = inp_data[0]
    for _ in range(moves):
        next1 = next_data[first]
        next2 = next_data[next1]
        next3 = next_data[next2]
        next4 = next_data[next3]
        insert_idx = first - 1
        while True:
            if insert_idx == 0:
                insert_idx = 1000000
            if insert_idx not in [next1, next2, next3]:
                break
            else:
                insert_idx = insert_idx - 1
        # Insert Data
        prev_next = next_data[insert_idx]
        next_data[insert_idx] = next1
        next_data[next3] = prev_next
       # input()
        # Get the next element
        next_data[first] = next4
        first = next4
        
    num1 = next_data[1]
    num2 = next_data[num1]
    print(num1, num2)
    print(num1*num2)


def testcase():
    main(inp_dat='389125467', moves=10, part=1) # Test Data
    main(inp_dat='389125467', moves=100, part=1) # Test Data


def testcase2():
    main2(inp_data='389125467', moves=1000000)
    main2(inp_data='389125467')


if __name__ == '__main__':
    start1 = time.time()
    # testcase()
    # main(part=1)
    print(f'Part One finished in {time.time()-start1}')

    start2 = time.time()
    # testcase2()
    main2()
    print(f'Part Two finished in {time.time()-start2}')