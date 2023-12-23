#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
  tiles = [list(line.strip()) for line in f.readlines()]

directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

rocks = set()
garden = set()
start = (0, 0)
for y in range(len(tiles)):
  for x in range(len(tiles[0])):
    match tiles[y][x]:
      case ".":
        garden.add((x, y))
      case "#":
        rocks.add((x, y))
      case "S":
        garden.add((x, y))
        start = (x, y)

current = set()
current.add(start)
for _ in range(64):
  next = set()
  for x, y in current:
    for dx, dy in directions:
      c = (x + dx, y + dy)
      if c in garden:
        next.add(c)
  current = next

print(f"Solution 1: {len(current)}")