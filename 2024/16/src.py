#!/usr/bin/env python3

import sys
import networkx as nx

with open(sys.argv[1], "r") as f: 
  input = [[c for c in l.strip()] for l in f.readlines()]

maze = nx.DiGraph()
start, end = None, None

for y in range(len(input)):
  for x in range((len(input[0]))):
    # check special cases: wall, start tile, target tile
    match input[y][x]:
      case "#":
        continue
      case "S":
        start = (x + y * 1j, 1 + 0j)
      case "E":
        end = (x + y * 1j)
    # for each tile, handle its four cardinal directions
    for d in [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]:
      tile = (x + y * 1j)
      # on each tile, we can turn 90 degrees CCW or CW for a cost of 1,000
      maze.add_edge((tile, d), (tile, d * 1j), weight=1000)
      maze.add_edge((tile, d), (tile, d * -1j), weight=1000)
      # now connect the tile and direction to the neighbor, if it exists
      neighbor = tile + d
      if input[int(neighbor.imag)][int(neighbor.real)] != "#":
        maze.add_edge((tile, d), (neighbor, d), weight=1)

# we don't care what direction we face on the target tile
targets = [(end, d) for d in [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]]
# get the shortest path length
costs = [nx.shortest_path_length(maze, start, t, weight="weight") for t in targets]
# and pick the cheapest one
print(f"Solution 1: {min(costs)}")

# get the direction we're facing in on the shortest path
idx = costs.index(min(costs))
d = [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j][idx]
# create the actual target that also encodes that direction
target = (end, d)

# get all shortest paths going there
paths = nx.all_shortest_paths(maze, start, target, weight="weight")
# pull out the tiles in each path into a set
tiles = set()
for p in paths:
  for n in p:
    tiles.add(n[0])
# and find the set size
print(f"Solution 2: {len(tiles)}")