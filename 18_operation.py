import time
import operator


def evaluate_expresion(expression):
    for char in expression:
        if char == ' ':
            continue


def find_bracket_end2(expression):
    opening_count = 1
    for idx, char in enumerate(expression[1:]):
        if char == '(':
            opening_count = opening_count + 1
        elif char == ')':
            if opening_count > 1:
                opening_count = opening_count - 1
            else:
                close_pos = idx+1
                break
    # Find value of expression inside the bracketes
    value = calculate_expression(expression[1:close_pos])
    return value, close_pos


def calculate_expression(expression):
    
    expression = expression.split(' ')
    l = 0
    r = 0

    operation = operator.add
    for char in expression:
        try:
            val = int(char)
            r = val
            l = operation(l, r)
        except ValueError:
            if char == ' ':
                continue
            elif char == '+':
                operation = operator.add 
            elif char == '*':
                operation = operator.mul
    # print(l)
    return l


def calculate_expression2(expression):
    # Remove all plus signs
    plus_loc = expression.find('+')
    while plus_loc != -1:
        expression = expression.split()
        plus_loc = expression.index('+')
        plus_val = int(expression[plus_loc-1]) + int(expression[plus_loc+1])
        expression = expression[:plus_loc-1] + [str(plus_val)] + expression[plus_loc+2:]
        expression = ' '.join(expression)
        plus_loc = expression.find('+')

    val = calculate_expression(expression)
    return val


def find_bracket_end(expression):
    opening_count = 1
    open_idx = expression.find('(')
    for idx, char in enumerate(expression[open_idx+1:], start=open_idx+1):
        if char == '(':
            opening_count = opening_count + 1
        elif char == ')':
            if opening_count > 1:
                opening_count = opening_count - 1
            else:
                close_pos = idx
                break
    return close_pos


def evaluate(expression, part=1):
    # Check if there are any brackets
    open_bracket = expression.find('(')
    while open_bracket != -1:
        # Find corresponding closing bracket index
        close_bracket = find_bracket_end(expression)
        # Calculate value of bracket
        if part == 2:
            bracket_val = evaluate(expression[open_bracket+1:close_bracket], part=2)
        else:
            bracket_val = evaluate(expression[open_bracket+1:close_bracket])
        # Replace brackets in the expression
        expression = expression[:open_bracket] + str(bracket_val) + expression[close_bracket+1:]
        # print(expression)
        # Check if there are more brackets and repeat
        open_bracket = expression.find('(')

    # print(expression)
    # input()
    if part == 2: 
        val = calculate_expression2(expression)
    else:
        val = calculate_expression(expression)
    # print(val)
    return val


def main(file_name='Day_18/18_input.txt'):
    with open(file_name, 'r') as f:
        input_data = list(map(str.strip, f.readlines()))

    total = 0
    for exp in input_data:
        total = total + evaluate(exp)

    print(total)


def main2(file_name='Day_18/18_input.txt'):
    with open(file_name, 'r') as f:
        input_data = list(map(str.strip, f.readlines()))

    total = 0
    for exp in input_data:
        total = total + evaluate(exp, part=2)

    print(total)


def testcases():
    print(calculate_expression('4 * 11'))
    evaluate('1 + (2 * 3) + (4 * (5 + 6))')


def testcases2():
    print(evaluate('1 + 2 * 3 + 4 * 5 + 6', part=2))
    print(evaluate('1 + (2 * 3) + (4 * (5 + 6))', part=2))
    print(evaluate('2 * 3 + (4 * 5)', part=2))
    print(evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)', part=2))
    print(evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', part=2))
    print(evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', part=2))


if __name__ == '__main__':
    start1 = time.time()
    # main(file_name='Day_18/18_test.txt')
    # testcases()
    # main()
    print(f'Part One finished in {time.time() - start1}')

    start2 = time.time()
    # testcases2()
    main2()
    print(f'Part Two finished in {time.time() - start2}')