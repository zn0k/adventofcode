from typing import NamedTuple
from functools import reduce
from collections import deque

class P(NamedTuple):
    x: int
    y: int

offsets = [P(-1, 0), P(0, -1), P(1, 0), P(0, 1)]

with open("9-4096-4.in", "r") as f:
    heightmap = [[int(c) for c in l.rstrip()] for l in f]
    height = len(heightmap)
    width = len(heightmap[0])

def get_point_height(point):
    return heightmap[point.y][point.x]

def get_neighbors(point):
    def valid_point(point):
        if point.x < 0 or point.x >= width: return False
        if point.y < 0 or point.y >= height: return False
        return True
    return list(filter(valid_point, map(lambda o: P(point.x + o.x, point.y + o.y), offsets)))

def is_low_point(value, point, neighbors):
    point_value = heightmap[point.y][point.x]
    values = [heightmap[n.y][n.x] for n in neighbors]
    return all(map(lambda x: point_value < x, values))

points = [(heightmap[y][x], P(x, y), get_neighbors(P(x, y))) for x in range(width) for y in range(height)]

low_points = list(filter(lambda x: is_low_point(*x), points))
risk_levels = map(lambda x: x[0] + 1, low_points)
print(f"Solution 1: {sum(risk_levels)}")

def basin_size(start):
    result = 1
    frontier = deque()
    frontier.appendleft(start)
    reached = set()
    reached.add(start)
    while len(frontier):
        current = frontier.pop()
        neighbors = get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in reached and get_point_height(neighbor) != 9:
                result += 1
                frontier.appendleft(neighbor)
                reached.add(neighbor)
    return result

low_points = map(lambda x: x[1], low_points)
basin_sizes = map(basin_size, low_points)
result = reduce(lambda x, y: x * y, sorted(basin_sizes, reverse=True)[0:3])
print(f"Solution 2: {result}")