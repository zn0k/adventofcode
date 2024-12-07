#!/usr/bin/env python3

import sys
from operator import mul, add
from itertools import product

with open(sys.argv[1], "r") as f: 
  calibrations = [l.strip().split(": ") for l in f.readlines()]
  calibrations = [(int(c[0]), list(map(int, c[1].split()))) for c in calibrations]

def isValid(c, s, ops_options):
  def calc(acc, xs, ops):
    for x, op in zip(xs, ops):
      acc = op(acc, x)
    return acc == s
  return any(calc(c[0], c[1:], op) for op in product(ops_options, repeat=len(c) - 1))
  
part1 = sum(c[0] for c in calibrations if isValid(c[1], c[0], [mul, add]))
print(f"Solution 1: {part1}")

def concat(a, b):
  return int(str(a) + str(b))

part2 = sum(c[0] for c in calibrations if isValid(c[1], c[0], [mul, add, concat]))
print(f"Solution 2: {part2}")