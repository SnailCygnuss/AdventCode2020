file_name = '1_input.txt'

with open(file_name, 'r') as f:
    numbers = f.readlines()

numbers = [int(x.strip()) for x in numbers]


for idx, n1 in enumerate(numbers):
    for n2 in numbers[idx+1:]:
        if (n1 + n2) == 2020:
            print(n1, n2, n1*n2)