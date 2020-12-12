import pprint
import itertools
import numpy as np
import time



def occupy_seats(seat_layout):
    # 1 2 3
    # 8   4
    # 7 6 5 
    # Neighboouring seats in clockwise direction
    initial_layout = seat_layout.copy()

    seat_layout = np.insert(seat_layout, 0, '.', axis=1)
    seat_layout = np.append(seat_layout, seat_layout[:, 0].reshape(-1, 1), axis=1)
    seat_layout = np.insert(seat_layout, 0, '.', axis=0)
    seat_layout = np.append(seat_layout, seat_layout[0, :].reshape(1, -1), axis=0)
 
    # Insert empty row above and delete last row
    seat_1 = seat_layout[:-2, :-2].copy()
    seat_2 = seat_layout[:-2, 1:-1].copy()
    seat_3 = seat_layout[:-2, 2:].copy()
    seat_4 = seat_layout[1:-1, 2:].copy()
    seat_5 = seat_layout[2:, 2:].copy()
    seat_6 = seat_layout[2:, 1:-1].copy() 
    seat_7 = seat_layout[2:, :-2].copy()
    seat_8 = seat_layout[1:-1, :-2].copy()

    seat_set = [seat_1, seat_2, seat_3, seat_4,
                seat_5, seat_6, seat_7, seat_8]
    seat_add = np.char.add(seat_1, seat_2)
    for seat in seat_set[2:]:
        seat_add = np.char.add(seat_add, seat)
    # print(seat_add)
    seat_neighbour_occupied = np.char.count(seat_add, '#')
    # print(seat_neighbour_occupied)

    new_layout = initial_layout.copy()
    # Intial seat empty and 0 neighbours
    empty_seat_with_no_neighbour = np.logical_and((initial_layout == 'L'), (seat_neighbour_occupied == 0))
    new_layout[empty_seat_with_no_neighbour] = '#'

    # Intial seat is occupied and more than 4 neighbours
    occupied_more_four_neighbour = np.logical_and((initial_layout == '#'),  (seat_neighbour_occupied >= 4))
    new_layout[occupied_more_four_neighbour] = 'L'

    return new_layout

def toggle_seat_layout(seat_layout, loop=1):
    # print(f'Loop {loop}')
    loop = loop + 1
    new_layout = occupy_seats(seat_layout)
    if (new_layout == seat_layout).all():
        return new_layout
    else:
        return toggle_seat_layout(new_layout, loop)


def assign_neighbour(ele, x, y, seat_layout):
    error_tuple = (0, 1) # == '.' in test data
    # Seat 1
    try:
        inc = 1
        s1 = seat_layout[x-inc, y-inc]
        while s1 == '.':
            inc = inc + 1
            s1 = seat_layout[x-inc, y-inc]
        if (x - inc) < 0 or (y - inc) < 0:
            s1 = error_tuple
        else:
            s1 = (x-inc, y-inc)
    except IndexError:
        s1 = error_tuple

    # Seat 2    
    try:
        inc = 1
        s2 = seat_layout[x-inc, y]
        while s2 == '.':
            inc = inc + 1
            s2 = seat_layout[x-inc, y]
        if x - inc < 0:
            s2 = error_tuple
        else:
            s2 = (x-inc, y)
    except IndexError:
        s2 = error_tuple
    
    # Seat 3
    try:
        inc = 1
        s3 = seat_layout[x-inc, y+inc]
        while s3 == '.':
            inc = inc + 1
            s3 = seat_layout[x-inc, y+inc]
        if x - inc < 0:
            s3 = error_tuple
        else:
            s3 = (x-inc, y+inc)
    except IndexError:
        s3 = error_tuple
    
    # Seat 4
    try:
        inc = 1
        s4 = seat_layout[x, y+inc]
        while s4 == '.':
            inc = inc + 1
            s4 = seat_layout[x, y+inc]
        s4 = (x, y+inc)
    except IndexError:
        s4 = error_tuple
    
    # Seat 5
    try:
        inc = 1
        s5 = seat_layout[x+inc, y+inc]
        while s5 == '.':
            inc = inc + 1
            s5 = seat_layout[x+inc, y+inc]
        s5 = (x+inc, y+inc)
    except IndexError:
        s5 = error_tuple
    
    # Seat 6
    try:
        inc = 1
        s6 = seat_layout[x+inc, y]
        while s6 == '.':
            inc = inc + 1
            s6 = seat_layout[x+inc, y]
        s6 = (x+inc, y)
    except IndexError:
        s6 = error_tuple
    
    # Seat 7
    try:
        inc = 1
        s7 = seat_layout[x+inc, y-inc]
        while s7 == '.':
            inc = inc + 1
            s7 = seat_layout[x+inc, y-inc]
        if y - inc < 0:
            s7 = error_tuple
        else:
            s7 = (x+inc, y-inc)
    except IndexError:
        s7 = error_tuple
    
    # Seat 8
    try:
        inc = 1
        s8 = seat_layout[x, y-inc]
        while s8 == '.':
            inc = inc + 1
            s8 = seat_layout[x, y-inc]
        if y-inc < 0: 
            s8 = error_tuple 
        else:
            s8 = (x, y-inc)
    except IndexError:
        s8 = error_tuple

    return s1, s2, s3, s4, s5, s6, s7, s8
    

def find_neighbours_coords(seat_layout):
    seat_1x = np.zeros(seat_layout.shape, dtype='int')
    seat_1y = np.zeros(seat_layout.shape, dtype='int')
    seat_2x = np.zeros(seat_layout.shape, dtype='int')
    seat_2y = np.zeros(seat_layout.shape, dtype='int')
    seat_3x = np.zeros(seat_layout.shape, dtype='int')
    seat_3y = np.zeros(seat_layout.shape, dtype='int')
    seat_4x = np.zeros(seat_layout.shape, dtype='int')
    seat_4y = np.zeros(seat_layout.shape, dtype='int')
    seat_5x = np.zeros(seat_layout.shape, dtype='int')
    seat_5y = np.zeros(seat_layout.shape, dtype='int')
    seat_6x = np.zeros(seat_layout.shape, dtype='int')
    seat_6y = np.zeros(seat_layout.shape, dtype='int')
    seat_7x = np.zeros(seat_layout.shape, dtype='int')
    seat_7y = np.zeros(seat_layout.shape, dtype='int')
    seat_8x = np.zeros(seat_layout.shape, dtype='int')
    seat_8y = np.zeros(seat_layout.shape, dtype='int')

    for idx, row in enumerate(seat_layout):
        for idy, ele in enumerate(row):
            neighbours = assign_neighbour(ele, idx, idy, seat_layout)
            seat_1x[idx, idy] = neighbours[0][0]
            seat_1y[idx, idy] = neighbours[0][1]
            seat_2x[idx, idy] = neighbours[1][0]
            seat_2y[idx, idy] = neighbours[1][1]
            seat_3x[idx, idy] = neighbours[2][0]
            seat_3y[idx, idy] = neighbours[2][1]
            seat_4x[idx, idy] = neighbours[3][0]
            seat_4y[idx, idy] = neighbours[3][1]
            seat_5x[idx, idy] = neighbours[4][0]
            seat_5y[idx, idy] = neighbours[4][1]
            seat_6x[idx, idy] = neighbours[5][0]
            seat_6y[idx, idy] = neighbours[5][1]
            seat_7x[idx, idy] = neighbours[6][0]
            seat_7y[idx, idy] = neighbours[6][1]
            seat_8x[idx, idy] = neighbours[7][0]
            seat_8y[idx, idy] = neighbours[7][1]
    # print(seat_1x, seat_1y)
    seat_x = [seat_1x, seat_2x, seat_3x, seat_4x,
              seat_5x, seat_6x, seat_7x, seat_8x]
    seat_y = [seat_1y, seat_2y, seat_3y, seat_4y,
              seat_5y, seat_6y, seat_7y, seat_8y] 
    
    return seat_x, seat_y


def find_neighbour_counts(seat_layout, coords_x, coords_y):
    seat = []
    size = seat_layout.shape
    for _ in range(8):
        seat.append(np.zeros(size, dtype='<U1'))
    
    # print(seat[0][0, 0])
    # seat[0][0, 0] = seat_layout[coords_x[0][0, 0], coords_y[0][0, 0]]
    # print(seat[0][0, 0])
    for x, y in itertools.product(range(size[0]), range(size[1])):
        # print(x, y)
        seat[0][x, y] = seat_layout[coords_x[0][x, y], coords_y[0][x, y]]
        seat[1][x, y] = seat_layout[coords_x[1][x, y], coords_y[1][x, y]]
        seat[2][x, y] = seat_layout[coords_x[2][x, y], coords_y[2][x, y]]
        seat[3][x, y] = seat_layout[coords_x[3][x, y], coords_y[3][x, y]]
        seat[4][x, y] = seat_layout[coords_x[4][x, y], coords_y[4][x, y]]
        seat[5][x, y] = seat_layout[coords_x[5][x, y], coords_y[5][x, y]]
        seat[6][x, y] = seat_layout[coords_x[6][x, y], coords_y[6][x, y]]
        seat[7][x, y] = seat_layout[coords_x[7][x, y], coords_y[7][x, y]]

    # print(coords_x[0][0, 0], coords_y[0][0, 0])
    # print(seat_layout[0, 1])
    # print(seat[0])
    seat_combined = np.char.add(seat[0], seat[1])
    for n in seat[2:]:
        seat_combined = np.char.add(seat_combined, n)
    # print()
    # print(seat_combined)
    seat_occupied_count = np.char.count(seat_combined, '#')
    return seat_occupied_count


def replace_seats(seat_layout, seat_occupied_count):
   
    new_layout = seat_layout.copy()
    # Intial seat empty and 0 neighbours
    empty_seat_with_no_neighbour = np.logical_and((seat_layout == 'L'), (seat_occupied_count == 0))
    new_layout[empty_seat_with_no_neighbour] = '#'

    # Intial seat is occupied and more than 5 neighbours
    occupied_more_five_neighbour = np.logical_and((seat_layout == '#'),  (seat_occupied_count >= 5))
    new_layout[occupied_more_five_neighbour] = 'L'

    return new_layout


def find_neighbours_2(seat_layout, neighbor_coords=None):
    # Find coords of neighbours
    # start = time.time()
    if neighbor_coords is None:
        neighbor_coords_x, neighbor_coords_y = find_neighbours_coords(seat_layout)
    else:
        neighbor_coords_x = neighbor_coords[0]
        neighbor_coords_y = neighbor_coords[1]
    # print(f'Finished neighbour coords in {time.time() - start}')

    # Find count of neighbors as per coordinates
    # start = time.time()
    neighbour_counts = find_neighbour_counts(seat_layout, neighbor_coords_x, neighbor_coords_y)
    # print(f'Finished neighbour counts in {time.time() - start}')
    # Find count of neighbours

    # Replace seats as per rules
    # start = time.time()
    changed_seat_layout = replace_seats(seat_layout, neighbour_counts)
    # print(f'Finished changing seat in {time.time() - start}')
    return changed_seat_layout
    

def main():
    file_name = 'Day_11/11_test.txt'
    file_name = 'Day_11/11_input.txt'
    with open(file_name, 'r') as f:
        seating_layout = list(map(str.strip, f.readlines()))

    seating_layout = [list(x) for x in seating_layout]
    seating_layout = np.array(seating_layout)
    # n_rows, n_cols = seating_layout.shape
    # # Add dummy rows and columns at four sides
    # seating_layout = np.insert(seating_layout, 0, '.', axis=1)
    # seating_layout = np.append(seating_layout, seating_layout[:, 0].reshape(-1, 1), axis=1)
    # seating_layout = np.insert(seating_layout, 0, '.', axis=0)
    # seating_layout = np.append(seating_layout, seating_layout[0, :].reshape(1, -1), axis=0)
    # print(seating_layout)
    
    # Part One
    #new_seating_layout = toggle_seat_layout(seating_layout)
    #print((new_seating_layout == '#').sum())

    # Part Two
    neighbour_coords = find_neighbours_coords(seating_layout)
    new_layout = find_neighbours_2(seating_layout, neighbor_coords=neighbour_coords)
    new_layout2 = find_neighbours_2(new_layout, neighbor_coords=neighbour_coords)
    while not (new_layout == new_layout2).all():
        new_layout = new_layout2
        new_layout2 = find_neighbours_2(new_layout, neighbor_coords=neighbour_coords)
    print((new_layout2 == '#').sum())
    # print(new_layout)


if __name__ == '__main__':
    start = time.time()
    main()
    print(f'Finished in {time.time() - start}')