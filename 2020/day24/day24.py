import re
from collections import Counter
from functools import reduce
with open("input.txt", "r") as f:
    directions = [x.rstrip() for x in f.readlines()]
step_regex = re.compile("(e|se|sw|w|nw|ne)")
offsets = {
    "e": (2, 0), 
    "w": (-2, 0), 
    "se": (1, -3), 
    "sw": (-1, -3), 
    "ne": (1, 3), 
    "nw": (-1, 3)}
def move(point, step):
    offset = offsets[step]
    return (point[0] + offset[0], point[1] + offset[1])
def follow(directions):
    steps = re.findall(step_regex, directions)
    return reduce(move, steps, (0, 0))
def count_black():
    return sum(map(lambda x: x % 2 == 1, tiles.values()))
tiles = Counter([follow(x) for x in directions])
print(f"Answer 1: {count_black()}")
def get_neighbors(tile):
    return [move(tile, offset) for offset in offsets]
def is_black(tile):
    return 1 if tiles[tile] % 2 == 1 else 0
def add_neighbors():
    # for each tile already placed, place all neighbors
    # do this as a set so each new tile only gets counted once
    new = set()
    for tile in tiles:
        for neighbor in get_neighbors(tile):
            if neighbor not in tiles:
                new.add(neighbor)
    # add each new tile twice so it counts as white
    tiles.update(new)
    tiles.update(new)
def flip_for_day():
    flips = set()
    for tile in tiles:
        black_neighbors = sum(map(is_black, get_neighbors(tile)))
        if is_black(tile) and (black_neighbors == 0 or black_neighbors > 2):
            flips.add(tile)
        if not is_black(tile) and black_neighbors == 2:
            flips.add(tile)
    tiles.update(flips)
for i in range(0, 100):
    add_neighbors()
    flip_for_day()
print(f"Answer 2: {count_black()}")