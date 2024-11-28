#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import repeat
from collections import Counter

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  def parse(l):
    n, c, *cs = l.split()
    c = int(c.replace("(", "").replace(")", ""))
    if len(cs):
      cs = [x.replace(",", "") for x in cs[1:]]
    return [n, c, cs]
  return [parse(l) for l in lines]

data = readInput()

G = nx.DiGraph()
# first, create the tree
for name, weight, children in data:
  if len(children):
    G.add_edges_from(zip(repeat(name), children))
# then create the weight attributes
for name, weight, _ in data:
  G.nodes[name]["weight"] = weight
  G.nodes[name]["acc"] = 0

# find the one node that doesn't have an inbound edges, it's the root
root = [node for node in G.nodes if G.in_degree(node) == 0][0]
print(f"Solution 1: {root}")

# propagate the accumulated weights up the tree
for node in reversed(list(nx.topological_sort(G))):
  child_weights = [G.nodes[child]["acc"] for child in G.successors(node)]
  G.nodes[node]["acc"] = G.nodes[node]["weight"] + sum(child_weights)

# function to check if all the child weights of a node are balanced
def check_weights(node):
  child_weights = sorted(Counter(G.nodes[child]["acc"] for child in G.successors(node)).items())
  if len(child_weights) > 1:
    # this node is unbalanced. pull out the wrong and right weights
    right_weight = child_weights[0][0]
    wrong_weight = child_weights[1][0]
    delta = right_weight - wrong_weight
    # find the child with the wrong weight
    for child in G.successors(node):
      if G.nodes[child]["acc"] == wrong_weight:
        # and fix it
        print(f"Solution 2: {G.nodes[child]['weight'] + delta}")
        return True
  return False

# go through all nodes from the leafs in so the first unbalanced node is the one
# that needs to be fixed
for node in reversed(list(nx.topological_sort(G))):
  # bail after first unbalanced node
  if check_weights(node): break