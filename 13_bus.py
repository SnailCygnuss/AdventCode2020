import time
import itertools
import operator
from functools import reduce


def iter_factors(min_number=0, factor=1):
    if min_number == 0:
        q = 0
    else:
        q = int(min_number / factor)
    nearest_number = (q * factor) + factor
    return itertools.count(start=nearest_number, step=factor)


def main(time, bus_numbers):
    bus_numbers = [int(x) for x in bus_numbers if not x == 'x']
    bus_numbers.sort()
    sieves = {}
    for s in bus_numbers:
        sieves[s] = iter_factors(time, s)
    
    while True:
        # bus = next(bus_iterator)
        arrival_times = {}
        for s in bus_numbers:
            arrival_times[s] = next(sieves[s])
        earliest_bus = min(arrival_times, key=arrival_times.get)
        if arrival_times[earliest_bus] >= time:
            wait_time = arrival_times[earliest_bus] - time
            print(f'Earliest bus is {earliest_bus} as {arrival_times[earliest_bus]}')
            print(f'{wait_time * earliest_bus}')
            break 


def departure_intervals(bus_numbers):
    interval = 0
    dep_intervals = {}
    for s in bus_numbers:
        if s == 'x':
            interval = interval + 1
        else:
            dep_intervals[int(s)] = interval
            interval = interval + 1
    max_bus_number = max(dep_intervals)
    leaving_time = dep_intervals[max_bus_number]
    for bus in dep_intervals:
        dep_intervals[bus] = dep_intervals[bus] - leaving_time
    return dep_intervals


def find_closest_departure(time, factor, side='+'):
    q = int(time / factor)
    if side == '+':
        return (q * factor) + factor - time
    else:
        return q * factor - time


def check_division(number, factor):
    if number % factor == 0:
        return True
    else:
        return False


def main2(bus_numbers):
    # Brute force method
    dep_intervals = departure_intervals(bus_numbers)
    bus_numbers = [int(x) for x in bus_numbers if not x == 'x']
    max_bus = max(bus_numbers)
    reverse_bus_numbers = sorted(bus_numbers, reverse=True)
    reverse_bus_numbers.remove(max_bus)

    max_bus_iter = iter_factors(min_number=0 , factor=max_bus)
    bus_bool = [False]
    time = 0

    while True:
        time = next(max_bus_iter)
        bus_bool = []
        for s in reverse_bus_numbers:
            if dep_intervals[s] > 0:
                nearest_time = find_closest_departure(time, s, side='+')
            else:
                nearest_time = find_closest_departure(time, s, side='-')
            if nearest_time != dep_intervals[s]:
                break
            else:
                bus_bool.append(True)
        if len(bus_bool) == len(reverse_bus_numbers) and all(bus_bool):
            break
        
    # Find dep time of first bus in list
    dep_time = int(time / bus_numbers[0]) * bus_numbers[0]
    print(dep_time)


def solve_congruence(coeff, mod):
    coeff = coeff % mod
    n = 1
    while True:
        if (coeff * n) % mod == 1:
            break
        n = n + 1
    return n


def main3(bus_numbers):
    # Chinese Remainder Theorem
    # Works on test cases but not on input. Don't know
    delays = []
    delay = 0
    for s in bus_numbers:
        if not s == 'x':
            delays.append(delay)
        delay = delay + 1
    bus_numbers = [int(x) for x in bus_numbers if not x == 'x']
    bi = list(map((lambda x, y: x - (y % x)), bus_numbers, delays))
    bi[0] = 0
    N = reduce(operator.mul, bus_numbers)
    Ni = list(map(operator.truediv, itertools.repeat(N), bus_numbers))
    xi = list(map(solve_congruence, Ni, bus_numbers))
    biNi = list(map(operator.mul, bi, Ni))
    biNixi = list(map(operator.mul, biNi, xi))
    x = sum(biNixi) % N
    print(x)


def main4(bus_numbers):
    # Searching using multiples of product.
    delays = []
    delay = 0
    for s in bus_numbers:
        if not s == 'x':
            delays.append(delay)
        delay = delay + 1
    bus_numbers = [int(x) for x in bus_numbers if not x == 'x']

    bi = list(map((lambda x, y: x - (y % x)), bus_numbers, delays))
    bi[0] = 0

    step = itertools.count(start=bus_numbers[0] + bi[0], step=bus_numbers[0])
    i = 1
    while True:
        number = next(step)
        if number % bus_numbers[i] == bi[i]:
            product = reduce(operator.mul, bus_numbers[:i+1], 1)
            step = itertools.count(start=number, step=product)
            i = i + 1
        if i >= len(bus_numbers):
            break
    print(number)


def test_cases_part_2(func=main2):
    test = [[17,'x',13,19],
            [67,7,59,61],
            [67,'x',7,59,61],
            [67,7,'x',59,61],
            [1789,37,47,1889]]
    
    for t in test:
        func(t)


def read_file():
    file_name = 'Day_13/13_test.txt'
    # file_name = 'Day_13/13_input.txt'
    with open(file_name, 'r') as f:
        txt_contents = f.readlines()

    time = int(txt_contents[0].strip())
    bus_numbers = txt_contents[1].strip().split(',')

    return time, bus_numbers


if __name__ == '__main__':
    start = time.time()
    arrival_time, available_bus_ids = read_file()
    main(arrival_time, available_bus_ids)
    print(f'Finished Part 1 in {time.time() - start}')

    # Brute Force - Not working on input data
    # start2 = time.time()
    # main2(available_bus_ids)
    # test_cases_part_2()
    # print(f'Finished Part 2 in {time.time() - start2}')

    # CRT - not working on input data
    # start3 = time.time()
    # main3(available_bus_ids)
    # test_cases_part_2(func=main3)
    # print(f'Finished Part 3 in {time.time() - start3}')

    # Efficient search
    start4 = time.time()
    main4(available_bus_ids)
    # test_cases_part_2(func=main4)
    print(f'Finished Part 4 in {time.time() - start4}')