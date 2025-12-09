#!/usr/bin/env python3

import sys
from itertools import combinations

with open(sys.argv[1], "r") as f:
    coordinates = [tuple([int(x) for x in l.split(",")]) for l in f.readlines()]
# coordinates = [(7, 1), (11, 1), ...]

# generate all possible rectangles given those coordinates as opposed corners
rectangles = list(combinations(coordinates, 2))

# function to calculate the area of a rectangle given opposed corners
def area(a, b):
    return (abs(a[1] - b[1]) + 1) * (abs(a[0] - b[0]) + 1)

# calculate all the areas
areas = [area(a, b) for a, b in rectangles]
# and pick the largest one
print(f"Solution 1: {max(areas)}")

from shapely.geometry import Polygon, Point, box

# create the larger polygon
polygon = Polygon(coordinates)

# helper to determine whether a rectangle is within a polygon
def in_polygon(p, r):
    # pull out the coordinate components
    x1, y1 = r[0]
    x2, y2 = r[1]
    # create a box based on them, constructor expects minx, miny, maxx, maxy
    rectangle = box(min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
    # and check
    if rectangle.within(p):
        return True
    return False

# filter out rectangles that aren't fully within the polygon
rectangles = filter(lambda s: in_polygon(polygon, s), rectangles)
# calculate areas of remaining rectangles
areas = [area(a, b) for a, b in rectangles]
# pick the biggest one
print(f"Solution 2: {max(areas)}")
