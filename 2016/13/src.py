#!/usr/bin/env python3

import sys
import networkx as nx

fave = 1362
destination = (31,39)

# build the map
map = []
for y in range(50):
    # default to open spaces
    map.append(["."] * 50)
    for x in range(50):
        # get the number of 1s in the binary representation of the magic formula
        n = x * x + 3 * x + 2 * x * y + y + y * y 
        n += fave 
        count = bin(n).count("1")
        # check if the coordinate is a wall
        if count % 2 == 1:
            map[y][x] = "#"

# initialize the network graph
G = nx.Graph()
# initialize the offsets for walking non-diagonally
offsets = [(-1, 0), (1, 0), (0, 1), (0, -1)]
# go through the map and build edges between coordinates
for y in range(50):
    for x in range(50):
        # check if this is a wall
        if map[y][x] == "#": continue
        # look at the four directions we can walk in
        for dy, dx in offsets:
             # check that we're in bounds
             if y + dy < 0 or x + dx < 0: continue
             if y + dy > 49 or x + dx > 49: continue
             # check if there's an open space in that direction
             if map[y + dy][x + dx] == ".":
                 # we can get there, add an edge
                 G.add_edge((x, y), (x + dx, y + dy))

# get the shortest path from (1, 1) to the destination
path = nx.shortest_path(G, (1, 1), destination)

# solution is the length of that path minus one,
# because the path given by nx contains the starting node
print(f"Solution 1: {len(path) - 1}")

# calculate the shortest path from (1, 1) to all possible destinations
paths = nx.shortest_path(G, (1, 1))

# this gives us a dictionary keyed by destinations with a value of the full node path
# count the paths that have a length of 50 or less
destinations = [k for k, v in paths.items() if (len(v) - 1) <= 50]
print(f"Solution 2: {len(destinations)}")