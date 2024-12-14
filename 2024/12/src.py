#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import groupby
import numpy as np

with open(sys.argv[1], "r") as f:
    farm = [l.strip() for l in f.readlines()]

w, h = len(farm[0]), len(farm)

# read the farm map into a graph
G = nx.Graph()

for y in range(h):
    for x in range(w):
        G.add_node((x, y))
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if not 0 <= x + dx < w:
                continue
            if not 0 <= y + dy < h:
                continue
            if farm[y][x] == farm[y + dy][x + dx]:
                G.add_edge((x, y), (x + dx, y + dy))


# we only connected like plants, so they each form a strong or weak component
regions = [G.subgraph(c) for c in nx.connected_components(G)]
# area is just the number of nodes in the subgraph
# perimeter is four per node, minus two for each edge
prices = [len(r) * (len(r) * 4 - len(nx.edges(r)) * 2) for r in regions]

print(f"Solution 1: {sum(prices)}")

def draw_graph(G):
    xs = [n[0] for n in G.nodes]
    ys = [n[1] for n in G.nodes]
    x_min, x_max, y_min, y_max = min(xs), max(xs), min(ys), max(ys)
    farm = [[" " for _ in range(x_max - x_min + 1)] for _ in range(y_max - y_min + 1)]
    for i, c in enumerate(nx.connected_components(G)):
        for x, y in c:
            farm[y - y_min][x - x_min] = chr(i + 65)
    farm = ["".join(row) for row in farm]
    print("\n".join(farm))

def sides(r):
    # the number of sides is equivalent to the number of corners in the region
    corners = 0
    # go through the tiles in the region
    for (x, y) in r.nodes:
        # determine whether their neighbors are set
        up = (x, y - 1) in r.nodes
        down = (x, y + 1) in r.nodes
        left = (x - 1, y) in r.nodes
        right = (x + 1, y) in r.nodes
        upleft = (x - 1, y - 1) in r.nodes
        downleft = (x - 1, y + 1) in r.nodes
        upright = (x + 1, y - 1) in r.nodes
        downright = (x + 1, y + 1) in r.nodes
        # determine how many corners the tile contributes
        if not up and not left: corners += 1
        if not down and not left: corners += 1
        if not up and not right: corners += 1
        if not down and not right: corners += 1
        if up and left and not upleft: corners += 1
        if down and left and not downleft: corners += 1
        if up and right and not upright: corners += 1
        if down and right and not downright: corners += 1
    return corners

prices = [len(r) * sides(r) for r in regions]

print(f"Solution 2: {sum(prices)}")