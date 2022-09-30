from functools import reduce, partial

with open("3-1000001-100.in", "r") as f:
    numbers = [l.rstrip() for l in f]

def binary_string_to_decimal(num):
    return int("".join(num), 2)

def count_digits(counts, number):
    for index, digit in enumerate(number):
        counts[index][int(digit)] += 1
    return counts

gamma = lambda x: "0" if x[0] > x[1] else "1"
epsilon = lambda x: "0" if x[0] < x[1] else "1"

def count(items):
    return reduce(count_digits, items, [[0, 0] for x in items[0]])

counts = count(numbers)
gamma = binary_string_to_decimal(map(gamma, counts))
epsilon = binary_string_to_decimal(map(epsilon, counts))

print(f"Solution 1: {gamma * epsilon}")

def find_rating(f, default, candidates):
    position = 0
    while len(candidates) > 1:
        position_count = count(candidates)[position]
        if position_count[0] == position_count[1]:
            match = default
        else:
            match = str(position_count.index(f(position_count)))
        candidates = list(filter(lambda x: x[position] == match, candidates))
        position += 1
    return list(candidates[0])

oxygen_rating = partial(find_rating, max, "1")
co2_rating = partial(find_rating, min, "0")

oxygen = binary_string_to_decimal(oxygen_rating(numbers))
co2 = binary_string_to_decimal(co2_rating(numbers))

print(f"Solution 2: {oxygen * co2}")