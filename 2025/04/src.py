#!/usr/bin/env python3

import sys
from itertools import product

with open(sys.argv[1], "r") as f:
    rows = [list(l.strip()) for l in f.readlines()]
# rows = [['.', '.', '@', ...]...]

# return a closure that indicates whether a coordinate pair
# is within grid boundaries given a grid
def make_boundary_function(data):
    max_x = len(data[0])
    max_y = len(data)
    return lambda x, y: x >= 0 and y >= 0 and x < max_x and y < max_y

is_inbound = make_boundary_function(rows)

# create the directions for neighbors of a given coordinate
directions = list(product([0, 1, -1], [0, 1, -1]))
# that creates 9 including (0, 0), the coordinate itself
directions.remove((0, 0))

# count how many rolls in a grid are accessible
# also return the coordinates of those accessible rolls
def count_accessible(data):
    accessible = 0
    coordinates = []
    # walk the grid, by row and then by column
    for y, row in enumerate(rows):
        for x, cell in enumerate(row):
            if rows[y][x] == ".":
                # no roll here, skip the coordinate
                continue
            rolls = 0
            # walk the neighbors of the roll
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_inbound(nx, ny):
                    if rows[ny][nx] == "@":
                        # neighbor is a roll, count it
                        rolls += 1
            if rolls < 4:
                # fewer than 4 rolls as neighbors
                accessible += 1
                coordinates.append((x, y))
    return accessible, coordinates

accessible, coordinates = count_accessible(rows)
print(f"Solution 1: {accessible}")

# while we can remove rolls
while len(coordinates):
    # remove those rolls
    for x, y in coordinates:
        rows[y][x] = "."
    # and iterate, adding up accessible rolls as we go
    additional, coordinates = count_accessible(rows)
    accessible += additional

print(f"Solution 2: {accessible}")