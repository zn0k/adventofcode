#!/usr/bin/env python3

import sys
from collections import deque

with open(sys.argv[1], "r") as f:
  tiles = [list(line.strip()) for line in f.readlines()]

directions = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}

moves = {
  "\\": {"R": ["D"], "D": ["R"], "L": ["U"], "U": ["L"]},
  "/":  {"R": ["U"], "D": ["L"], "L": ["D"], "U": ["R"]},
  "-":  {"R": ["R"], "D": ["R", "L"], "L": ["L"], "U": ["R", "L"]},
  "|":  {"R": ["D", "U"], "D": ["D"], "L": ["D", "U"], "U": ["U"]},
  ".":  {"R": ["R"], "D": ["D"], "L": ["L"], "U": ["U"]},
}

def oob(x, y):
  if x < 0: return True
  if y < 0: return True
  if x >= len(tiles[0]): return True
  if y >= len(tiles): return True
  return False

def score(start):
  seen = set()
  q = deque([start])
  while len(q):
    beam = q.popleft()
    coordinate, direction = beam
    if oob(*coordinate): continue
    if beam in seen: continue
    seen.add(beam)
    x, y = coordinate
    tile = tiles[y][x]
    for new_direction in moves[tile][direction]:
      vector = directions[new_direction]
      new_x, new_y = x + vector[0], y + vector[1]
      q.append(((new_x, new_y), new_direction))
  return len(set([x for x, _ in seen]))

print(f"Solution 1: {score(((0,0), 'R'))}")

max_x, max_y = len(tiles[0]), len(tiles)
starts = [((x, 0), "D") for x in range(max_x)] + \
         [((max_x, y), "L") for y in range(max_y)] + \
         [((x, max_y), "U") for x in range(max_x)] + \
         [((0, y), "R") for y in range(max_y)]
scores = map(score, starts)

print(f"Solution 2: {max(scores)}")