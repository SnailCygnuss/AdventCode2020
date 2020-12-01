file_name = '1_input.txt'

with open(file_name, 'r') as f:
    numbers = f.readlines()

numbers = [int(x.strip()) for x in numbers]


for id1, n1 in enumerate(numbers):
    for id2, n2 in enumerate(numbers[id1+1:]):
        if (n1 + n2) >= 2020:
            continue
        else:
            for n3 in numbers[id2+1:]:
                if (n1 + n2 + n3) == 2020:
                    print(n1, n2, n3, n1*n2*n3)