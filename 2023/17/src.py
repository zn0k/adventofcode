#!/usr/bin/env python3

import sys
from queue import PriorityQueue
from collections import defaultdict
from math import inf

with open(sys.argv[1], "r") as f:
  tiles = [[int(x) for x in y.strip()] for y in f.readlines()]

directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
max_x, max_y = len(tiles[0]) - 1, len(tiles) - 1
target = (max_x, max_y)

def inbounds(x, y):
  if x < 0 or x > max_x: return False
  if y < 0 or y > max_y: return False
  return True

def solve(target_fn, straight_fn, turn_fn):
  pq = PriorityQueue()
  # start with the two possible moves from (0, 0)
  pq.put((tiles[1][0], (0, 1), ((0, 1), 1)))
  pq.put((tiles[0][1], (1, 0), ((1, 0), 1)))
  visited = set()

  while not pq.empty():
    (cost, (x, y), ((dx, dy), n)) = pq.get()
    
    if target_fn(x, y, n): return cost

    current = ((x, y), ((dx, dy), n))
    if current in visited: continue
    visited.add(current)

    # can we still go straight?
    if straight_fn(n):
      new_x, new_y = x + dx, y + dy
      if inbounds(new_x, new_y):
        pq.put((cost + tiles[new_y][new_x], (new_x, new_y), ((dx, dy), n + 1)))

    # turn
    if turn_fn(n):
      for pdx, pdy in directions:      # proposed new directions
        if (pdx, pdy) != (dx, dy):     # already covered going the same way
          if (pdx, pdy) != (-dx, -dy): # can't turn around
            new_x, new_y = x + pdx, y + pdy
            if inbounds(new_x, new_y):
              pq.put((cost + tiles[new_y][new_x], (new_x, new_y), ((pdx, pdy), 1)))

val = solve(lambda x, y, n: (x, y) == target,
            lambda n: n < 3,
            lambda n: True)

print(f"Solution 1: {val}")

val = solve(lambda x, y, n: (x, y) == target and n >= 4,
            lambda n: n < 10,
            lambda n: n >= 4)

print(f"Solution 2: {val}")