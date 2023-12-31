#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import combinations

def get_graph(file):
  G = nx.Graph()
  with open(file, "r") as f:
    for line in f.readlines():
      words = line.split()
      u = words[0].replace(":", "")
      for v in words[1:]:
        # add a static capacity of 1 to each node
        # that's because the minimum_cut function below requires capacity
        G.add_edge(u, v, capacity=1.0)
  return G

G = get_graph(sys.argv[1])

# periphery nodes are those with a distance equal to the diameter of the graph
# these should be in the two partitions we want to form
ps = list(nx.periphery(G))
# but there could be more than one node in each partition, so pull out 
# all nodes combined with the first one. compute the shortest path length between them
ls = [(len(nx.shortest_path(G, c[0], c[1])), c) for c in combinations(ps, 2) if ps[0] in c]
# pull out one of the longest path node pairs
pair = sorted(ls)[-1][1]
# use the max-flow min-cut theorem to partition the graph for that node pair
_, partitions = nx.flow.minimum_cut(G, pair[0], pair[1])
print(f"Solution 1: {len(partitions[0]) * len(partitions[1])}")