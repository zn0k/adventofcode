#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f: 
  lines = [l.strip() for l in f.readlines()]
  lines = [[int(x) for x in l.split()] for l in lines]

def isValid(row):
  ps = list(zip(row, row[1:]))
  dec = (p[0] > p[1] for p in ps)
  inc = (p[0] < p[1] for p in ps)
  gradual = (abs(p[0] - p[1]) > 0 and abs(p[0] - p[1]) <= 3 for p in ps)
  return (all(dec) or all(inc)) and all(gradual)

def isValidDampened(row):
  return any(isValid(row[0:i] + row[i+1:]) for i in range(len(row)))

valid = list(filter(isValid, lines))
print(f"Solution 1: {len(valid)}")

valid = list(filter(isValidDampened, lines))
print(f"Solution 2: {len(valid)}")
