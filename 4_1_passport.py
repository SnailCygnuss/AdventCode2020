# file_name = 'Day_4/4_test.txt'
file_name = 'Day_4/4_input.txt'

def check_passport_validity(credentials):
    reqd_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    found_fields = []
    for item in credentials.split():
        found_fields.append(item[:3])
        continue
    # print(found_fields)
    diff = set(reqd_fields) - set(found_fields)
    if diff == set():
        # print('found')
        return True
    elif diff == set(['cid']):
        # print('found')
        return True
    else:
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