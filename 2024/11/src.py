#!/usr/bin/env python3

import sys
from functools import lru_cache

with open(sys.argv[1], "r") as f:
    input = [int(x) for l in f.readlines() for x in l.strip().split()]


@lru_cache(maxsize=None)
def count(x, depth):
    if depth == 0:
        return 1
    if x == 0:
        return count(1, depth - 1)
    x = str(x)
    if len(x) % 2 == 0:
        middle = len(x) // 2
        left = count(int(x[:middle]), depth - 1)
        right = count(int(x[middle:]), depth - 1)
        return left + right
    return count(int(x) * 2024, depth - 1)


print(f"Solution 1: {sum(count(x, 25) for x in input)}")
print(f"Solution 2: {sum(count(x, 75) for x in input)}")
