#!/usr/bin/env python3

import sys
import networkx as nx

with open(sys.argv[1], "r") as f:
    input = [[c for c in l.strip()] for l in f.readlines()]

directions = [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]
maze = nx.DiGraph()

for y in range(len(input)):
    for x in range((len(input[0]))):
        # check special cases: wall, start tile, target tile
        match input[y][x]:
            case "#":
                continue
            case "S":
                start = (x + y * 1j, 1 + 0j)
            case "E":
                end = x + y * 1j
        # for each tile, handle its four cardinal directions
        for d in directions:
            tile = x + y * 1j
            # on each tile, we can turn 90 degrees CCW or CW for a cost of 1,000
            maze.add_edge((tile, d), (tile, d * 1j), weight=1000)
            maze.add_edge((tile, d), (tile, d * -1j), weight=1000)
            # now connect the tile and direction to the neighbor, if it exists
            n = tile + d
            if input[int(n.imag)][int(n.real)] != "#":
                maze.add_edge((tile, d), (n, d), weight=1)

# get the shortest path length to all possible directions on the target tile
costs = [
    nx.shortest_path_length(maze, start, t, weight="weight")
    for t in [(end, d) for d in directions]
]
# and pick the cheapest one
print(f"Solution 1: {min(costs)}")

# get the direction we're facing in on the shortest path
d = directions[costs.index(min(costs))]
# create the actual target that also encodes that direction
target = (end, d)

# get all shortest paths going there
paths = nx.all_shortest_paths(maze, start, target, weight="weight")
# pull out the tiles in each path into a set
tiles = set(n[0] for p in paths for n in p)
# and find the set size
print(f"Solution 2: {len(tiles)}")
