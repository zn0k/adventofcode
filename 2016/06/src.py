#!/usr/bin/env python3

import sys
from collections import Counter
import numpy as np

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [[x for x in l] for l in lines]

data = np.array(readInput())
msg = ""
msg2 = ""

for row in data.T:
  c = Counter(row)
  msg += sorted(c.items(), key=lambda x: (-x[1], x[0]))[0][0]
  msg2 += sorted(c.items(), key=lambda x: (-x[1], x[0]))[-1][0]

print(f"Solution 1: {msg}")
print(f"Solution 2: {msg2}")