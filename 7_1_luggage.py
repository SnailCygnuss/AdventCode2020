import re


def check_bag_containing(target_bag, rule):
    pattern = r'(.+) bags contain.*{}.*'.format(target_bag)
    # print(target_bag)
    # print(pattern)
    # print(rule)
    matching_group = re.match(pattern, rule)
    if matching_group:
        # print(matching_group)
        # print(matching_group.group(1))
        return matching_group.group(1)
    else:
        return None


def check_rules(f_name, target):
    allowed_bags = []
    with open(f_name, 'r') as f:
        for line in f:
            matched_bag = check_bag_containing(target, line.strip())
            if matched_bag:
                allowed_bags.append(matched_bag)
    return allowed_bags


def main():
    file_name = 'Day_7/7_test.txt'
    file_name = 'Day_7/7_input.txt'
    allowed_bags = check_rules(file_name, 'shiny gold')
    # print(allowed_bags)
    allowed_bags = set(allowed_bags)
    new_set = set()
    for bag in allowed_bags:
        new_set.update(check_rules(file_name, bag))
    while not set(allowed_bags).issuperset(new_set):
        new_bags_to_check = list(new_set)
        allowed_bags.update(new_set)
        new_set.clear()
        for bag in new_bags_to_check:
            new_set.update(check_rules(file_name, bag))
    
    # print(allowed_bags)
    print(len(allowed_bags))


if __name__ == '__main__':
    main()