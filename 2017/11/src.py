#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [l.split(",") for l in lines]

data = readInput()

# axial coordinates with rows and columns
# https://www.redblobgames.com/grids/hexagons/
directions = {"nw": (-1, 0), "n": (0, -1), "ne": (1, -1), "se": (1, 0), "s": (0, 1), "sw": (-1, 1)}

# calculate distance using formula for axial coordinates
def distance(a, b):
  return max(abs(b[1] - a[1]), abs(b[0] - a[0]), abs((-1 * a[0] - a[1]) - (-1 * b[0] - b[1])))

for line in data:
  start = (0, 0)
  pos = (0, 0)
  d_max = 0
  # walk
  for step in line:
    dx, dy = directions[step]
    pos = (pos[0] + dx, pos[1] + dy)
    # calculate distance
    d = distance(start, pos)
    # store maximum seen distance
    d_max = max(d, d_max)
  print(f"Solution 1: {d}")
  print(f"Solution 2: {d_max}")