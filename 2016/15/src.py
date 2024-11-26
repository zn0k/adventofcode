#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  lines = [l.split() for l in lines]
  return list(map(lambda x: (int(x[3]), int(x[11].rstrip("."))), lines))

data = readInput()

def run():
  t = 0
  while True:
    found = True
    for i, (positions, start_position) in enumerate(data):
      disc_position = i + 1 + t + start_position
      if (i + 1 + t + start_position) % positions != 0:
        found = False
        break
    if found:
      return t
    t += 1

t = run()
print(f"Solution 1: {t}")

data.append((11, 0))
t = run()
print(f"Solution 2: {t}")