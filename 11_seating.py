import pprint
import numpy as np


def toggle_seats_middle_row(three_rows):
    middle_row = three_rows[1]
    # Find occupied neighbors for each seat
    neighbours = 

def occupy_seat(seat_layout):
    modified_seat_layout = []

def insert_empty_space_beginning_end(row):
    row.insert(0, '.')
    row.append('.')
    return row


def main():
    file_name = 'Day_11/11_test.txt'
    # file_name = 'Day_11/11_input.txt'
    with open(file_name, 'r') as f:
        seating_layout = list(map(str.strip, f.readlines()))

    # Insert empty rows at the top and bottom
    row_length = len(seating_layout[0])
    seating_layout = [list(x) for x in seating_layout]
    empty_row = ['.' for _ in range(row_length)]
    # print(empty_row)
    seating_layout.insert(0, empty_row.copy())
    seating_layout.append(empty_row.copy())

    # Insert empty columns at left and right
    seating_layout = list(map(insert_empty_space_beginning_end, seating_layout))
    pprint.pprint(seating_layout)


if __name__ == '__main__':
    main()