#!/usr/bin/env python3

import sys
from itertools import combinations

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [[int(x) for x in l.split()] for l in lines]

data = readInput()

part1 = sum([max(x) - min(x) for x in data])
print(f"Solution 1: {part1}")

expanded = [list(combinations(x, 2)) for x in data]
evenly_divisible = [list(filter(lambda x: max(x) % min(x) == 0, x))[0] for x in expanded]
part2 = sum([max(x) // min(x) for x in evenly_divisible])
print(f"Solution 2: {part2}")