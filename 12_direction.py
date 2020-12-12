import time
import itertools
import re
import numpy as np

DIRECTIONS_CL = itertools.cycle('NESW')
DIRECTIONS_CCL = itertools.cycle('WSEN')
def change_dir(present_direction, instruction):
        
    degrees = int(instruction[1:])
    turns = int(degrees / 90)
    if instruction[0] == 'R':
    # Get iteration to present directions
        direction = next(DIRECTIONS_CL)
        while direction != present_direction:
            direction = next(DIRECTIONS_CL)
        # Rotate to new direction
        for _ in range(turns):
            direction = next(DIRECTIONS_CL)
    elif instruction[0] == 'L':
        direction = next(DIRECTIONS_CCL)
        while direction != present_direction:
            direction = next(DIRECTIONS_CCL)
        # Rotate to new direction
        for _ in range(turns):
            direction = next(DIRECTIONS_CCL)
    
    return direction


def remove_f_directions(list_of_directions):
    facing_dir = 'E'
    clean_directions = []
    for direction in list_of_directions:
        clean_dir = None
        word = direction[0]
        qty = direction[1:]
        if word == 'F':
            clean_dir = facing_dir
            clean_dir = clean_dir + qty
        elif word in ['L', 'R']:
            facing_dir = change_dir(facing_dir, direction)
            continue 
        else:
            clean_dir = word + qty
        # print(clean_dir)
        clean_directions.append(clean_dir)
    return clean_directions    


def negative_directions(list_of_directions):
    list_of_directions = list(map(str.replace, list_of_directions, itertools.repeat('S'), itertools.repeat('N-')))

    list_of_directions = list(map(str.replace, list_of_directions, itertools.repeat('W'), itertools.repeat('E-')))
    return list_of_directions


def count_directions(list_of_directions):
    list_of_directions = np.array(list_of_directions)
    north_directions = list_of_directions[np.char.startswith(list_of_directions, 'N')]
    north_directions = np.char.strip(north_directions, 'N')
    n_sum = np.abs(north_directions.astype('int').sum())

    east_directions = list_of_directions[np.char.startswith(list_of_directions, 'E')]
    east_directions = np.char.strip(east_directions, 'E')
    e_sum = np.abs(east_directions.astype('int').sum())

    return n_sum, e_sum

def main1(input_dir):
    directions = remove_f_directions(input_dir)
    # Replace S with neg N and W with neg E
    directions = negative_directions(directions)
    n_sum, e_sum = count_directions(directions)
    print(n_sum + e_sum)


def main2(input_dir):
    # Make directions N- and E-
    directions = negative_directions(input_dir)
    # Starting Waypoint
    dir_1 = 'E'
    dir_2 = 'N'
    waypoint_dir_1 = 10
    waypoint_dir_2 = 1

    ship_E = 0
    ship_N = 0

    for direction in directions:
        word = direction[0]
        qty = int(direction[1:])
        if word == 'F':
            ship_E = ship_E + waypoint_dir_1 * qty
            ship_N = ship_N + waypoint_dir_2 * qty
        elif word == 'N':
            waypoint_dir_2 = waypoint_dir_2 + qty
        elif word == 'E':
            waypoint_dir_1 = waypoint_dir_1 + qty
        elif word in ['L', 'R']:
            # print(dir_1, dir_2)
            new_dir_1 = change_dir('E', direction)
            new_dir_2 = change_dir('N', direction)
            # print(new_dir_1, new_dir_2)
            # print(dir_1, dir_2)
            if new_dir_1 in ['N', 'S']:
                dir_1 = new_dir_2
                dir_2 = new_dir_1
                waypoint_dir_1, waypoint_dir_2 = waypoint_dir_2, waypoint_dir_1
            if dir_1 == 'W' or new_dir_1 == 'W':
                dir_1 = 'E'
                waypoint_dir_1 = -1 * waypoint_dir_1
            if dir_2 == 'S' or new_dir_2 == 'S':
                dir_2 = 'N'
                waypoint_dir_2 = -1 * waypoint_dir_2
            # print(dir_1, dir_2)
        # print(direction)
        # print(waypoint_dir_1, waypoint_dir_2)
        # print(ship_E, ship_N)
        # input()
    print(np.abs(ship_E) + np.abs(ship_N))


def read_file():
    file_name = 'Day_12/12_test.txt'
    file_name = 'Day_12/12_input.txt'
    with open(file_name, 'r') as f:
        directions = list(map(str.strip, f.readlines()))
    return directions


if __name__ == '__main__':
    start = time.time()
    input_dir = read_file()
    main1(input_dir)
    print(f'Finished in {time.time() - start}')
    # Part Two
    start = time.time()
    main2(input_dir)
    print(f'Finished in {time.time() - start}')