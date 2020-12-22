import time


def remove_decoded_word(possibilities_dict, word_to_remove):
    for key in possibilities_dict:
        try:
            possibilities_dict[key].discard(word_to_remove) 
        except ValueError:
            continue

    return possibilities_dict


def eliminate_possiblities(possibilities_dict):
    decode = {}
    # Check for item with single possibility
    while len(possibilities_dict) != 0:
        for allg, possibility in possibilities_dict.items():
            if len(possibility) == 1:
                decode[allg] = list(possibility)[0]
                decoded_word = list(possibility)[0]
                break

        possibilities_dict.pop(allg)

        possibilities_dict = remove_decoded_word(possibilities_dict, decoded_word)
    return decode


def find_allergen(unkno_allg, known_allg):
    # Find list of known allergens
    all_known_allg = []
    for allg_list in known_allg:
        for allg in allg_list:
            all_known_allg.append(allg)
    all_known_allg = set(all_known_allg)
    possibilities = {} # Dictionary to store possiblities of each allergen
    # Find common names between each unknown allergen list
    for allg in all_known_allg:
        possible_set = set()
        for u_allg, k_allg in zip(unkno_allg, known_allg):
            if allg in k_allg:
                if len(possible_set) == 0:
                    possible_set.update(u_allg)
                else:
                    possible_set.intersection_update(u_allg)
        possibilities[allg] = possible_set
    
    decode_key = eliminate_possiblities(possibilities)
    return decode_key


def without_allergens(unkno_allg, decoded_allg_dict):
    # Eliminate known allergens from each list
    # and find sum of list
    allg_list = decoded_allg_dict.values()
    for unkno_list in unkno_allg:
        for allg in allg_list:
            try:
                unkno_list.remove(allg)
            except ValueError:
                continue
    sum_no_allergens = sum(list(map(len, unkno_allg)))
    print(sum_no_allergens)


def process_input(input_data):

    unknown_allergen = []
    known_allergen = []
    for line in input_data:
        unknown_lang, known_lang = line.split('(')
        unknown_lang = unknown_lang.split()
        known_lang = known_lang.split()[1:]
        known_lang = [x.strip(',)') for x in known_lang]
        unknown_allergen.append(unknown_lang)
        known_allergen.append(known_lang)

    return unknown_allergen, known_allergen


def main(file_name='Day_21/21_input.txt'):
    with open(file_name, 'r') as f:
        input_data = f.readlines()

    # Parse Input
    unkno_alg_list, known_alg_list = process_input(input_data)

    # Find mapping of each allergen
    decode_allg = find_allergen(unkno_alg_list, known_alg_list)
    # Calculate ingredients without allergen
    without_allergens(unkno_alg_list, decode_allg)

    # Part 2
    ingredient_list = ''
    for label in sorted(decode_allg):
        ingredient_list += decode_allg[label] + ','
    ingredient_list = ingredient_list[:-1]
    print(ingredient_list)
    

def testcase():
    print('TestCase')
    main(file_name='Day_21/21_test.txt')


if __name__ == '__main__':
    start1 = time.time()
    # testcase()
    main()
    print(f'Part One finished in {time.time() - start1}')