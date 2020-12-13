import time
import itertools


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
    # max_bus_number = max(bus_numbers)
    # max_time = time + max_bus_number
    # bus_iterator = itertools.cycle(bus_numbers)
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
    # print(dep_intervals)
    max_bus_number = max(dep_intervals)
    leaving_time = dep_intervals[max_bus_number]
    for bus in dep_intervals:
        dep_intervals[bus] = dep_intervals[bus] - leaving_time
    # print(dep_intervals)
    return dep_intervals


def find_closest_departure(time, factor, side='+'):
    q = int(time / factor)
    if side == '+':
        return (q * factor) + factor - time
    else:
        return q * factor - time


def main2(bus_numbers):
    dep_intervals = departure_intervals(bus_numbers)
    bus_numbers = [int(x) for x in bus_numbers if not x == 'x']
    max_bus = max(bus_numbers)
    # print(bus_numbers)
    reverse_bus_numbers = sorted(bus_numbers, reverse=True)
    # print(reverse_bus_numbers)
    reverse_bus_numbers.remove(max_bus)

    # max_bus_iter = iter_factors(min_number=max_bus , factor=max_bus)
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


def test_cases_part_2():
    test = [[17,'x',13,19],
            [67,7,59,61],
            [67,'x',7,59,61],
            [67,7,'x',59,61],
            [1789,37,47,1889]]
    
    for t in test:
        main2(t)


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
    # print(arrival_time, available_bus_ids)
    main(arrival_time, available_bus_ids)
    print(f'Finished Part 1 in {time.time() - start}')

    start2 = time.time()
    main2(available_bus_ids)
    test_cases_part_2()
    print(f'Finished Part 2 in {time.time() - start2}')