#!/usr/bin/env python3

import sys

# read in the grid
with open(sys.argv[1], "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]
# grid = [['.', '.', 'S', ...], ...]

def print_grid(grid):
    lines = ["".join(line) for line in grid]
    print("\n".join(lines))

# part 1 hit every branch falling down the ugly tree

# function to fill beams into the grid
def fill_beams(grid):
    # loop through grid cells
    # no need to look at first line
    for y in range(1, len(grid)):
        for x in range(len(grid[0])):
            # we're at a splitter
            if grid[y][x] == "^":
                # put beams to the left and right
                # input shows this is safe with boundaries
                grid[y][x - 1] = "|"
                grid[y][x + 1] = "|"
            # we're at an empty point
            elif grid[y][x] == ".":
                # if there's a beam or the start above us
                if grid[y - 1][x] in "S|":
                    grid[y][x] = "|"
    return grid

# count splits that occurred
def count_splits(grid):
    count = 0
    # walk grid
    for y in range(1, len(grid)):
        for x in range(1, len(grid[0]) - 1):
            # we're at a splitter
            if grid[y][x] == "^":
                # and there's a beam above it
                if grid[y - 1][x] == "|":
                    count += 1
    return count


# fill grid with beams, and then count splits
grid = fill_beams(grid)
solution1 = count_splits(grid)
print(f"Solution 1: {solution1}")

# read in the grid
with open(sys.argv[1], "r") as f:
    grid = [list(line.strip()) for line in f.readlines()]

# count the number of realities created
def count_realities(grid):
    # start with 0 realities at each x coordinate
    realities = [0 for _ in range(len(grid[0]))]
    # walk the grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            # the starting position creates one reality
            if grid[y][x] == "S":
                realities[x] = 1
            # each splitter adds the number of realities
            # above it to the number of realities otherwise
            # already created to its left and right
            # the beam no longer moves straight down, so reset
            # at this coordinate
            if grid[y][x] == "^":
                realities[x - 1] += realities[x]
                realities[x + 1] += realities[x]
                realities[x] = 0
    # sum the realities
    return sum(realities)

solution2 = count_realities(grid)
print(f"Solution 2: {solution2}")