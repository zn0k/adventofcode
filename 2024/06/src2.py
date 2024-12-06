import sys

with open(sys.argv[1], "r") as f: 
    grid = {}
    for row, line in enumerate(f.readlines()):
        for col, tile in enumerate(line.strip()):
            if tile == "^": start = col + row * 1j
            grid[col + row * 1j] = tile

direction = 0 - 1j
pos = start
part1 = set([pos])
while pos + direction in grid:
    if grid[pos + direction] == "#":
        direction *= 1j # turn
    else:
        pos += direction # move
        part1.add(pos)

print(f"Solution 1: {len(part1)}")

loops = []
for i in part1:
    if grid[i] != ".": continue
    grid[i] = "#"
    direction = 0 - 1j
    pos = start
    visited = set([(pos, direction)])
    while pos + direction in grid:
        if grid[pos + direction] == "#":
            direction *= 1j # turn
        else:
            pos += direction # move
            if (pos, direction) in visited:
                loops.append(i)
                break
            else:
                visited.add((pos, direction))
    grid[i] = "."

print(f"Solution 2: {len(loops)}")