import time
import re
import itertools


def simplify_directions(directions):
    pat = r'(se|sw|w|nw|ne|e|se)'
    accumulated_dir = {'ne': 0, 'e': 0, 'se': 0,
                       'sw': 0, 'w': 0, 'nw': 0 }
    dir_map = {'ne': 1, 'e': 1, 'se': 1,
               'sw': -1, 'w': -1, 'nw': -1}
    match = re.findall(pat, directions)
    for i in match:
        accumulated_dir[i] += dir_map[i]

    simplified_dir = {}
    simplified_dir['ne'] = accumulated_dir['ne'] + accumulated_dir['sw']
    simplified_dir['e'] = accumulated_dir['e'] + accumulated_dir['w']
    simplified_dir['se'] = accumulated_dir['se'] + accumulated_dir['nw']
    coords = (simplified_dir['ne'] + simplified_dir['e'], 
              simplified_dir['se'] + simplified_dir['e'])
    return coords


def find_largest_SE_NE_tile(tile_status):
    ne_list = []
    sw_list = []
    for key in tile_status:
        ne_list.append(abs(key[0]))
        sw_list.append(abs(key[1]))
    return max(ne_list), max(sw_list)


def flip_tile(tile_coords: tuple, tile_status: int, tiles_status: dict) -> int:
    new_tile_status = tile_status
    black_neighbour_count = 0
    exclude = [(0, 0), (-1, 1), (1, -1)]

    for a, b in itertools.product([-1, 0, 1], repeat=2):
        if (a, b) not in exclude:
            n_coords = (tile_coords[0] - a, tile_coords[1] - b)
            black_neighbour_count += tiles_status.get(n_coords, 0)

    if tile_status == 1:
        if black_neighbour_count == 0 or black_neighbour_count > 2:
            new_tile_status = 0
    elif tile_status == 0:
        if black_neighbour_count == 2:
            new_tile_status = 1

    return new_tile_status


def flip_tiles(tiles_status: dict, ne_max: int, sw_max: int) -> dict:
    
    new_tiles_status = {}
    for x, y in itertools.product(range(-ne_max-1, ne_max+2, 1), 
                                  range(-sw_max-1, sw_max+2, 1)):

        updated_tile = flip_tile((x, y), tiles_status.get((x, y), 0),
                                 tiles_status)
        if updated_tile:
            new_tiles_status[(x, y)] = updated_tile

    return new_tiles_status
    


def main(file_name='Day_24/24_input.txt'):
    with open(file_name, 'r') as f:
        input_data = list(map(str.strip, f.readlines()))

    tile_flipped = {}
    for data in input_data:
        tile_loc = simplify_directions(data)
        tile_flipped.setdefault(tile_loc, 0)
        tile_flipped[tile_loc] = 1 if tile_flipped[tile_loc] == 0 else 0

    count_black = sum(tile_flipped.values())
    print(count_black)

    print('Part Two')
    # Find largest tile
    ne_max, sw_max = find_largest_SE_NE_tile(tile_flipped)

    print_days = [(i*10)-1 for i in range(1, 11)]
    for i in range(100):
        tile_flipped = flip_tiles(tile_flipped, ne_max+i, sw_max+i)
        count_black = sum(tile_flipped.values())
        if i in print_days:
            print(f'Day {i+1}: {count_black}')


if __name__ == '__main__':
    start1 = time.time()
    # main(file_name='Day_24/24_test.txt') # Test Case
    main()
    print(f'Part One finished in {time.time() - start1}')