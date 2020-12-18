import itertools
import time


def get_sorrounding_elems(input_dim, d=3):
    x = (input_dim[0][0] - 1, input_dim[0][1] + 1)
    y = (input_dim[1][0] - 1, input_dim[1][1] + 1)
    z = (input_dim[2][0] - 1, input_dim[2][1] + 1)
    if d == 4:
        w = (input_dim[3][0] - 1, input_dim[3][1] + 1)
        return [x, y, z, w]
    return [x, y, z]


def get_neighbour_sum(coords, active_states, d=3):
    neighbour_sum = 0
    if d == 3:
        for a, b, c in itertools.product([-1, 0, 1], repeat=3):
            if a == b == c == 0:
                continue
            x = coords[0] - a
            y = coords[1] - b
            z = coords[2] - c
            if (x, y, z) in active_states:
                neighbour_sum = neighbour_sum + 1
        return neighbour_sum
    elif d == 4:
        for a, b, c, d in itertools.product([-1, 0, 1], repeat=4):
            if a == b == c == d == 0:
                continue
            x = coords[0] - a
            y = coords[1] - b
            z = coords[2] - c
            w = coords[3] - d
            if (x, y, z, w) in active_states:
                neighbour_sum = neighbour_sum + 1
        return neighbour_sum


def print_cubes(dims, active_states):
    for z in range(dims[2][0], dims[2][1]):
        print(f'z = {z}') 
        for y in range(dims[1][0], dims[1][1]):
            for x in range(dims[0][0], dims[0][1]):
                if (x, y, z) in active_states:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print()
        

def main2(file_name='Day_17/17_input.txt'):
    with open(file_name, 'r') as f:
        input_slice = list(map(str.strip, f.readlines()))
    input_dim = len(input_slice)

    active_states = []
    for x, y, z in itertools.product(range(input_dim), range(input_dim), 
                                     range(1)):
        if input_slice[y][x] == '#':
            active_states.append((x, y, z))

    dims = [(0, input_dim), (0, input_dim), (0, 1)]
    
    for i in range(6):
        print(f'Iteration {i+1}')
        new_active_states = []
        dims = get_sorrounding_elems(dims)
        for x, y, z in itertools.product(range(dims[0][0], dims[0][1]),
                                        range(dims[1][0], dims[1][1]),
                                        range(dims[2][0], dims[2][1])):
            n_sum = get_neighbour_sum((x, y, z), active_states)
            if (x, y, z) in active_states:
                if (n_sum == 2) or (n_sum == 3):
                    new_active_states.append((x, y, z))
            else:
                if n_sum == 3:
                    new_active_states.append((x, y, z))
        active_states = new_active_states.copy()

    print(len(new_active_states))


def main3(file_name='Day_17/17_input.txt'):
    with open(file_name, 'r') as f:
        input_slice = list(map(str.strip, f.readlines()))
    input_dim = len(input_slice)

    active_states = []
    for x, y, z, w in itertools.product(range(input_dim), range(input_dim), 
                                     range(1), range(1)):
        if input_slice[y][x] == '#':
            active_states.append((x, y, z, w))

    dims = [(0, input_dim), (0, input_dim), (0, 1), (0, 1)]
    
    for i in range(6):
        print(f'Iteration {i+1}')
        new_active_states = []
        dims = get_sorrounding_elems(dims, d=4)
        for x, y, z, w in itertools.product(range(dims[0][0], dims[0][1]),
                                        range(dims[1][0], dims[1][1]),
                                        range(dims[2][0], dims[2][1]),
                                        range(dims[3][0], dims[3][1])):
            n_sum = get_neighbour_sum((x, y, z, w), active_states, d=4)
            if (x, y, z, w) in active_states:
                if (n_sum == 2) or (n_sum == 3):
                    new_active_states.append((x, y, z, w))
            else:
                if n_sum == 3:
                    new_active_states.append((x, y, z, w))
        active_states = new_active_states.copy()

    print(len(new_active_states))


if __name__ == '__main__':
    start1 = time.time()
    # main2(file_name='Day_17/17_test.txt')
    main2()
    print(f'Part One completed in {time.time() - start1}')

    start2 = time.time()
    # main3(file_name='Day_17/17_test.txt')
    main3()
    print(f'Part Two completed in {time.time() - start2}')