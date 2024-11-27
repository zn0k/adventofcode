#!/usr/bin/env python3

import sys
import math
import networkx as nx
from itertools import permutations
from collections import defaultdict

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [list(l) for l in lines]

data = readInput()

wc = {}
offsets = [(-1, 0), (1, 0), (0, 1), (0, -1)]

G = nx.Graph()

for y in range(len(data)):
  for x in range(len(data[y])):
    if data[y][x] not in ".#": 
      wc[data[y][x]] = (x, y)
    if data[y][x] == "#": continue
    for dy, dx in offsets:
      if y + dy < 0 or y + dy >= len(data): continue
      if x + dx < 0 or x + dx >= len(data[y]): continue
      if data[y + dy][x + dx] != "#":
        G.add_edge((x, y), (x + dx, y + dy))

waypoints = set(wc.keys()) - set("0")
cache = defaultdict(dict)

def solve(ret=False):
  shortest = math.inf
  for path in permutations(waypoints, len(waypoints)):
    l = 0
    path = ["0"] + list(path) + (["0"] if ret else [])
    segments = zip(path, path[1:])
    for s in segments:
      a, b = sorted([wc[s[0]], wc[s[1]]])
      if a not in cache or b not in cache[a]:
        cache[a][b] = len(nx.shortest_path(G, a, b)) - 1
      l += cache[a][b]
    shortest = min(l, shortest)
  return shortest

print(f"Solution 1: {solve()}")
print(f"Solution 2: {solve(ret=True)}")