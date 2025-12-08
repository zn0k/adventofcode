#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import combinations
from math import dist
from operator import mul
from functools import reduce

connections = 10 if sys.argv[1] == "test.txt" else 1000
with open(sys.argv[1], "r") as f:
    coordinates = [tuple([int(x) for x in l.split(",")]) for l in f.readlines()]
    # coordinates. = [(162, 817, 812), (57, 618, 57), (906, 360, 560), ...]

# generate the distances between pairs, sorted by euclidean distance
pairs = [(a, b, dist(a, b)) for a, b in combinations(coordinates, 2)]
pairs = sorted(pairs, key=lambda x: x[2])
# pairs = [((162, 817, 812), (425, 690, 689), 316.90219311326956),
#          ((162, 817, 812), (431, 825, 988), 321.560258738545), ...]

# generate a new graph and add edges between the top N closest pairs
G = nx.Graph()
for a, b, _ in pairs[:connections]:
    G.add_edge(a, b)

# select the three largest components of the graph
largest = list(reversed(sorted(nx.connected_components(G), key=len)))[:3]

# multiply their sizes
solution1 = reduce(mul, map(len, largest), 1)
print(f"Solution 1: {solution1}")

# start a new graph and add all nodes to it
G = nx.Graph()
for a, b, _ in pairs:
    G.add_node(a)
    G.add_node(b)

# continue adding edges between the next closest pair
# until the graph is fully connected
for a, b, _ in pairs:
    last = (a, b)
    G.add_edge(a, b)
    if nx.is_connected(G):
        break

# pull out the X coordinates and multiply them
solution2 = last[0][0] * last[1][0]
print(f"Solution 2: {solution2}")