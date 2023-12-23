
#!/usr/bin/env python3
import sys
from collections import deque
import networkx as nx

with open(sys.argv[1], "r") as f:
  tiles = [list(line.strip()) for line in f.readlines()]

max_x, max_y = len(tiles[0]) - 1, len(tiles) - 1
uphill = {(1, 0): "<", (0, 1): "^", (-1, 0): ">", (0, -1): "v"}

# can't go anywhere else from the true start, so move one down
start = (tiles[0].index("."), 1)
# must take the exit path one tile up, or we've blocked the only way out
target = (tiles[max_y].index("."), max_y - 1)

def inbounds(x, y):
  if x < 0 or x > max_x: return False
  if y < 0 or y > max_y: return False
  return True

def solve(start):
  solutions = []
  q = deque([(start, [], (0, 1))])
  while len(q):
    (x, y), pathref, pdir = q.popleft()
    path = [i for i in pathref]
    if (x, y) == target:
      solutions.append(len(set(path)))
    if tiles[y][x] in "><v^":
      directions = [pdir]
    else:
      directions = [(1, 0), (0, 1), (-1, 0), (0, -1)] 
    for dx, dy in directions:
      new_x, new_y = x + dx, y + dy
      if not inbounds(new_x, new_y): continue
      if tiles[new_y][new_x] == "#": continue
      if uphill[(dx, dy)] == tiles[new_y][new_x]: continue
      if (new_x, new_y) in path: continue
      path.append((x, y))
      q.append(((new_x, new_y), path, (dx, dy)))
  return solutions

solutions = solve(start)
print(f"Solution 1: {max(solutions) + 2}")

# find all valid neighbors given a coordinate
def neighbors(x, y):
  ns = []
  for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
    new_x, new_y = x + dx, y + dy
    if inbounds(new_x, new_y) and tiles[new_y][new_x] != "#":
      ns.append((new_x, new_y))
  return ns

# find all nodes that have more than two neighbors 
# nodes with one neighbor are dead ends (can only go where we came from)
# nodes with two neighbors are part of corridors without choices
def find_junctions():
  nodes = []
  for y in range(max_y):
    for x in range(max_x):
      ns = neighbors(x, y)
      if len(ns) > 2:
        nodes.append((x, y))
  return nodes

# BFS to calculate the distance between two intersection nodes
def bfs(start, intersections):
  distances = {}
  visited = set()
  q = deque([(start, 0)])
  while len(q):
    c, d = q.popleft()
    if c in intersections and c != start:
      distances[c] = d
      continue
    for n in neighbors(*c):
      if n not in visited:
        visited.add(n)
        q.append((n, d + 1))
  return {start: distances}

# DFS to calculate the maximum distance between two nodes given the 
# pre-calculated distances between junctions
def dfs(g, start, end):
  q = deque([(start, 0, {start})])
  max_d = 0
  while len(q):
    node, d, visited = q.pop()
    if node == end:
      max_d = max_d if max_d > d else d
      continue
    for neighbor, cost in g[node].items():
      if neighbor not in visited:
        q.append((neighbor, d + cost, visited | {neighbor}))
  return max_d

# pre-calculate distances between junctions
nodes = [start] + find_junctions() + [target]
g = {}
for node in nodes:
  g |= bfs(node, nodes)

# and find the longest path
print(f"Solution 2: {dfs(g, start, target) + 2}")