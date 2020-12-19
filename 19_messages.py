import time
import re


def process_rule_regex(rule_no, rule_dict, processed_recursive={}):

    if rule_no in processed_recursive:
        return processed_recursive[rule_no]
    elif len(rule_dict[rule_no].strip('"')) == 1:
        processed_recursive[rule_no] = rule_dict[rule_no].strip('"')
    else:
        regex_pat = '('
        rule_string = rule_dict[rule_no].split()
        for rule in rule_string:
            if rule == '|':
                regex_pat = regex_pat + ')' + '|' + '('
                continue
            regex_pat = regex_pat + '(' + process_rule_regex(rule, rule_dict, processed_recursive) + ')'
        regex_pat = regex_pat + ')'
        processed_recursive[rule_no] = regex_pat
    return processed_recursive[rule_no]


def read_rules(f_obj):
    # Read all the rules
    rule_dict = {}
    line = next(f_obj)
    while line != '\n':
        # print(line)
        rule_num, rules = line.split(':')
        rules = rules.strip()
        rule_dict[rule_num] = rules
        line = next(f_obj)
    return rule_dict, f_obj


def main1(file_name='Day_19/19_input.txt', part=1):
    global PROCESSED_RULES
    processed_recursive = {}
    print(file_name)
    f_obj = open(file_name, 'r')
    allowed_count = 0

    rule_dict, f_obj = read_rules(f_obj)    

    # For part Two update the rules
    if part == 2:
        rule_8 = process_rule_regex('8', rule_dict)
        rule_8 = rule_8 + '+'
        rule_dict['11'] = ('| '.join(['42 '*i + '31 '*i for i in range(1, 10)]))
        processed_recursive['8'] = rule_8
        allowed_messages = process_rule_regex('0', rule_dict, processed_recursive=processed_recursive)
    
    # Process rules for Rule '0' as per problem
    else:
        allowed_messages = process_rule_regex('0', rule_dict)
    allowed_patterns = re.compile(allowed_messages)
    # Read messages and count matching messages
    line = next(f_obj)
    while True:
        if allowed_patterns.fullmatch(line.strip()):
            allowed_count = allowed_count + 1
        try:
            line = next(f_obj)
        except StopIteration:
            break

    f_obj.close()
    return allowed_count



def testcases():
    PROCESSED_RULES = {}
    ipt_text = '''0: 4 1 5
                  1: 2 3 | 3 2
                  2: 4 4 | 5 5
                  3: 4 5 | 5 4
                  4: "a"
                  5: "b
                  6: 5 4'''
    opt_text = '''['aaaabb', 'aaabab', 'abbabb', 'abbbab', 'aabaab', 'aabbbb', 'abaaab', 'ababbb']
                  ['aaab', 'aaba', 'bbab', 'bbba', 'abaa', 'abbb', 'baaa', 'babb']
                  ['aa', 'bb']
                  ['ab', 'ba']
                  ['a']
                  ['b']
                  ['ba']'''
    
    input_text = ipt_text.split('\n')
    output_text = opt_text.split('\n')
    rule_dict = {}
    rule_out = {}
    for inp, opt in zip(input_text, output_text):
        rule_num, rule_string = inp.split(':')
        rule_dict[rule_num.strip()] = rule_string.strip()
        rule_out[rule_num.strip()] = eval(opt.strip())
            
    rule_res = {}
    for key in rule_dict:
        rule_res[key] = process_rule_regex(key, rule_dict)
    print(rule_res)
    for key in rule_res:
        for out in rule_out[key]:
            pattern = re.compile(rule_res[key])
            assert(pattern.fullmatch(out))
    print('Test Passed')


if __name__ == '__main__':
    start1 = time.time()
    # testcases()
    # out = main1(file_name='Day_19/19_test.txt')
    out = main1()
    print(out)
    print(f'Part One finished in {time.time() - start1}')
    

    # Delete all values in PROCESSED_RULES beofre running each function
    start2 = time.time()
    # test_part2()
    # out = main1('Day_19/19_test2.txt')
    # out = main1('Day_19/19_test2.txt', part=2)
    out = main1(part=2)
    print(out)
    print(f'Part Two finished in {time.time() - start2}')