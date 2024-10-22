#!/usr/bin/env python3

import sys
from collections import deque
from PIL import Image
from functools import reduce

with open(sys.argv[1], "r") as f:
  instructions = [x.strip().replace("(#", "").replace(")", "").split() for x in f.readlines()]

directions = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}

# start at (0,0) in the color of that edge
current = (0, 0)
tiles = {current: instructions[0][2]}
for i in instructions:
  # get the offset based on the direction
  dx, dy = directions[i[0]]
  # dig out that many tiles
  for _ in range(int(i[1])):
    x, y = current
    current = x + dx, y + dy
    tiles[current] = i[2]

current = (0, 0)
nodes = [(current)]
for direction, steps, color in instructions:
  x, y = current
  steps = int(steps)
  match direction:
    case "R":
      current = (x + steps, y)
    case "L":
      current = (x - steps, y)
    case "D":
      current = (x, y + steps)
    case "U": 
      current = (x, y - steps)
  nodes.append(current)

def area(nodes):
  x = y = 0
  for i in range(len(nodes) - 1):
    x += nodes[i][0] * nodes[i+1][1]
    y += nodes[i][1] * nodes[i+1][0]
  return (x - y) / 2

def hex2rgb(hex):
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def neighbors(x, y):
  return [(x + dx, y + dy)for dx, dy in directions.values()]

# we had some clever algorithms to determine the first tile to flood
# they didn't work, so we looked at the picture instead. ok then.
first = (-1, -1)
# now floodfill from that space
q = deque([first])
while len(q):
  x, y = q.popleft()
  tiles[(x, y)] = "000000"
  next = [x for x in neighbors(x, y) if x not in tiles and x not in q]
  q.extend(next)

print(f"Solution 1: {len(tiles)}")

# b = integer points on boundary
# i = integer points inside polygon
# A = i + (b/2) - 1

def pick(nodes):
  b = 0
  current = nodes[0]
  for node in nodes:
    if current[0] == node[0]:
      b += abs(current[1] - node[1])
    else:
      b += abs(current[0] - node[0])
    current = node
  return b

print(pick(nodes))