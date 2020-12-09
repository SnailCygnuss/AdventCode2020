import itertools


def check_num_is_sum_from_list(num, list_of_nums):
    for a, b in itertools.combinations(list_of_nums, 2):
        if num == a + b:
            return True
    return False


def find_invalid_number(list_numbers, len_preamble=25):
    for idx, num in enumerate(list_numbers[len_preamble:]):
        list_num_preceeding = list_numbers[idx:len_preamble+idx]
        if not check_num_is_sum_from_list(num, list_num_preceeding):
            return num
    return False


def find_continous_sum_combination(num, list_of_nums):
    first_index_iterator = itertools.count()
    slice_index_iterator = itertools.count(2)
    f_idx = next(first_index_iterator)
    s_idx = next(slice_index_iterator)
    while True:
        sum_list_slice = sum(list_of_nums[f_idx:s_idx])
        if sum_list_slice == num:
            break
        elif sum_list_slice >= num:
            f_idx = next(first_index_iterator)
            slice_index_iterator = itertools.count(2)
        s_idx = next(slice_index_iterator)
    return list_of_nums[f_idx:s_idx]    


def main():
    file_name = 'Day_9/9_test.txt'
    file_name = 'Day_9/9_input.txt'
    with open(file_name, 'r') as f:
        list_numbers_stream = f.readlines()
    list_numbers_stream = [int(x) for x in list_numbers_stream]
    invalid_num = find_invalid_number(list_numbers_stream, 25)
    print('Part One')
    print(f'Invalid Number: {invalid_num}')
    print('Part Two')
    sum_combination = find_continous_sum_combination(invalid_num,
                                            list_numbers_stream)
    print(sum_combination)
    print(f'Sum of Max and Min: {max(sum_combination) + min(sum_combination)}')


if __name__ == '__main__':
    main()