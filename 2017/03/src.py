#!/usr/bin/env python3

import sys
import math
import numpy as np

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [int(x) for x in lines]

data = readInput()

for val in data:
  l = math.ceil(math.sqrt(val))
  if l % 2 == 0: l += 1
  corner = l ** 2
  while (corner - l) > val:
    corner -= l + 1
  md = (l // 2) + abs((l // 2 - (corner - val)))
  print(f"Solution 1: {md}")

val = data[0]

l_max = 10
floor = np.zeros((l_max, l_max))
c = [l_max // 2, l_max // 2]
floor[c[1]][c[0]] = 1
directions = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
found = False

def neighbors(c):
  s = 0
  x, y = c
  for dx, dy in directions:
    if x + dx < 0 or x + dx >= len(floor): continue
    if y + dy < 0 or y + dy >= len(floor): continue
    s += floor[y + dy][x + dx]
  if s > val:
    print(f"Solution 2: {int(s)}")
    raise Exception("found it")
  return s

try:
  for l in range(3, l_max + 1, 2):
    c[0] += 1
    floor[c[1]][c[0]] = neighbors(c)
    dx, dy = (0, -1)
    for _ in range(l - 2):
      c[0] += dx
      c[1] += dy
      floor[c[1]][c[0]] = neighbors(c)
    for dx, dy in [(-1, 0), (0, 1), (1, 0)]:
      for _ in range(l - 1):
        c[0] += dx
        c[1] += dy
        floor[c[1]][c[0]] = neighbors(c)
except:
  pass