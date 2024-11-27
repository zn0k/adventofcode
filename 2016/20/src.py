#!/usr/bin/env python3

import sys
from functools import reduce

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return list(map(lambda x: tuple(map(int, x.split("-"))), lines))

data = readInput()
data = sorted(data)

current = list(filter(lambda x: x[0] == 0, data))[0]

while True:
  new = list(filter(lambda x: x[0] <= current[1] + 1 and x[1] >= current[1] + 1, data))
  if len(new) == 0:
    break
  current = new[0]

print(f"Solution 1: {current[1] + 1}")

merged = [data[0]]
for (start, end) in data[1:]:
  if merged[-1][1] >= start - 1:
    merged[-1] = (merged[-1][0], max(merged[-1][1], end))
  else:
    merged.append((start, end))

def gap(a, b):
    c = a[0] + max(b[0] - a[1] - 1, 0)
    return (c, b[1])

allowed = reduce(gap, merged, (0, 0))[0]
allowed += 4294967295 - merged[-1][1]
print(f"Solution 2: {allowed}")
