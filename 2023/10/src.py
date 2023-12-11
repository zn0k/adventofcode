#!/usr/bin/env python3

import sys
import networkx as nx

exits = {"|": "NS", "-": "WE", "L": "NE", "J": "NW", "7": "SW", "F": "SE", ".": "", "S": "NSWE"}
connections = {"N": "S", "S": "N", "W": "E", "E": "W"}
directions = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}

with open(sys.argv[1], "r") as f:
  tiles = [list(line.strip()) for line in f.readlines()]

# helper function to determine if a coordinate is in bounds
def inBounds(x, y):
  if x < 0 or x >= len(tiles[0]): return False
  if y < 0 or y >= len(tiles): return False
  return True

# return the list of connected neighbors of tile (x,y)
def getNeighbors(x, y):
  neighbors = []
  tile = tiles[y][x]
  for exit in exits[tile]:
    dx, dy = directions[exit]
    cx, cy = (x + dx, y + dy)
    if inBounds(cx, cy):
      neighborTile = tiles[cy][cx]
      if connections[exit] in exits[neighborTile]:
        neighbors.append((cx, cy))
  return neighbors

G = nx.Graph()
start = None
remove = set()
for x in range(len(tiles[0])):
  for y in range(len(tiles)):
    if tiles[y][x] == "S":
      start = (x, y)
    for neighbor in getNeighbors(x, y):
      G.add_edge((x, y), neighbor)
      remove |= {(2 * x, 2 * y), (2 * neighbor[0], 2 * neighbor[1])}

lengths = [v for k, v in dict(nx.single_source_shortest_path_length(G, start)).items()]
print(f"Solution 1: {max(lengths)}")

# determine vertical chars. some definitely are.
# whether S is depends on its neighbors on the path
verticals = "|LJ"
if any([start[1] - n[1] for n in list(G.neighbors(start))]): verticals += "S"

# start by considering things to be outside.
# whenever a vertical pipe is crossed, it flips.
# count the non-path tiles left to right when inside
path_nodes = set(nx.node_connected_component(G, start))
inside_count = 0
for y in range(len(tiles)):
  inside = False
  for x in range(len(tiles[0])):
    if (x, y) in path_nodes:
      if tiles[y][x] in verticals:
        inside = (not inside)
    else:
      if inside: inside_count += 1

print(f"Solution 2: {inside_count}")