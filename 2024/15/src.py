#!/usr/bin/env python3

import sys
from collections import deque


def parse_grid(raw):
    chunks = raw.split("\n\n")
    grid = [[c for c in line] for line in chunks[0].split("\n")]
    moves = deque()
    for line in chunks[1].split("\n"):
        moves.extend(line)
    h, w = len(grid), len(grid[0])
    for y in range(h):
        for x in range(w):
            if grid[y][x] == "@":
                p = (x, y)
                grid[y][x] = "."
    return (grid, moves, p)


def play(grid, moves, p):
    directions = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}
    while len(moves):
        m = moves.popleft()
        x, y = p
        dx, dy = directions[m]
        new_x, new_y = (x + dx, y + dy)
        if grid[new_y][new_x] == "#":
            # ran into a wall, do nothing
            continue
        if grid[new_y][new_x] == ".":
            # moving to free tile, record new position
            p = (new_x, new_y)
            continue
        # moving into a box
        # add all boxes connected to our position to us
        # katamari!
        katamari = set([p])
        prior = len(katamari)
        while True:
            for ox, oy in list(katamari):
                match grid[oy + dy][ox + dx]:
                    case "O":
                        katamari.add((ox + dx, oy + dy))
                    case "[":
                        katamari.add((ox + dx, oy + dy))
                        katamari.add((ox + dx + 1, oy + dy))
                    case "]":
                        katamari.add((ox + dx, oy + dy))
                        katamari.add((ox + dx - 1, oy + dy))
            if len(katamari) == prior:
                break
            prior = len(katamari)
        # check if any tiles covered by our katamari run into walls
        # when moving in the direction we want to go on in
        blocked = any(
            True if grid[oy + dy][ox + dx] == "#" else False for ox, oy in katamari
        )
        if not blocked:
            # we can move the katamari
            # create the new positions
            moved_katamari = set((ox + dx, oy + dy) for ox, oy in katamari)
            # move the actual tiles
            old_grid = [x.copy() for x in grid]
            for ox, oy in katamari:
                grid[oy + dy][ox + dx] = old_grid[oy][ox]
            # clean out the tiles we moved away from
            for ox, oy in katamari - moved_katamari:
                grid[oy][ox] = "."
            # and move the player
            p = (x + dx, y + dy)
    # score the boxes
    h, w = len(grid), len(grid[0])
    boxes = [100 * y + x for y in range(h) for x in range(w) if grid[y][x] in "[O"]
    return sum(boxes)


with open(sys.argv[1], "r") as f:
    file_content = f.read()

grid, moves, p = parse_grid(file_content)
part1 = play(grid, moves, p)

print(f"Solution 1: {part1}")

extended = file_content.replace(".", "..")
extended = extended.replace("@", "@.")
extended = extended.replace("O", "[]")
extended = extended.replace("#", "##")

grid, moves, p = parse_grid(extended)

part2 = play(grid, moves, p)

print(f"Solution 2: {part2}")
