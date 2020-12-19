import time
import itertools


PROCESSED_RULES = {}
def process_rule(rule_no: str, rule_dict: dict) -> str:
    
    rule_string = rule_dict[rule_no]

    if rule_no in PROCESSED_RULES:
        return PROCESSED_RULES[rule_no]
    elif len(rule_string.strip('"')) == 1:
        PROCESSED_RULES[rule_no] = [rule_string.strip('"')]
        return PROCESSED_RULES[rule_no]
    else:
        try:
            l_rule, r_rule = list(map(str.strip, rule_string.split('|')))
        except ValueError:
            l_rule = rule_string.strip()
            r_rule = ''

        l_rule = l_rule.split()
        r_rule = r_rule.split()

        processed_l_rule = ['']
        for rule in l_rule:
            new_rules = []
            processed_rule = process_rule(rule, rule_dict)
            for x, y in itertools.product(range(len(processed_l_rule)), 
                                          range(len(processed_rule))):
                new_rules.append(processed_l_rule[x] + processed_rule[y])
            processed_l_rule = new_rules

        processed_r_rule = ['']
        for rule in r_rule:
            new_rules = []
            processed_rule = process_rule(rule, rule_dict)
            for x, y in itertools.product(range(len(processed_r_rule)), 
                                          range(len(processed_rule))):
                new_rules.append(processed_r_rule[x] + processed_rule[y])
            processed_r_rule = new_rules

        complete_rules = [*processed_l_rule, *processed_r_rule]
        PROCESSED_RULES[rule_no] = complete_rules
        return PROCESSED_RULES[rule_no]
        # rule_list = rule_string.split()
        # complete_rule = []
        # processed_rule1 = []
        # processed_rule2 = []
        # for rule in rule_list:
        #     if rule != '|':
        #         # Get processed rule
        #         rule_value = process_rule(rule, rule_dict)
        #         if len(rule_value) == 1:
        #             processed_rule1.append(rule_value[0])
        #         else:
        #             processed_rule1.append(rule_value[0])
        #             processed_rule2.append(rule_value[1])
        #     else:
        #         processed_rule1 = ''.join(processed_rule1)
        #         complete_rule.append(processed_rule1)
        #         processed_rule1 = []
        # # print(processed_rule1)
        # # print(processed_rule2)
        # processed_rule1 = ''.join(processed_rule1)
        # processed_rule2 = ''.join(processed_rule2)
        # complete_rule.append(processed_rule1)
        # if processed_rule2:
        #     complete_rule.append(processed_rule2)
        # PROCESSED_RULES[rule_no] = complete_rule
        # return PROCESSED_RULES[rule_no]
    

def process_rules(rule_dict):
    processed_rule_dict = {}
    # Find keys with single alpha char
    for rule_num, rule in rule_dict.items():
        if '"' in rule:
            processed_rule = rule.strip('"')
            processed_rule_dict[int(rule_num)] = processed_rule
    print(processed_rule_dict)
    # Remove rule_nums with single alpha char


def main1(file_name='Day_19/19_input.txt'):
    f_obj = open(file_name, 'r')
    zero_matches = 0    

    # Read all the rules
    rule_dict = {}
    line = next(f_obj)
    while line != '\n':
        print(line)
        rule_num, rules = line.split(':')
        rules = rules.strip()
        rule_dict[rule_num] = rules
        line = next(f_obj)
    print(rule_dict)
    # Process rules
    process_rules(rule_dict)
    # Read messages and count matching messages
    f_obj.close()
    return zero_matches


def testcases():
    input_text = '''0: 4 1 5
                    1: 2 3 | 3 2
                    2: 4 4 | 5 5
                    3: 4 5 | 5 4
                    4: "a"
                    5: "b
                    6: 5 4'''
    input_text = input_text.split('\n')
    rule_dict = {}
    for inp in input_text:
        rule_num, rule_string = inp.split(':')
        rule_dict[rule_num.strip()] = rule_string.strip()
    # print(rule_dict)
    print(process_rule('4', rule_dict))
    print(process_rule('5', rule_dict))
    print(process_rule('6', rule_dict))
    print(process_rule('3', rule_dict))
    print(process_rule('2', rule_dict))
    print(process_rule('1', rule_dict))
    print(process_rule('0', rule_dict))


if __name__ == '__main__':
    start1 = time.time()
    testcases()
    # main1(file_name='Day_19/19_test.txt')
    # main1()
    print(f'Part One finished in {time.time() - start1}')
