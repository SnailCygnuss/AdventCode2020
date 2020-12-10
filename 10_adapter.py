import operator


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
        return max(list_joltage) + 3
    else:
        next_list = find_next_joltages(first_set, complete_joltage_set)
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


count_dict = {}
def count_dictionary_nesting(dictionary):
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
    print('Part One')
    print(find_joltage_difference(joltage_list))
    print('Part Two')
    adapter_combinations = recursive_find_next_combinations(0, joltage_list)
    print(count_dictionary_nesting(adapter_combinations))
    print('Done')


if __name__ == '__main__':
    main()