#!/usr/bin/env python3

import sys
import operator as op

with open(sys.argv[1], "r") as f:
    data = f.read()

chunks = data.split("\n\n")
pieces = [0 for _ in range(len(chunks) - 1)]
for i, chunk in enumerate(chunks[:-1]):
    pieces[i] = chunk.count("#")

grids = []
for line in chunks[-1].split("\n"):
    size, components = line.split(": ")
    size = op.mul(*[int(x) for x in size.split("x")])
    components = [int(x) for x in components.split(" ")]
    grids.append((size, components))

def fits(grid):
    size, components = grid
    needed = 0
    for i in range(len(components)):
        needed += components[i] * pieces[i]
    return needed <= size

solution1 = sum(map(fits, grids))
print(f"Solution 1: {solution1}")