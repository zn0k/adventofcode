from collections import deque
from itertools import combinations
import sys

with open(sys.argv[1], "r") as f:
    grid = [[c for c in l.strip()] for l in f.readlines()]

threshold = 100 if sys.argv[1] == "input.txt" else 50

h, w = len(grid), len(grid[0])

for y in range(h):
    for x in range(w):
        if grid[y][x] == "S":
            start = (x, y)
            grid[y][x] = "."
        if grid[y][x] == "E":
            end = (x, y)
            grid[y][x] = "."


# simple BFS
def bfs(grid, start):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    h, w = len(grid), len(grid[0])

    q = deque([start])
    ds = [[None] * w for _ in range(h)]
    ds[start[1]][start[0]] = 0

    while len(q):
        x, y = q.popleft()
        d = ds[y][x]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if grid[ny][nx] == "." and ds[ny][nx] is None:
                    q.append((nx, ny))
                    ds[ny][nx] = d + 1
    return ds


# run a BFS from the start tile to get the distance to any other tile
from_start = bfs(grid, start)
# do the same for the end tile
to_end = bfs(grid, end)

# benchmark the fastest path without cheating
benchmark = from_start[end[1]][end[0]]

# enumerate the tiles reachable from the start
reachable = [(x, y) for y in range(h) for x in range(w) if from_start[y][x] is not None]
# sort them to be in order from the start tile
reachable_sorted = sorted(reachable, key=lambda x: from_start[x[1]][x[0]])

part1 = 0
part2 = 0 

for (ax, ay), (bx, by) in combinations(reachable_sorted, r=2):
    md = abs(bx  - ax) + abs(by - ay)
    if md == 2:
        path_length = from_start[ay][ax] + md + to_end[by][bx]
        if path_length + threshold <= benchmark:
            part1 += 1
    if md < 21:
        path_length = from_start[ay][ax] + md + to_end[by][bx]
        if path_length + threshold <= benchmark:
            part2 += 1

print(f"Solution 1: {part1}")
print(f"Solution 1: {part2}")
