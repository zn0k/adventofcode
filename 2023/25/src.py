#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import combinations
from collections import Counter

def get_graph(file):
  G = nx.Graph()
  with open(file, "r") as f:
    for line in f.readlines():
      words = line.split()
      u = words[0].replace(":", "")
      for v in words[1:]:
        G.add_edge(u, v)
  return G

G = get_graph(sys.argv[1])

# find all cut nodes with a cardinality of 3, and create a set from them
# this works for the test data. it would work for the real input
# but it doesn't finish in 45 minutes. sad panda.
#cut_nodes = set([y for x in list(nx.all_node_cuts(G, 3)) for y in x])

# alright, let's hack around that. the three edges we need to cut are choke points
# so it follows that a lot of paths between nodes run through them
# calculate all shortest paths between all pairs of nodes
sps = list(nx.all_pairs_shortest_path(G))
# create a long list that concatenates all shortest paths
paths = []
for _, ps in sps:
  for _, p in ps.items():
    paths += p
# count how often each node appears in this list
c = Counter(paths)
# i'm confused by the official documentation and don't know if these 
# counter objects are guaranteed to be ordered by occurence. 
# do that explicitly
cut_nodes = sorted([(v, k) for k, v in c.items()])[-6:]
# get just the names of the nodes
cut_nodes = list(map(lambda x: x[1], cut_nodes))

# back to the regularly scheduled program. find all edge tuples of nodes
edges = list(G.edges())
# remove the edges between cut nodes, filtering for the ones that actually exist
for a, b in combinations(cut_nodes, 2):
  if (a, b) in edges or (b, a) in edges:
    G.remove_edge(a, b)

# grab the disconnected components
components = list(nx.connected_components(G))

print(f"Solution 1: {len(components[0]) * len(components[1])}")