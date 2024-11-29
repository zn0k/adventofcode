#!/usr/bin/env python3

import sys
import numpy as np
import networkx as nx
from functools import reduce

key = "ffayrhll"

def knot_hash(input):
  lengths = [ord(x) for x in input] + [17, 31, 73, 47, 23]
  pos, skip = 0, 0
  data = np.arange(256)
  for _ in range(64):
    for length in lengths:
      data[0:length] = data[0:length][::-1]
      data = np.roll(data, (length + skip) * -1)
      pos += length + skip
      skip += 1
  data = np.roll(data, pos)
  dense = [reduce(np.bitwise_xor, data[p:p+16]) for p in range(0, 256, 16)]
  return "".join(["%02x" % x for x in dense])

def hash2bin(hash):
  return "".join([f"{int(x, 16):04b}" for x in hash])

data = [hash2bin(knot_hash(key + "-" + str(x))) for x in range(128)]
row_counts = [row.count("1") for row in data]

print(f"Solution 1: {sum(row_counts)}")

G = nx.Graph()
directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
for y in range(len(data)):
  for x in range(len(data[y])):
    if data[y][x] == "1": G.add_node((x, y))
    for dy, dx in directions:
      if y + dy < 0 or y + dy >= len(data): continue
      if x + dx < 0 or x + dx >= len(data[y]): continue
      if data[y][x] == "1" and data[y + dy][x + dx] == "1":
        G.add_edge((x, y), (x + dx, y + dy))

print(f"Solution 2: {nx.number_connected_components(G)}")