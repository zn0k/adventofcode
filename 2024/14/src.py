#!/usr/bin/env python3

import sys
import re
import numpy as np
from PIL import Image

# define the grid size and its midpoints
grid = np.array([11, 7]) if sys.argv[1] == "test.txt" else np.array([101, 103])
mx = grid[0] // 2
my = grid[1] // 2

# get the robots into a 2d-array
with open(sys.argv[1], "r") as f:
    robots = [l.strip() for l in f.readlines()]
    robots = [re.findall(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", r) for r in robots]
    robots = [list(map(int, list(r[0]))) for r in robots]
    robots = np.array(robots)

# pull out the positions and velocities
positions = robots[:, :2]
velocities = robots[:, 2:]

rounds = 100

# calculate the new positions
new = (positions + velocities * rounds) % grid

# define some masks to slice out the quadrants
upper_left = (new[:, 0] < mx) & (new[:, 1] < my)
upper_right = (new[:, 0] > mx) & (new[:, 1] < my)
lower_left = (new[:, 0] < mx) & (new[:, 1] > my)
lower_right = (new[:, 0] > mx) & (new[:, 1] > my)

# generate the answer by multiplying the number of robots in the quadrants
part1 = len(new[upper_left]) * len(new[upper_right])
part1 *= len(new[lower_left]) * len(new[lower_right])

print(f"Solution 1: {part1}")

rounds = 10000
# generate the variance of coordinates for each iteration
variances = np.zeros(rounds)
for i in range(rounds):
    ps = (positions + velocities * i) % grid
    variances[i] = np.var(ps)

part2 = np.argmin(variances)

# find the iteration with the least variance
print(f"Solution 2: {part2}")

# draw it out because why not
image = Image.new("RGB", list(grid), "white")
green = (0, 105, 62)
for c in (positions + velocities * part2) % grid:
    image.putpixel(c, green)
image.save("part2.png")