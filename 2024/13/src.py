#!/usr/bin/env python3

import sys
import re
import numpy as np

with open(sys.argv[1], "r") as f:
    chunks = f.read().split("\n\n")

part1 = 0
part2 = 0
for c in chunks:
    c = c.replace("+", "=")
    xs = list(map(int, re.findall(r"X=(\d+)", c)))
    ys = list(map(int, re.findall(r"Y=(\d+)", c)))

    a = np.array([[xs[0], xs[1]], [ys[0], ys[1]]])
    b = np.array([xs[2], ys[2]])
    x = list(map(np.round, np.linalg.solve(a, b)))
    if np.allclose(np.dot(a, x), b):
        part1 += x[0] * 3 + x[1]

    b = np.array([xs[2] + 10000000000000, ys[2] + 10000000000000])
    x = np.linalg.solve(a, b)
    if all(np.abs(x - x.round().astype(int)) < 0.01):
        part2 += x[0] * 3 + x[1]

print(f"Solution 1: {int(part1)}")
print(f"Solution 2: {int(part2)}")
