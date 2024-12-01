#!/usr/bin/env python3

import sys
import numpy as np
from collections import Counter

with open(sys.argv[1], "r") as f: 
  lines = [l.strip() for l in f.readlines()]
data = np.array([[int(x) for x in l.split()] for l in lines])

left, right = sorted(data[:, 0]), sorted(data[:, 1])
diffs = [abs(x[0] - x[1]) for x in zip(left, right)]
print(f"Solution 1: {sum(diffs)}")

c = Counter(right)
scores = [x * (c[x] if x in c else 0) for x in left]
print(f"Solution 2: {sum(scores)}")