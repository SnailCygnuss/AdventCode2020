import time
import re
import itertools


def file_parse(contents):
    content_iterator = iter(contents)
    line = next(content_iterator)

    field_rules = {}
    reg_field = r'(.+): (\d+)-(\d+) or (\d+)-(\d+)'
    while not line.startswith('\n'):
        matches = re.match(reg_field, line)
        item, low1, high1, low2, high2 = matches.groups()
        field_rules[item] = {'low1': int(low1),
                             'high1': int(high1),
                             'low2': int(low2),
                             'high2': int(high2)}
        line = next(content_iterator)

    # print(field_rules)
    line = next(content_iterator) # Line 'your ticket:'
    line = next(content_iterator) # Self ticket details.
    self_ticket = list(map(int, line.strip().split(',')))

    line = next(content_iterator) # Line 'nearby tickets'
    line = next(content_iterator)
    other_tickets = []
    for line in content_iterator:
        other_tickets.append(list(map(int, line.strip().split(','))))
    # print(self_ticket)
    # print(other_tickets)
    return field_rules, self_ticket, other_tickets


def parse_field_values(field_rules):
    numbers = []
    for _, val in field_rules.items():
        numbers.extend(list(range(val['low1'], val['high1'] + 1)))
        numbers.extend(list(range(val['low2'], val['high2'] + 1)))
    numbers = set(numbers)
    # print(numbers)
    # input()
    return numbers


def validate_field(rule_set, ticket_char):
    if ticket_char in rule_set:
        return 0
    else:
        return ticket_char


def validate_ticket(rule_set, ticket):
    errors = map(validate_field, itertools.repeat(rule_set), ticket)
    # print(list(errors))
    return sum(list(errors))


def main(file_name='Day_16/16_input.txt'):
    with open(file_name, 'r') as f:
        file_contents = f.readlines()
    field_rules, self_ticket, other_tickets = file_parse(file_contents)
    allowed_nums = parse_field_values(field_rules)

    errors = []
    errors.append(validate_ticket(allowed_nums, self_ticket))
    for tkt in other_tickets:
        errors.append(validate_ticket(allowed_nums, tkt))

    print(sum(errors))
    

def validate_field2(rule_set, ticket_char):
    if ticket_char in rule_set:
        return True
    else:
        return False


def validate_ticket2(rule_set, ticket):
    errors = map(validate_field2, itertools.repeat(rule_set), ticket)
    # print(list(errors))
    return all(errors)


def get_field_values(tickets):
    num_fields = len(tickets[0])
    field_values = []
    for i in range(num_fields):
        field_values.append([x[i] for x in tickets])
    field_values = [sorted(x) for x in field_values]
    return field_values


def check_list_in_prohibited(value_list, fields_rules):
    smaller = [1 for x in value_list if x < fields_rules['low1']]
    between = [1 for x in value_list if fields_rules['high1'] < x < fields_rules['low2']]
    greater = [1 for x in value_list if x > fields_rules['high2']]

    # print(value_list)
    # print(smaller)
    # print(between)
    # print(greater)
    # input()
    if smaller or between or greater:
        return True
    else:
        return False


def remove_fields(field_list, not_fields):
    return [x for x in field_list if x not in not_fields]

def find_single_field(field_order):
    for idx, x in enumerate(field_order):
        if len(x) == 1:
            index = idx
            single_field = x[0]
    print(single_field, index)
    input()
    return single_field, index 


def find_field(field_rules, field_values):
    fields = list(field_rules.keys())
    fields_prohibited = {}
    nums = list(range(0, 1001))
    for key, val in field_rules.items():
        num1 = list(range(val['low1'], val['high1'] + 1))
        # num2= list(range(val['low2'], val['high2'] + 1)))
        num1.extend(list(range(val['low2'], val['high2'] + 1)))
        # nums = list(range(0, val['high2'] + 1))
        # combined = num1.union(num2)
        #print(combined)
        # fields_prohibited[key] = nums - combined
        fields_prohibited[key] = [x for x in nums if x not in num1]
        # print(key)
        # print(val['low1'], val['high1'], val['low2'], val['high2'])
        # print(fields_prohibited[key])
        # print(set(nums) - set(num1).union(set(num2)))
        # input()
    # print(fields_prohibited)

    field_order = [None for _ in fields]
    not_fields_list = []
    for value_list in field_values:
        # value_set = set(value_list)
        not_fields = []
        for field in fields:
            # print(value_set)
            # print(fields_prohibited[field])
            # if value_set.intersection(fields_prohibited[field]):
            if check_list_in_prohibited(value_list, field_rules[field]):
                # print('here')
                not_fields.append(field)
                continue
            # else:
            #    field_order.append(field)
                # fields.remove(field)
            #    break
        not_fields_list.append(not_fields)
    # print(not_fields_list)
    # for not_fields in not_fields_list:
    #     print(len(not_fields))
    
    while len(fields) > 0:
        field_order_list = [remove_fields(fields, x) for x in not_fields_list]
        single_item, index = find_single_field(field_order_list)
        fields.remove(single_item)
        field_order[index] = single_item
        print(field_order)
        print(f'Rem fields {fields}')
        input()
    # print(field_order)
    # input()
    return field_order


def main2(file_name='Day_16/16_input.txt'):
    with open(file_name, 'r') as f:
        file_contents = f.readlines()
    field_rules, self_ticket, other_tickets = file_parse(file_contents)
    allowed_nums = parse_field_values(field_rules)

    errors_free_tickets = []
    # errors.append(validate_ticket(allowed_nums, self_ticket))
    for idx, tkt in enumerate(other_tickets):
    # for tkt in other_tickets:
        if validate_ticket2(allowed_nums, tkt):
            errors_free_tickets.append(tkt)
        else:
            pass
            # print(idx+1)

    field_values_list = get_field_values(errors_free_tickets)
    field_order = find_field(field_rules, field_values_list)

    print(field_order)
    dep_mul = 1
    for idx, field in enumerate(field_order):
        if field.startswith('departure'):
            dep_mul = dep_mul * self_ticket[idx]
    print(dep_mul)

 

if __name__ == '__main__':
    start1 = time.time()
    # main(file_name='Day_16/16_test.txt')
    # main()
    print(f'Part One finished in {time.time() - start1}')

    start2 = time.time()
    # main2(file_name='Day_16/16_test2.txt')
    main2()
    print(f'Part Two finished in {time.time() - start2}')