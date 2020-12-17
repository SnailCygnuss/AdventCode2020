import numpy as np
import itertools
import time


def get_neigbours(infinite_array):
    # Compute coordinates of neighbours for each element
    neighbours = []
    z_limit, x_limit, y_limit = infinite_array.shape
    for z, x, y in itertools.product(range(1, z_limit - 1), 
                                     range(1, x_limit - 1),
                                     range(1, y_limit - 1)):
        # n_list = [(z - a, x - b, y - c) for a, b, c in itertools.product([-1, 0, 1], repeat=3)]
        z_list = np.array([z - a for a, b, c in itertools.product([-1, 0, 1], repeat=3) if not a == b == c == 0], dtype='B')
        x_list = np.array([x - b for a, b, c in itertools.product([-1, 0, 1], repeat=3) if not a == b == c == 0], dtype='B')
        y_list = np.array([y - c for a, b, c in itertools.product([-1, 0, 1], repeat=3) if not a == b == c == 0], dtype='B')
        # n_list.remove((z, x, y))
        # print(len(n_list))
        # print(z_list)
        # print(x_list)
        # print(y_list)
        neighbours.append((z_list, x_list, y_list))
        # print(neighbours)
        # input()
    return neighbours


def get_active_neighbours(infinite_array, neigbour_coords):
    active_neighbours_count = np.zeros((infinite_array.shape), dtype='b')
    z_l , x_l, y_l = infinite_array.shape

    for (z, x, y), n_coords in zip(itertools.product(range(1, z_l-1),
                                                     range(1, x_l-1),
                                                     range(1, y_l-1)),
                                                     neigbour_coords):
        active_neighbours_count[z, x, y] = infinite_array[n_coords].sum()

    return active_neighbours_count


def switch_neighbours(infinite_array, active_neighbours_count):
    
    return_array = infinite_array.copy()

    active = infinite_array == 1
    n_2 = active_neighbours_count == 2
    n_3 = active_neighbours_count == 3
    to_be_active = np.logical_and(active, np.logical_or(n_2, n_3))
    to_be_inactive = ~to_be_active
    return_array[to_be_active] = 1
    return_array[to_be_inactive] = 0

    inactive = ~active
    to_be_active_2 = np.logical_and(inactive, n_3)
    return_array[to_be_active_2] = 1

    # Make edges 0
    z_limit, x_limit, y_limit = infinite_array.shape
    return_array[0, :, :] = 0
    return_array[z_limit-1, :, :] = 0
    
    return_array[:, 0, :] = 0
    return_array[:, x_limit-1, :] = 0
    
    return_array[:, :, 0] = 0
    return_array[:, :, y_limit-1] = 0
    
    # print(active_neighbours_count)
    # print(return_array)
    # input()
    return return_array


def main(file_name='Day_17/17_input.txt'):
    ARRAY_LEN = 250
    with open(file_name, 'r') as f:
        input_data = list(map(str.strip, f.readlines()))
        input_data = [x.replace('.', '0') for x in input_data]
        input_data = [x.replace('#', '1') for x in input_data]
        input_data = [list(x) for x in input_data]
    
    input_data = np.array(input_data)
    infinite_array = np.zeros((ARRAY_LEN, ARRAY_LEN, ARRAY_LEN), dtype='B')
    starting_point = (ARRAY_LEN // 2) - (input_data.shape[0] // 2)
    for x, y in itertools.product(range(3), repeat=2):
        infinite_array[ARRAY_LEN // 2, starting_point+x, starting_point+y] = input_data[x, y].copy()
    # print(infinite_array[0, starting_point: starting_point+5, starting_point: starting_point+5])
    neigbour_coords = get_neigbours(infinite_array)
    
    new_array = infinite_array.copy()
    for i in range(6):
        active_neighbours_count = get_active_neighbours(new_array, neigbour_coords)
        new_array = switch_neighbours(new_array, active_neighbours_count)
        print('Cycle', i)

    print(new_array.sum())


if __name__ == '__main__':
    start1 = time.time()
    # main(file_name='Day_17/17_test.txt')
    main()
    print(f'Part One completed in {time.time() - start1}')
