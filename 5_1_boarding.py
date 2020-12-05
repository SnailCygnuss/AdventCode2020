def seat_id(row, col):
    return (row * 8) + col


def lower_upper(char, start, stop):
    if char in ['F', 'L']:
        pos1 = start
        pos2 = start + ((stop - start) / 2) - 0.5
    elif char in ['B', 'R']:
        pos1 = start + ((stop - start) / 2) + 0.5
        pos2 = stop
    return int(pos1), int(pos2)


def bin_int(num_chars):
    i = '1' * num_chars
    return int(i, 2)


def position(seat_num, start, end):
    if len(seat_num) == 1:
        pos, _ = lower_upper(seat_num, start, end)
        return pos
    else:
        rem_seat = seat_num[1:]
        next_start, next_end = lower_upper(seat_num[0], start, end)
        # print(seat_num, next_start, next_end)
        return position(rem_seat, next_start, next_end)


def seat_position(seat_num):
    row = position(seat_num[:-3], 0, bin_int(len(seat_num[:-3])))
    col = position(seat_num[-3:], 0, bin_int(len(seat_num[-3:])))
    return row, col


def main():
    with open(file_name, 'r') as f:
        seat_ids = []
        for seat in f:
            row, col = seat_position(seat.strip())
            seat_ids.append(seat_id(row, col))
            # print(f'Row: {row} Col: {col} SeatID: {seat_id(row, col)}')
    print(max(seat_ids))

if __name__ == '__main__':
    # file_name = 'Day_5/5_test.txt'
    file_name = 'Day_5/5_input.txt'
    main()
