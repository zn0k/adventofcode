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
    draw_graph(r)
    # create a new graph for the outside boundaries
    outside = nx.Graph()
    # step through each node and move it up/down/left/right
    # those results that are now outside the original graph
    # form boundaries
    for n in r.nodes:
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (n[0] + dx, n[1] + dy) not in r.nodes:
                outside.add_node((n[0] + dx, n[1] + dy))
    # now connect the nodes in those boundaries into regions
    for n in outside.nodes:
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (n[0] + dx, n[1] + dy) in outside.nodes:
                outside.add_edge(n, (n[0] + dx, n[1] + dy))
    # we only want single tiles or lines as boundary regions
    regions = [outside.subgraph(c) for c in nx.connected_components(outside)]
    for r in regions:
        # check if the region has any horizontal edges
        if any(u_y == v_y for (_, u_y), (_, v_y) in r.edges):
            # it does, delete all the vertical edges in it
            for u, v in [(u, v) for u, v in r.edges if u[0] == v[0]]:
                outside.remove_edge(u, v)

    # the number of sides is equal to the number of regions
    # regions that are single tiles count for two sides
    sides = [1 if len(c) > 1 else 2 for c in nx.connected_components(outside)]
    print("\n")
    draw_graph(outside)
    return sum(sides)

for r in regions:
    area = len(r)
    s = sides(r)
    print(f"A region of plants with price {area} * {s} = {area * s}")

prices = [len(r) * sides(r) for r in regions]

print(f"Solution 2: {sum(prices)}")