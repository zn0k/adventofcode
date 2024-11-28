#!/usr/bin/env python3

import sys
from collections import Counter

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [l.split() for l in lines]

data = readInput()

valid = [x for x in data if len(x) == len(set(x))]
print(f"Solution 1: {len(valid)}")

counted = [[frozenset(Counter(x)) for x in phrase] for phrase in data]
valid = [x for x in counted if len(x) == len(set(x))]
print(f"Solution 2: {len(valid)}")