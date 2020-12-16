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

    line = next(content_iterator) # Line 'your ticket:'
    line = next(content_iterator) # Self ticket details.
    self_ticket = list(map(int, line.strip().split(',')))

    line = next(content_iterator) # Line 'nearby tickets'
    line = next(content_iterator)
    other_tickets = []
    for line in content_iterator:
        other_tickets.append(list(map(int, line.strip().split(','))))
    return field_rules, self_ticket, other_tickets


def parse_field_values(field_rules):
    numbers = []
    for _, val in field_rules.items():
        numbers.extend(list(range(val['low1'], val['high1'] + 1)))
        numbers.extend(list(range(val['low2'], val['high2'] + 1)))
    numbers = set(numbers)
    return numbers


def validate_field(rule_set, ticket_char):
    if ticket_char in rule_set:
        return 0
    else:
        return ticket_char


def validate_ticket(rule_set, ticket):
    errors = map(validate_field, itertools.repeat(rule_set), ticket)
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
    return all(errors)


def get_field_values(tickets):
    # Create dataset for each column
    num_fields = len(tickets[0])
    field_values = []
    for i in range(num_fields):
        field_values.append([x[i] for x in tickets])
    field_values = [sorted(x) for x in field_values]
    return field_values


def check_list_in_prohibited(value_list, fields_rules):
    # Check if value falls outside the range of 
    # corresponding field rules
    smaller = [1 for x in value_list if x < fields_rules['low1']]
    between = [1 for x in value_list if fields_rules['high1'] < x < fields_rules['low2']]
    greater = [1 for x in value_list if x > fields_rules['high2']]

    if smaller or between or greater:
        return True
    else:
        return False


def remove_fields(field_list, not_fields):
    # Eliminate fields which cannot be contained by each fields list
    return [x for x in field_list if x not in not_fields]


def find_single_field(field_order):
    # Find which list is made of single item
    for idx, x in enumerate(field_order):
        if len(x) == 1:
            index = idx
            single_field = x[0]
    return single_field, index 


def find_field(field_rules, field_values):
    # Find order of fields
    fields = list(field_rules.keys())
    fields_prohibited = {}

    nums = list(range(0, 1001)) # Largest field value HARDCODED to 1000

    for key, val in field_rules.items():
        num1 = list(range(val['low1'], val['high1'] + 1))
        num1.extend(list(range(val['low2'], val['high2'] + 1)))
        fields_prohibited[key] = [x for x in nums if x not in num1]

    field_order = [None for _ in fields]
    # Find which fields each dataset do not belong to
    not_fields_list = []
    for value_list in field_values:
        not_fields = []
        for field in fields:
            if check_list_in_prohibited(value_list, field_rules[field]):
                not_fields.append(field)
        not_fields_list.append(not_fields)
    
    # Eliminate one after the other to find the field
    # of each dataset
    while len(fields) > 0:
        field_order_list = [remove_fields(fields, x) for x in not_fields_list]
        single_item, index = find_single_field(field_order_list)
        fields.remove(single_item)
        field_order[index] = single_item
    return field_order


def main2(file_name='Day_16/16_input.txt'):
    with open(file_name, 'r') as f:
        file_contents = f.readlines()
    field_rules, self_ticket, other_tickets = file_parse(file_contents)
    allowed_nums = parse_field_values(field_rules)

    errors_free_tickets = []
    for idx, tkt in enumerate(other_tickets):
        if validate_ticket2(allowed_nums, tkt):
            # Append if ticket does not contain error
            errors_free_tickets.append(tkt)

    field_values_list = get_field_values(errors_free_tickets)
    field_order = find_field(field_rules, field_values_list)

    dep_mul = 1
    # Multiply all fields containing 'departure'
    for idx, field in enumerate(field_order):
        if field.startswith('departure'):
            dep_mul = dep_mul * self_ticket[idx]
    print(dep_mul)

 
if __name__ == '__main__':
    start1 = time.time()
    # main(file_name='Day_16/16_test.txt')
    main()
    print(f'Part One finished in {time.time() - start1}')

    start2 = time.time()
    # main2(file_name='Day_16/16_test2.txt')
    main2()
    print(f'Part Two finished in {time.time() - start2}')