#!/usr/bin/env python3

import sys
from functools import reduce

with open(sys.argv[1], "r") as f:
  lines = [[int(x) for x in line.split()] for line in f.readlines()]

def predict(vals):
  last_digits = [vals[-1]]
  while(any(vals)):
    vals = list(map(lambda x: x[1] - x[0], zip(vals, vals[1:])))
    last_digits.append(vals[-1])
  return sum(last_digits)

print(f"Solution 1: {sum(map(predict, lines))}")

def history(vals):
  first_digits = [vals[0]]
  while(any(vals)):
    vals = list(map(lambda x: x[1] - x[0], zip(vals, vals[1:])))
    first_digits.append(vals[0])
  while len(first_digits) > 1:
    z, y = first_digits.pop(), first_digits.pop()
    first_digits.append(y - z)
  return first_digits[0]

print(f"Solution 2: {sum(map(history, lines))}")