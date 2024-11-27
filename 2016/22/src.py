#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  lines = lines[2:]
  lines = list(map(lambda x: x.split(), lines))
  def m(x):
    return int(x[:-1])
  return [(x[0], m(x[2]), m(x[3])) for x in lines]

data = readInput()

count = 0
for a in data:
  for b in data:
    if a == b: continue
    if a[1] == 0: continue
    if b[2] < a[1]: continue
    count += 1
print(f"Solution 1: {count}")