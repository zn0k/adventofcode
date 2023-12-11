#!/usr/bin/env python3

import sys
from itertools import combinations

with open(sys.argv[1], "r") as f:
  tiles = [list(line.strip()) for line in f.readlines()]

# track empty rows, columns, and galaxy coordinates
empty_h = []
empty_v = [False for _ in range(len(tiles))]
galaxies = set()

for y in range(len(tiles)):
  if tiles[y].count(".") == len(tiles[0]):  # all dots, empty row
    empty_h.append(y)                       # track that y coordinate
  for x in range(len(tiles[0])):
    if tiles[y][x] == "#":                  # it's a galaxy
      empty_v[x] = True                     # mark its column
      galaxies.add((x, y)) 
# pull out the columns we've not seen galaxies in
empty_v = [idx for idx, val in enumerate(empty_v) if not val] 

# manhattan distance
def md(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

# number of empty horizontals and verticals between a and b
# space expands by that much since each of those is doubled
def expansion(a, b, factor):
  ax, ay = a
  bx, by = b
  fst, snd = (ax, bx) if ax > bx else (bx, ax)
  dv = len(list(filter(lambda x: fst > x > snd, empty_v))) * (factor - 1)
  fst, snd = (ay, by) if ay > by else (by, ay)
  dh = len(list(filter(lambda y: fst > y > snd, empty_h))) * (factor - 1)
  return dv + dh

# actual distance is manhattan + expansion
def distance(a, b, factor):
  return md(a, b) + expansion(a, b, factor=factor)

distances = map(lambda c: distance(*c, factor=2), combinations(galaxies, 2))
print(f"Solution 1: {sum(distances)}")

distances = map(lambda c: distance(*c, factor=1_000_000), combinations(galaxies, 2))
print(f"Solution 2: {sum(distances)}")