#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip("\n") for l in f.readlines()]
  return lines

data = readInput()

def next_turn(pos, dir, to_find):
  dx, dy = dir
  x, y = pos
  waypoints = []
  steps = 0
  while True:
    x, y = (x + dx, y + dy)
    steps += 1
    if data[y][x].isalpha():
      waypoints.append(data[y][x])
      to_find.remove(data[y][x])
    if len(to_find) == 0:
      return (None, waypoints, to_find, steps)
    if data[y][x] == "+":
      return ((x, y), waypoints, to_find, steps)
  
c = (data[0].index("|"), 0)
d = (0, 1)
waypoints = []
steps = 0

to_find = [x for row in data for x in row if x.isalpha()]

while True:
  c, w, to_find, s = next_turn(c, d, to_find)
  waypoints += w
  steps += s
  if c is None: break
  x, y = c
  if d in [(0, -1), (0, 1)]:
    for dx, dy in [(-1, 0), (1, 0)]:
      if x + dx < 0 or x + dx >= len(data[y]): 
        continue
      if data[y + dy][x + dx] in ["-", "+"] or data[y + dy][x + dx].isalpha(): 
        d = (dx, dy)
  else:
    for dx, dy in [(0, -1), (0, 1)]:
      if y + dy < 0 or y + dy >= len(data): 
        continue
      if data[y + dy][x + dx] in ["|", "+"] or data[y + dy][x + dx].isalpha(): 
        d = (dx, dy)

waypoints = "".join(waypoints)

print(f"Solution 1: {waypoints}")
print(f"Solution 2: {steps + 1}")