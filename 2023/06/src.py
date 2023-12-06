#!/usr/bin/env python3

import sys
from functools import reduce
from operator import mul

def parseLine(line):
  return list(map(int, line.strip().split()[1:]))

with open(sys.argv[1], "r") as f:
  lines = f.readlines()
  times = parseLine(lines[0])
  distances = parseLine(lines[1])

def generateWins(duration, distanceToBeat):
  wins = 0
  for hold in range(duration):
    if ((duration - hold) * hold) > distanceToBeat: wins += 1
  return wins

wins = map(lambda x: generateWins(times[x], distances[x]), range(len(times)))
ways = reduce(mul, wins, 1)

print(f"Solution 1: {ways}")

def concat(nums):
  return int("".join(map(str, nums)))

print(f"Solution 2: {generateWins(concat(times), concat(distances))}")