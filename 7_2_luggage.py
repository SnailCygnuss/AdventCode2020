import re


def check_number_of_bags_inside(target_bag):
    f_name = 'Day_7/7_test.txt'
    f_name = 'Day_7/7_input.txt'

    pattern = r'{} bags contain(.*)'.format(target_bag)
    with open(f_name, 'r') as f:
        for line in f:
            # Find rule corresponding to target_bag
            match = re.match(pattern, line.strip())
            if match:
                break
    contained_bags = match.group(1).strip()
    # print(contained_bags)
    no_bag_pattern = r'no other bags'
    if re.match(no_bag_pattern, contained_bags):
        # If rule for target_bag contains 'no other bags' return 0
        return 0
    else:
        # Find the other bags in target_bag rule
        contained_bags_qty_name = contained_bags.split(',')
        contained_bags_qty_name = [x.strip('. ') for x in contained_bags_qty_name]
        # print(contained_bags_qty_name)
        qty_pattern = r'(\d+) ([\w ]+) bag'
        other_bag_quantity = [] # List to store other bags qty
        for contained_bag_qty_name in contained_bags_qty_name:
            qty, bag = re.match(qty_pattern, contained_bag_qty_name).groups()
            other_bag_quantity.append((int(qty), bag))
        
        # print(other_bag_quantity)
        return sum([x[0] + (x[0]*check_number_of_bags_inside(x[1])) for x in other_bag_quantity])


def main():
    bag = 'shiny gold'
    num_bags = check_number_of_bags_inside(bag)
    print(num_bags)


if __name__ == '__main__':
    main()
