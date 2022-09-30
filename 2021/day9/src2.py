from typing import NamedTuple
from functools import reduce
import networkx as nx

class P(NamedTuple):
    x: int
    y: int

offsets = [P(-1, 0), P(0, -1), P(1, 0), P(0, 1)]

with open("input.txt", "r") as f:
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

G = nx.Graph()
for value, point, neighbors in points:
    if value == 9: continue
    for neighbor in neighbors:
        if heightmap[neighbor.y][neighbor.x] == 9:
            continue
        G.add_edge(point, neighbor)

basin_sizes = map(len, nx.connected_components(G))
result = reduce(lambda x, y: x * y, sorted(basin_sizes, reverse=True)[0:3])
print(f"Solution 2: {result}")