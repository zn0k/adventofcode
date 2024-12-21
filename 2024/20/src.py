#!/usr/bin/env python3

import sys
import networkx as nx
from collections import Counter

with open(sys.argv[1], "r") as f:
    input = [[c for c in l.strip()] for l in f.readlines()]

h, w = len(input), len(input[0])

# create a graph that connects free bytes with one another
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
G = nx.Graph()
candidates = set()
for y in range(h):
    for x in range(w):
        match input[y][x]:
            case "#":
                # it's a wall. check if it could be skipped horizontally
                if 0 <= x - 1 < w and 0 <= x + 1 < w:
                    if input[y][x - 1] in ".SE" and input[y][x + 1] in ".SE":
                        candidates.add((x, y, "h"))
                # check for vertically
                if 0 <= y - 1 < h and 0 <= y + 1 < h:
                    if input[y - 1][x] in ".SE" and input[y + 1][x] in ".SE":
                        candidates.add((x, y, "v"))
                # but for now don't do anything with it
                continue
            case "E":
                end = (x, y)
            case "S":
                start = (x, y)
        for dx, dy in directions:
            if 0 <= x + dx < w and 0 <= y + dy < h:
                if input[y + dy][x + dx] in ".SE":
                    G.add_edge((x, y), (x + dx, y + dy))

# find the shortest path without cheating
benchmark = nx.shortest_path_length(G, start, end)
paths = []

# loop through the walls that can be skipped
for x, y, d in candidates:
    # add connections through them
    match d:
        case "h":
            G.add_edge((x, y), (x - 1, y))
            G.add_edge((x, y), (x + 1, y))
        case "v":
            G.add_edge((x, y), (x, y - 1))
            G.add_edge((x, y), (x, y + 1))
    # record the best path in this adjusted map
    paths.append(nx.shortest_path_length(G, start, end))
    # and remove that wallskip
    G.remove_node((x, y))

part1 = sum(benchmark - p >= 100 for p in paths)
print(f"Solution 1: {part1}")
