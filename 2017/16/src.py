#!/usr/bin/env python3

import sys
import string
from collections import deque

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines[0].split(",")

def dance(seed, steps):
  programs = deque(seed)
  for cmd in steps:
    match cmd[0]:
      case "s":
        programs.rotate(int(cmd[1:]))
      case "x":
        a, b = [int(x) for x in cmd[1:].split("/")]
        programs[a], programs[b] = programs[b], programs[a]
      case "p":
        a, b = [programs.index(x) for x in cmd[1:].split("/")]
        programs[a], programs[b] = programs[b], programs[a]
  return "".join(programs)

steps = readInput()

start = string.ascii_lowercase[0:16]
part1 = dance(start, steps)

print(f"Solution 1: {part1}")

repeats_after = 0
order = start
while True:
  repeats_after += 1
  order = dance(order, steps)
  if order == start:
    break

order = start
for _ in range(1_000_000_000 % repeats_after):
  order = dance(order, steps)

print(f"Solution 2: {order}")