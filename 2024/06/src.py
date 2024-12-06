#!/usr/bin/env python3

import sys
import numpy as np

with open(sys.argv[1], "r") as f: 
  lines = [l.strip() for l in f.readlines()]

# find the coordinates of the starting position
pos = [[line.index("^") if "^" in line else -1] for line in lines]
pos = (pos[np.argmax(pos)][0], int(np.argmax(pos)))

start = pos

# turn everything into a list of lists
ground = np.array([[c for c in line] for line in lines])

# keep track of visited coordinates
# do that in a list in case part 2 has anything to do with time steps
visited = [start]

# function to rotate left the position, matrix, and positions visited so far
def rotate(m, v, p):
  rot_pos = lambda p: (p[1], m.shape[1] - 1 - p[0])
  p = rot_pos(p)
  v = [rot_pos(x) for x in v]
  m = np.rot90(m=m, k=1)
  return (m, v, p)

# keep walking up until we hit an obstacle, then turn right by rotating 
# the map left. if we ever walk off to the top (x < 0), we're done
rotated = 0
while pos[1] > 0:
  if ground[pos[1] - 1][pos[0]] == "#":
    ground, visited, pos = rotate(ground, visited, pos)
    rotated += 1
  else:
    pos = (pos[0], pos[1] - 1)
    visited.append(pos)

print(f"Solution 1: {len(set(visited))}")

# turn everything the right way again for part 2
for _ in range(rotated % 4): ground, visited, pos = rotate(ground, visited, pos)

# lookup for rotating directions. up -> left, left -> down, etc
dl = {(0, -1): (-1, 0), (-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1)}

# function to rotate left the position, matrix, and positions visited so far
# this time, account for directionality
def rotate(m, v, p, d):
  def rot_pos(pt):
    p, d = pt
    return ((p[1], m.shape[1] - 1 - p[0]), dl[d])
  p, _ = rot_pos((p, d))
  v = [rot_pos(pt) for pt in v]
  m = np.rot90(m=m, k=1)
  return (m, v, p, d)

# naive solution where we just try every possible position
# it only makes sense to add obstructions to places where the
# guard would normally walk, so go through the unique tiles visited
variants = []
for x, y in set(visited):
    variant = np.array([[c for c in line] for line in lines])
    if variant[y][x] in "#^": continue # skip variant, can't place new obstruction
    variant[y][x] = "#" # place new obstruction
    direction = (0, -1) # start facing up
    pos = start
    visited = [(start, direction)]
    # start walking
    while pos[1] > 0:
        if variant[pos[1] - 1][pos[0]] == "#":
            variant, visited, pos, direction = rotate(variant, visited, pos, direction)
        else:
            pos = (pos[0], pos[1] - 1)
        if (pos, direction) in visited:
            # we've been on this tile facing this way before, that's a loop
            # record it and break
            variants.append((x, y))
            break
        else:
            visited.append((pos, direction))

print(f"Solution 2: {len(variants)}")