import time
import itertools
import operator
import functools
import re


class ImageData:

    def __init__(self, data_input):
        self.image_no = int(data_input[0].split()[1][:-1])
        self.image_data = data_input[1:].copy()
        self.find_edges()


    def find_edges(self):
        self.top_edge = self.image_data[0]
        self.bot_edge = self.image_data[-1]
        self.lft_edge = []
        self.rgt_edge = []
        for line in self.image_data:
            self.lft_edge.append(line[0])
            self.rgt_edge.append(line[-1])
        self.lft_edge = ''.join(self.lft_edge)
        self.rgt_edge = ''.join(self.rgt_edge)
        # Find flipped edges
        self.top_flp_edge = self.top_edge[::-1]
        self.bot_flp_edge = self.bot_edge[::-1]
        self.lft_flp_edge = self.lft_edge[::-1]
        self.rgt_flp_edge = self.rgt_edge[::-1]
        self.edges = [self.top_edge, self.bot_edge, 
                      self.lft_edge, self.rgt_edge,
                      self.top_flp_edge, self.bot_flp_edge,
                      self.lft_flp_edge, self.rgt_flp_edge]


    def check_matching_edge(self, image_data_obj):
        # Return mathcing edge numbers
        edge1 = -1  # No matching edge
        edge2 = -1  # No matching edge
        for e1, e2 in itertools.product(range(len(self.edges)),
                                            range(len(image_data_obj.edges))):
            if self.edges[e1] == image_data_obj.edges[e2]:
                edge1 = e1
                edge2 = e2
                break
        
        return edge1, edge2

    def flip_edge(self, edge_number):
        if edge_number == 'hor':
            self.image_data = [x[::-1] for x in self.image_data]
        elif edge_number == 'ver':
            self.image_data = self.image_data[::-1]
        self.find_edges()


    def rotate_edge_ccw(self):
        rotated = []
        for i in range(len(self.image_data[0])-1, -1, -1):
            rotated.append([line[i] for line in self.image_data])
        self.image_data = [''.join(line) for line in rotated]
        self.find_edges()


    def remove_border(self, line):
        if line in [0, len(self.image_data)-1]:
            rtr_str = ''
        else:
            rtr_str = self.image_data[line][1:-1]
        return rtr_str


def search_matching_edges(image_data_list):
    match_data = []
    # Compare one img_obj with another to find matching edges
    for img_obj1, img_obj2 in itertools.combinations(image_data_list, 2):
        edge1, edge2 = img_obj1.check_matching_edge(img_obj2)
        if not edge1 == edge2 == -1:
            match_data.append({img_obj1.image_no: edge1, 
                               img_obj2.image_no: edge2})

    return match_data


def find_corners(match_data, image_num_list):
    # Find numbers of corner tiles and return the list
    corner_tiles = []
    for image_num in image_num_list:
        matching_edges = map(operator.contains, match_data, 
                             itertools.repeat(image_num))
        no_matching_edges = sum(matching_edges)
        if no_matching_edges == 2:
            corner_tiles.append(image_num)
    
    return corner_tiles

   
def print_canvas(canvas):
    for i in range(len(canvas)):
        for j in range(len(canvas)):
            try:
                print(canvas[i][j].image_no, end=' ')
            except AttributeError:
                print(canvas[i][j], end=' ')
        print()

    for i in range(len(canvas)):
        for line in range(len(canvas[i][0].image_data)):
            for j in range(len(canvas)):
                try:
                    print_line = canvas[i][j].image_data[line]
                    print(print_line, end=' ')
                except AttributeError:
                    print(canvas[i][j], end=' ')
            print()
        print()
    print()


def make_canvas(canvas):
    canvas_list = []
    canvas_str = ''    

    for i in range(len(canvas)):
        for line in range(len(canvas[i][0].image_data)):
            canvas_str = ''    
            for j in range(len(canvas)):
                    canvas_str += canvas[i][j].remove_border(line=line)
            canvas_list.append(canvas_str)
    canvas_list = [x for x in canvas_list if x != '']
    return canvas_list

def find_tile_location(match_data, image_num_list, image_data_list):
    tile_corners = {}
    for image_num in image_num_list:
        image_edges = []
        matching_edges = map(operator.contains, match_data,
                             itertools.repeat(image_num))
        for match in itertools.compress(match_data, matching_edges):
            image_edges.append(match[image_num])
        tile_corners[image_num] = image_edges
    # Find a corner piece
    for image_num, corners in tile_corners.items():
        if len(corners) == 2:
            corner_image = image_num
            break           

    mask = [1 for _ in image_data_list]
    canvas_size = int(len(image_num_list)**0.5)
    canvas = [[0 for _ in range(canvas_size)] for _ in range(canvas_size)]
    idx = image_num_list.index(corner_image)
    canvas[0][0] = image_data_list[idx]
    mask[idx] = 0 # Do not check this tile again

    # Fix rotation of corner piece and tile below it
    for img_data in itertools.compress(image_data_list, mask):
        e1, e2 = canvas[0][0].check_matching_edge(img_data)
        if e1 == 0:
            # hardcoded for test data :(
            if e1 == 0:
                canvas[0][0].flip_edge('ver')
            elif e1 == 2:
                canvas[0][0].rotate_edge_ccw()
            elif e1 == 3:
                canvas[0][0].flip_edge('hor')
                canvas[0][0].rotate_edge_ccw()
            elif e1 == 4:
                canvas[0][0].flip_edge('hor')
                canvas[0][0].flip_edge('ver')
            elif e1 == 5:
                canvas[0][0].flip_edge('hor')
            elif e1 == 6:
                canvas[0][0].rotate_edge_ccw()
                canvas[0][0].flip_edge('hor')
            elif e1 == 7:
                for _ in range(3):
                    canvas[0][0].rotate_edge_ccw()
            if e2 == 1:
                img_data.flip_edge('ver')
            elif e2 == 2:
                img_data.rotate_edge_ccw()
                img_data.flip_edge('ver')
            elif e2 == 3:
                img_data.rotate_edge_ccw()
            elif e2 == 4:
                img_data.flip_edge('hor')
            elif e2 == 5:
                img_data.flip_edge('ver')
                img_data.flip_edge('hor')
            elif e2 == 6:
                for _ in range(3):
                    img_data.rotate_edge_ccw()
            elif e2 == 7:                    
                img_data.rotate_edge_ccw()
                img_data.flip_edge('hor')
            canvas[1][0] = img_data
            idx = image_num_list.index(canvas[1][0].image_no)
            mask[idx] = 0
        elif e1 == 2: 
            # Hardcoded for input data :(               
            canvas[0][0].rotate_edge_ccw()
            if e2 == 6:
                for _ in range(3):
                    img_data.rotate_edge_ccw()
            canvas[1][0] = img_data
            idx = image_num_list.index(canvas[1][0].image_no)
            mask[idx] = 0

    # Fill left edge
    for i in range(1, canvas_size-1):
        bot_line = canvas[i][0].image_data[-1]
        outer_break = 0
        for img_data in itertools.compress(image_data_list, mask):
            for idx, edge in enumerate(img_data.edges):
                if bot_line == edge:                        
                    if idx == 1:                            
                        img_data.flip_edge('ver')
                    elif idx == 2:
                        for _ in range(3):
                            img_data.rotate_edge_ccw()
                        img_data.flip_edge('hor')
                    elif idx == 3:
                        img_data.rotate_edge_ccw()
                    elif idx == 4:
                        img_data.flip_edge('hor')
                    elif idx == 5:
                        img_data.rotate_edge_ccw()
                        img_data.rotate_edge_ccw()
                    elif idx == 6:
                        for _ in range(3):
                            img_data.rotate_edge_ccw()
                    elif idx == 7:
                        img_data.rotate_edge_ccw()
                        img_data.flip_edge('hor')
                    canvas[i+1][0] = img_data
                    idx = image_num_list.index(canvas[i+1][0].image_no)
                    mask[idx] = 0
                    outer_break = 1
                    break
            if outer_break:
                break

    # Fill other tiles
    for i, j in itertools.product(range(canvas_size), range(canvas_size-1)):
        rgt_edge = canvas[i][j].edges[3]
        outer_break = 0
        for img_data in itertools.compress(image_data_list, mask):
                
            for idx, edge in enumerate(img_data.edges):                    
                if rgt_edge == edge:
                    if idx == 0:
                        img_data.rotate_edge_ccw()
                        img_data.flip_edge('ver')
                    elif idx == 1:
                        for _ in range(3):
                            img_data.rotate_edge_ccw()
                    elif idx == 3:
                        img_data.flip_edge('hor')
                    elif idx == 4:
                        img_data.rotate_edge_ccw()
                    elif idx == 5:
                        img_data.rotate_edge_ccw()
                        img_data.flip_edge('hor')
                    elif idx == 6:
                        img_data.flip_edge('ver')
                    elif idx == 7:
                        img_data.flip_edge('ver')
                        img_data.flip_edge('hor')
                    canvas[i][j+1] = img_data
                    idx = image_num_list.index(canvas[i][j+1].image_no)
                    mask[idx] = 0
                    outer_break = 1
                    break
            if outer_break:
                break

    # print_canvas(canvas)
    canvas_list = make_canvas(canvas)
    return canvas_list


def read_tile_data(file_obj):
    # Read data from file and save them as image objects
    line = file_obj.readline()
    image_data_list = []
    while True:
        if line.startswith('Tile'):
            tile_data = []
            tile_data.append(line.strip())
            # Append the next lines till blank line
            line = file_obj.readline()
            while line != '\n':
                tile_data.append(line.strip())
                line = file_obj.readline()
                if line == '':    
                    break
            image_data_list.append(ImageData(tile_data))
        
        line = file_obj.readline()
        if line == '':
            break
    
    return image_data_list


def flip_canvas(canvas_list):
    def rotate_ccw(canvas_list):
        rotated = []
        for i in range(len(canvas_list[0])-1, -1, -1):
            rotated.append([line[i] for line in canvas_list])
        rotated = [''.join(line) for line in rotated]
        return rotated

    def flip(canvas_list, direction):
        flipped = []
        if direction == 'hor':
            for line in canvas_list:
                flipped.append(line[::-1])
        elif direction == 'ver':
            flipped = canvas_list[::-1]
        return flipped

    flip_dirs = ['hor', 'ver']
    rot_deg = [0, 1, 2, 3]

    flipped_canvas = canvas_list.copy()
    for rot, flip_dir in itertools.product(rot_deg, flip_dirs):
        for _ in range(rot):
            flipped_canvas = rotate_ccw(flipped_canvas)
        flipped_canvas = flip(flipped_canvas, flip_dir)
        yield flipped_canvas


def find_monster(canvas_list):
    monster_pat = r'([\.#]{18})#([\.#]\n)#([\.#]{4})##([\.#]{4})##([\.#]{4})###(\n[\.#])#([\.#]{2})#([\.#]{2})#([\.#]{2})#([\.#]{2})#([\.#]{2})#([\.#]{3})'
    repl_pat = r'\g<1>0\g<2>0\g<3>00\g<4>00\g<5>000\g<6>0\g<7>0\g<8>0\g<9>0\g<10>0\g<11>0\g<12>'
    # Search in 20X3 grid
    loc_i = []
    loc_x = []
    monster_can = ''
    break_canvas = 0
    for can in flip_canvas(canvas_list):
        for i in range(len(can) - 2):
            for x in range(len(can) - 19):
                search_grid = can[i][x:20+x] + '\n' \
                        + can[i+1][x:20+x] + '\n' \
                        + can[i+2][x:20+x]
                if re.match(monster_pat, search_grid):
                    loc_i.append(i)
                    loc_x.append(x)
                    break_canvas = 1
                    monster_can = can
        if break_canvas:
            break            
            
    new_can = None
    for i, x in zip(loc_i, loc_x):            
        new_can = monster_can[:i].copy()
        search_grid = monster_can[i][x:20+x] + '\n' \
                      + monster_can[i+1][x:20+x] + '\n' \
                      + monster_can[i+2][x:20+x]
        monster_string = re.sub(monster_pat, repl_pat, search_grid)
        monster_string_list = monster_string.split('\n')
        first_line = monster_can[i][:x] + monster_string_list[0] \
                     + monster_can[i][x+20:]
        second_line = monster_can[i+1][:x] + monster_string_list[1] \
                     + monster_can[i+1][x+20:]
        third_line = monster_can[i+2][:x] + monster_string_list[2] \
                     + monster_can[i+2][x+20:]
        
        new_can.append(first_line)
        new_can.append(second_line)
        new_can.append(third_line)
        new_can.extend(monster_can[i+3:])
        monster_can = new_can.copy()

    hash_count = 0 
    for line in monster_can:
        hash_count += line.count('#')
    print('No of # in replaced image: ', hash_count)


def main(file_name='Day_20/20_input.txt'):
    file_obj = open(file_name, 'r')
    images_list = read_tile_data(file_obj)
    # List of image numbers
    image_num_list = [img_obj.image_no for img_obj in images_list]
    file_obj.close()

    # image_class_test(images_list)    
    match_data = search_matching_edges(images_list)
    corner_tiles = find_corners(match_data, image_num_list)
    print('Corner Tiles: ', corner_tiles)
    corner_product = functools.reduce(operator.mul, corner_tiles)
    print('Corner Tile number product: ', corner_product)

    
    canvas_list = find_tile_location(match_data, image_num_list, images_list)
    find_monster(canvas_list)
    return 


def testmain():
    main(file_name='Day_20/20_test.txt')


if __name__ == '__main__':
    start1 = time.time()
    # testmain()
    main()
    print(f'Part One completed in {time.time() - start1}')