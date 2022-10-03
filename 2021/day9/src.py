import math
from typing import NamedTuple
from functools import reduce

class P(NamedTuple):
    x: int
    y: int

offsets = [P(-1, 0), P(0, -1), P(1, 0), P(0, 1)]

with open("input.txt", "r") as f:
    heightmap = [[int(c) for c in l.rstrip()] for l in f]
    height = len(heightmap)
    width = len(heightmap[0])

def get_neighbors(point):
    def valid_point(point):
        if point.x < 0 or point.x >= width:
            return False
        if point.y < 0 or point.y >= height:
            return False
        return True
    return list(filter(valid_point, map(lambda o: P(point.x + o.x, point.y + o.y), offsets)))

def get_low_points():
    def is_low_point(point):
        point_value = get_point_height(point)
        neighbors = get_neighbors(point)
        values = map(get_point_height, neighbors)
        return all(map(lambda x: point_value < x, values))
    points = [P(x, y) for x in range(width) for y in range(height)]
    return list(filter(is_low_point, points))

def get_point_height(point):
    return heightmap[point.y][point.x]

low_points = get_low_points()
for p in low_points:
    print(f"{p.x},{p.y}")
risk_levels = [get_point_height(p) + 1 for p in low_points]
print(f"Solution 1: {sum(risk_levels)}")

def get_basin(point, done=[]):
    done.append(point)
    neighbors = list(filter(lambda x: x not in done, get_neighbors(point)))
    values = list(map(get_point_height, neighbors))
    result = [point]
    for i, n in enumerate(neighbors):
        if values[i] != 9:
            result.extend(get_basin(n, done))
    return set(result)

basins = map(get_basin, low_points)
basin_sizes = map(len, basins)
result = reduce(lambda x, y: x * y, sorted(basin_sizes)[-3:])
print(f"Solution 2: {result}")