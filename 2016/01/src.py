#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines[0].split(", ")

data = readInput()

# x, y coordinate on grid
position = (0, 0)
# directionality on number lines
direction = (1, 0)

# turn left or right, which aligns the directionality
def turn(d, t):
   match t:
      case "R":
        match d:
            case (1, 0): return (0, 1)
            case (0, 1): return (-1, 0)
            case (-1, 0): return (0, -1)
            case (0, -1): return (1, 0)
      case "L":
        match d:
           case (1, 0): return (0, -1)
           case (0, -1): return (-1, 0)
           case (-1, 0): return (0, 1)
           case (0, 1): return (1, 0)

# move by the given number of tiles
def move(p, d, s):
   return (p[0] + d[0] * s, p[1] + d[1] * s)

for step in data:
  # first, turn
  direction = turn(direction, step[0])
  distance = int(step[1:])
  # then move
  position = (position[0] + direction[0] * distance, position[1] + direction[1] * distance)

# get the manhattan distance
md = abs(position[0]) + abs(position[1])
print(f"Solution 1: {md}")

# reset
position = (0, 0)
direction = (1, 0)
visited = [(0, 0)]
found = False

for step in data:
  # first, turn
  direction = turn(direction, step[0])
  distance = int(step[1:])
  # record intermediate positions
  for d in range(1, distance + 1):
    intermediate = (position[0] + direction[0] * d, position[1] + direction[1] * d)
    # check if we've been here before
    if intermediate in visited:
      # yes, print it and flag
      md = abs(intermediate[0]) + abs(intermediate[1])
      print(f"Solution 2: {md}")
      found = True
    visited.append(intermediate)
  if found == True: break
  # then finalize moving to the new position
  position = intermediate
