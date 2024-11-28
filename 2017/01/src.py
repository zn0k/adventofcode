#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

data = readInput()

for line in data:
  line += line[0]
  sum = 0
  for a, b in zip(line, line[1:]):
    if a == b:
      sum += int(a)
  print(f"Solution 1: {sum}")

for line in data:
  sum = 0
  l = len(line)
  for i in range(l):
    j = (i + (l // 2)) % l
    if line[i] == line[j]:
      sum += int(line[i])
  print(f"Solution 2: {sum}")