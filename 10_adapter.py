import operator
import functools
import itertools


def find_next_joltage_set(joltage_set, full_joltage_set):
    min_next = min(joltage_set) + 1
    max_next = max(joltage_set) + 3
    next_joltage_set = set(range(min_next, max_next + 1))
    next_joltage_set.intersection_update(full_joltage_set)
    return next_joltage_set


def find_next_joltages(joltage, full_joltage_set):
    min_next = joltage + 1
    max_next = joltage + 3
    next_joltage_set = set(range(min_next, max_next + 1))
    next_joltage_set.intersection_update(full_joltage_set)
    return list(next_joltage_set)


recursive_dict = {}
def recursive_find_next_combinations(start, list_joltage):
    list_joltage.sort()
    complete_joltage_set = set(list_joltage)
    first_set = start
    if start in recursive_dict:
        return recursive_dict[start]
    elif start == max(complete_joltage_set):
        # print('Found')
        return max(list_joltage) + 3
    else:
        next_list = find_next_joltages(first_set, complete_joltage_set)
        # print(next_list)
        next_list_n = len(next_list)
        if next_list_n == 1:
            recursive_dict[start] = {next_list[0]: recursive_find_next_combinations(next_list[0], list_joltage)}
        elif next_list_n == 2:
            recursive_dict[start] = {next_list[0]: recursive_find_next_combinations(next_list[0], list_joltage),
            next_list[1]: recursive_find_next_combinations(next_list[1], list_joltage)}
        elif next_list_n == 3:
            recursive_dict[start] = {next_list[0]: recursive_find_next_combinations(next_list[0], list_joltage),
            next_list[1]: recursive_find_next_combinations(next_list[1], list_joltage),
            next_list[2]: recursive_find_next_combinations(next_list[2], list_joltage)}
        return recursive_dict[start]
    #    if next_list is None:
    #        return dict()
    #    for n in next_list:
    #        recursive_dict[n] = recursive_find_next_combinations(n, list_joltage)
    
    # print(recursive_dict)
    #return sum(list(map(recursive_find_next_combinations, next_list, itertools.repeat(list_joltage))))
    # return recursive_dict


count_dict = {}
def count_dictionary_nesting(dictionary):
    # print(list(dictionary.keys()))
    # if isinstance(dictionary, dict):
    #    print('Dict!!!')
    # if dictionary in count_dict:
    #    return count_dict[dictionary]
    if not isinstance(dictionary, dict):
        return 1

    keys = list(dictionary.keys())
    if len(keys) == 1:
        if not keys[0] in count_dict:
            count_dict[keys[0]] = count_dictionary_nesting(dictionary[keys[0]])
        return count_dict[keys[0]]
    
    elif len(keys) == 2:
        if not keys[0] in count_dict:
            count_dict[keys[0]] = count_dictionary_nesting(dictionary[keys[0]]) 
        if not keys[1] in count_dict:
            count_dict[keys[1]] = count_dictionary_nesting(dictionary[keys[1]])
        return count_dict[keys[0]] + count_dict[keys[1]]

    elif len(keys) == 3:
        if not keys[0] in count_dict:
            count_dict[keys[0]] = count_dictionary_nesting(dictionary[keys[0]]) 
        if not keys[1] in count_dict:
            count_dict[keys[1]] = count_dictionary_nesting(dictionary[keys[1]])
        if not keys[2] in count_dict:
            count_dict[keys[2]] = count_dictionary_nesting(dictionary[keys[2]])
        return count_dict[keys[0]] + count_dict[keys[1]] + count_dict[keys[2]]


def count_joltage_combinations(list_joltage):
    complete_joltage_set = set(list_joltage)
    first_set = {0}
    print(find_next_joltage_set(first_set, complete_joltage_set))
    print(find_next_joltage_set({19}, complete_joltage_set))
    
    present_set = first_set
    next_set = present_set
    list_length_set = []
    while len(next_set) != 0:
        next_set = find_next_joltage_set(present_set, complete_joltage_set)
        list_length_set.append(len(next_set))
        present_set = next_set
    print(list_length_set)
    print(functools.reduce(operator.mul, list_length_set))


def find_joltage_difference(list_num):
    sorted_list = sorted(list_num)
    sorted_list.append(sorted_list[-1] + 3) # Add device voltage +3
    sorted_list_shift = sorted_list.copy()
    sorted_list_shift.insert(0, 0)

    diff_list = list(map(operator.sub, sorted_list, sorted_list_shift))
    count_1 = diff_list.count(1)
    count_3 = diff_list.count(3)
    return count_1 * count_3


def main():
    file_name = 'Day_10/10_test.txt'
    file_name = 'Day_10/10_input.txt'
    with open(file_name, 'r') as f:
        joltage_list = f.readlines()
    joltage_list = list(map(int, joltage_list))
    # print(joltage_list)
    print(find_joltage_difference(joltage_list))
    print('Part Two')
    # count_joltage_combinations(joltage_list)
    print('='*10)
    # print(recursive_find_next_combinations(12, joltage_list))
    # print(recursive_find_next_combinations(11, joltage_list))
    # print(recursive_find_next_combinations(10, joltage_list))
    adapter_combinations = recursive_find_next_combinations(0, joltage_list)
    # print(adapter_combinations)
    print(count_dictionary_nesting(adapter_combinations))
    #print(count_dict)
    print('Done')
    # print(recursive_dict)


if __name__ == '__main__':
    main()