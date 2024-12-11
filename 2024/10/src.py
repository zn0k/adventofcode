#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import combinations

with open(sys.argv[1], "r") as f:
    input = [[int(x) for x in l.strip()] for l in f.readlines()]

w, h = len(input[0]), len(input)

G = nx.DiGraph()

trailheads = []
targets = []
for y in range(h):
    for x in range(w):
        if input[y][x] == 0:
            trailheads.append((x, y))
        if input[y][x] == 9:
            targets.append((x, y))
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if not 0 <= dx + x < w:
                continue
            if not 0 <= dy + y < h:
                continue
            if input[dy + y][dx + x] - input[y][x] == 1:
                G.add_edge((x, y), (dx + x, dy + y))

count = 0
distinct = 0
for a in trailheads:
    for b in targets:
        if nx.has_path(G, a, b):
            count += 1
            distinct += len(list(nx.all_simple_paths(G, a, b)))

print(f"Solution 1: {count}")
print(f"Solution 2: {distinct}")
