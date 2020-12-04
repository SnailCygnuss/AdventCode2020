import re

file_name = 'Day_2/2_input.txt'

with open(file_name, 'r') as f:
    text_lines = f.readlines()


def check_pass(limit_1, limit_2, c, pwd):
    matched_char = re.findall(c, pwd)
    n = len(matched_char)
    if n >= limit_1 and n <= limit_2:
        return True
    else:
        return False


count = 0
for text_line in text_lines:
    limit, char, password = text_line.split()
    limit = limit.split('-')
    limit = [int(x) for x in limit]
    if check_pass(limit[0], limit[1], char.rstrip(':'), password.strip()):
        count = count + 1
    
print(count)