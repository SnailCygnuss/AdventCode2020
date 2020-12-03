import pprint

# file_name = 'Day_3/3_test.txt'
file_name = 'Day_3/3_input.txt'

with open(file_name, 'r') as f:
    forest = f.readlines()

forest = [x.rstrip() for x in forest]
# print(pprint.pformat(forest))


def trajectory(forest, right=3, down=1):
    start_x = 0
    start_y = 0

    width = len(forest[0]) # Width of forest for repeating pattern

    x = start_x + right
    y = start_y + down

    # Make a copy of forest to represent transversing
    b = lambda x: list(x)
    transversed_forest = [b(x) for x in forest]

    open_space = 0
    tree_space = 0

    while y < len(forest):
        # print(x, y)
        if x >= width:
            x = x - width
            # print(x, y)
        if forest[y][x] == '.':
            open_space = open_space + 1
            transversed_forest[y][x] = 'O'
        elif forest[y][x] == '#':
            tree_space = tree_space + 1
            transversed_forest[y][x] = 'X'
        x = x + right
        y = y + down

    # print(f'Open Spaces: {open_space}')
    # print(f'Tree Spaces: {tree_space}')
    # print(pprint.pformat(transversed_forest))
    return open_space, tree_space


_, tree1 = trajectory(forest, right=1, down=1)
_, tree2 = trajectory(forest, right=3, down=1)
_, tree3 = trajectory(forest, right=5, down=1)
_, tree4 = trajectory(forest, right=7, down=1)
_, tree5 = trajectory(forest, right=1, down=2)

prod = tree1 * tree2 * tree3 * tree4 * tree5
print(prod)