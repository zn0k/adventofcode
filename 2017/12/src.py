#!/usr/bin/env python3

import sys
import networkx as nx

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip().split(" <-> ") for l in f.readlines()]
  return [[int(x[0]), [int(y) for y in x[1].split(", ")]] for x in lines]

data = readInput()

# create a graph connecting all the nodes from the input
G = nx.Graph()
for a, bs in data:
  for b in bs:
    G.add_edge(a, b)

# go through all components
components = list(nx.connected_components(G))
for component in components:
  # is the node of interest part of this component?
  if 0 in component:
    # yes, print that component's size
    print(f"Solution 1: {len(component)}")
    break

print(f"Solution 2: {len(components)}")