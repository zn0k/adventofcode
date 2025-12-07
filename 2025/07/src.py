#!/usr/bin/env python3

import sys

# read in the grid
with open(sys.argv[1], "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]
# grid = [['.', '.', 'S', ...], ...]

# keep track of total splits
splits = 0
# keep track of realities. the start gives us the first
realities = [1 if x == "S" else 0 for x in grid[0]]

# walk the grid, skipping the starting row
for y in range(1, len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == "^":
            # we're at a splitter
            if realities[x] > 0:
                # a split occurs
                splits += 1
                # carry down realities to the left and right
                realities[x - 1] += realities[x]
                realities[x + 1] += realities[x]
                # beam no longer goes straight down
                realities[x] = 0

print(f"Solution 1: {splits}")
print(f"Solution 2: {sum(realities)}")
