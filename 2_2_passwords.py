import re

file_name = 'Day_2/2_input.txt'

with open(file_name, 'r') as f:
    text_lines = f.readlines()


def check_pass(limit_1, limit_2, c, pwd):
    # print(limit_1, limit_2, c, pwd)
    pos_1_flag = False
    pos_2_flag = False
    for m in re.finditer(c, pwd):
        pos = m.end()
        if pos == limit_1:
            pos_1_flag = True
        elif pos == limit_2:
            pos_2_flag = True
    
    if all([pos_1_flag, pos_2_flag]) or all([not pos_1_flag, not pos_2_flag]):
        # print('Invalid')
        return False
    else:
        # print('Valid')
        return True


count = 0
for text_line in text_lines:
    limit, char, password = text_line.split()
    limit = limit.split('-')
    limit = [int(x) for x in limit]
    if check_pass(limit[0], limit[1], char.rstrip(':'), password.strip()):
        count = count + 1
    
print(count)
