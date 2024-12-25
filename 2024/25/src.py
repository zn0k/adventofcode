#!/usr/bin/env python3

import sys
from itertools import product
import numpy as np

with open(sys.argv[1], "r") as f: 
  chunks = f.read().split("\n\n")

def convert(chunk):
  return np.array([
    [1 if c == "#" else 0 for c in l]
    for l in chunk.split("\n")
  ]).T

locks, keys = [], []
for chunk in chunks:
  if "#" in chunk[:6]:
    locks.append(convert(chunk)) 
  else:
    keys.append(convert(chunk))

fits = 0
for l, k in product(locks, keys):
  overlap = len(l[0])
  if not any(sum(l[i]) + sum(k[i]) > overlap for i in range(len(l))):
    fits += 1

print(f"Solution 1: {fits}")