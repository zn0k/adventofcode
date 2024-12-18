#!/usr/bin/env python3

import sys
import numpy as np
import networkx as nx

input = np.loadtxt(sys.argv[1], delimiter=",", dtype=int)
if sys.argv[1] == "input.txt":
    d, limit = 71, 1024
else:
    d, limit = 7, 12

# initialize the memory
memory = np.zeros((d, d))
# and read in the first X fallen bytes
for i in range(limit):
    x, y = input[i]
    memory[y][x] = 1

# create a graph that connects free bytes with one another
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
G = nx.Graph()
for y in range(d):
    for x in range(d):
        if memory[y][x] == 1:
            continue
        for dx, dy in directions:
            if 0 <= x + dx < d and 0 <= y + dy < d:
                if memory[y + dy][x + dx] == 0:
                    G.add_edge((x, y), (x + dx, y + dy))

# find the shortest path to the target
part1 = nx.shortest_path_length(G, (0, 0), (d - 1, d - 1))
print(f"Solution 1: {part1}")

# drop bytes one by one
# cache the current shortest path
bp = nx.shortest_path(G, (0, 0), (d - 1, d - 1))
for i in range(limit, len(input)):
    x, y = input[i]
    # find all edges leading in and out of that byte
    edges = [(u, v) for u, v in G.edges if (x, y) == u or (x, y) == v]
    for u, v in edges:
        # remove those edges
        G.remove_edge(u, v)
    # check if we removed a node that is in the current best path
    # if it isn't we know we still have a path
    if (x, y) not in bp:
        continue
    # old best path is in valid
    # check if there is still an alternative
    if not nx.has_path(G, (0, 0), (d - 1, d - 1)):
        print(f"Solution 2: ({x},{y})")
        break
    bp = nx.shortest_path(G, (0, 0), (d - 1, d - 1))
