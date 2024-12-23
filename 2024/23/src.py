#!/usr/bin/env python3

import sys
import networkx as nx
from itertools import combinations

with open(sys.argv[1], "r") as f: 
  lines = [l.strip() for l in f.readlines()]

G = nx.Graph()

for l in lines:
  a, b = l.split("-")
  G.add_edge(a, b)

part1 = [
  c for c in nx.enumerate_all_cliques(G)
  if len(c) == 3 and 
  any(n.startswith("t") for n in c)
]

print(f"Solution 1: {len(part1)}")

lan_party = sorted([c for c in nx.enumerate_all_cliques(G)], key=len)[-1]
pwd = ",".join(sorted(lan_party))

print(f"Solution 2: {pwd}")