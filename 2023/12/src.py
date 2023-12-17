#!/usr/bin/env python3

import sys
from itertools import product

with open(sys.argv[1], "r") as f:
  patterns = []
  for line in f.readlines():
    pattern, sizes = line.strip().split(" ")
    sizes = list(map(int, sizes.split(",")))
    patterns.append((pattern, sizes))

total = 0
for pattern, sizes in patterns:
  chars = list(pattern)
  var_indexes = [i for i, c in enumerate(chars) if c == "?"]
  target = sum(sizes) - pattern.count("#")
  for p in product(".#", repeat=len(var_indexes)):
    if p.count("#") != target: continue
    for i in range(len(var_indexes)):
      chars[var_indexes[i]] = p[i]
    chunks = "".join(chars).replace(".", " ").split()
    chunks = list(map(len, chunks))
    if chunks == sizes:
      total += 1

print(f"Solution 1: {total}")