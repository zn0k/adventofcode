#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
    data = f.read()

ranges, ingredients = data.split("\n\n")
ingredients = [int(x) for x in ingredients.split("\n")]
# ingredients = [1, 5, 8, ...]
ranges = [x for x in ranges.split("\n")]
ranges = [list(map(int, x.split("-"))) for x in ranges]
# ranges = [(3, 5), (10, 14), ...]

# function to determine if a value is in any of the ranges
def in_range(i):
    for start, end in ranges:
        if i >= start and i <= end:
            return True
    return False

# True is 1, False is 0, so map the function and sum
solution1 = sum(map(in_range, ingredients))
print(f"Solution 1: {solution1}")

# merge them so there are no overlaps. bog standard algorithm
# first, sort the ranges by starting number
ranges = sorted(ranges, key=lambda x: x[0])
merged = []
for r in ranges:
    # if the list of merged ranges is empty or the
    # current range doesn't overlap with the last
    # element, simply add it as a new range
    if not merged or r[0] > merged[-1][1]:
        merged.append(r)
    else:
        # there is overlap, merge by resetting the end
        # of the last merged range to the max of the two
        merged[-1][1] = max(r[1], merged[-1][1])

# and now sum up the number of elements in the merged ranges
solution2 = sum(map(lambda x: x[1] - x[0] + 1, merged))
print(f"Solution 2: {solution2}")