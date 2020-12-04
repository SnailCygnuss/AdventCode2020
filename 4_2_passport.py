import re


# file_name = 'Day_4/4_2_test.txt'
file_name = 'Day_4/4_input.txt'

def year_check(field, value):
    '''Check if byr, iyr or eyr is valid'''
    if len(value) != 4:
        return False
    try:
        value = int(value)
    except ValueError:
        return False
    
    if field == 'byr':
        low = 1920
        high = 2002
    elif field == 'iyr':
        low = 2010
        high = 2020
    elif field == 'eyr':
        low = 2020
        high = 2030
    else:
        return False

    if value >= low and value <= high:
        return True
    else:
        return False


def hgt_check(value):
    unit = value[-2:]
    if unit not in ['cm', 'in']:
        return False
    value = int(value[:-2])
    if unit == 'cm':
        if value <= 193 and value >= 150:
            return True
    elif unit == 'in':
        if value <= 76 and value >= 59:
            return True
    return False


def hcl_check(value):
    pattern = r'^#[0-9a-f]{6}'
    if re.search(pattern, value):
        return True
    else:
        return False
    

def ecl_check(value):
    if value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return True
    else:
        return False


def pid_check(value):
    if len(value) == 9:
        return True
    else:
        return False


def check_field_validity(field, value):
    status = False
    # print(field, value)
    if field in ['byr', 'iyr', 'eyr']:
        status = year_check(field, value)
    elif field == 'hgt':
        status = hgt_check(value)
    elif field == 'hcl':
        status = hcl_check(value)
    elif field == 'ecl':
        status = ecl_check(value)
    elif field == 'pid':
        status = pid_check(value)
    elif field == 'cid':
        status = True
    return status


def check_passport_validity(credentials):
    reqd_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    found_fields = []
    for item in credentials.split():
        fd = item[:3]
        val = item[4:]
        found_fields.append(fd)
        if check_field_validity(fd, val):
            continue
        else:
            # print('Invalid')
            return False
    
    # print(found_fields)
    diff = set(reqd_fields) - set(found_fields)
    if diff == set():
        # print('found')
        return True
    elif diff == set(['cid']):
        # print('found')
        return True
    else:
        # print('invalid')
        return False


valid_count = 0
with open(file_name, 'r') as f:
    per_cred = None
    for line in f:
        if line == '\n':
            if check_passport_validity(per_cred):
                valid_count = valid_count + 1
            per_cred = None 
            continue
        else:
            if per_cred is None:
                per_cred = line.strip()
            else:
                per_cred = ' '.join((per_cred, line.strip()))
    # Check the last read credential
    if check_passport_validity(per_cred):
        valid_count = valid_count + 1
            
print(valid_count)