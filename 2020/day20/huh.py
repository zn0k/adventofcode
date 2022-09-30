from collections import Counter
from functools import reduce
from operator import mul
from itertools import product
from math import sqrt

with open("input_test.txt", "r") as f:
    paragraphs = f.read().split("\n\n")
    tiles = {}
    for paragraph in paragraphs:
        lines = paragraph.split("\n")
        tile_id = lines[0].split(" ")[1][0:-1]
        tiles[tile_id] = lines[1::]

def flip_edge(edge):
    return "".join(reversed(edge))

def get_edge(tile, which):
    # 0 is the top edge, 1 the right, 2 the bottom, and 3 the left
    if which == 0: return tile[0]
    if which == 1: return "".join([tile[x][-1] for x in range(0, 10)])
    if which == 2: return tile[-1]
    if which == 3: return "".join([tile[x][0] for x in range(0, 10)])

edges = {}
for tile_id in tiles:
    for which in range(0, 4):
        edge = get_edge(tiles[tile_id], which)
        if edge in edges:
            edges[edge].append(tile_id)
        else:
            flipped = flip_edge(edge)
            if flipped in edges:
                 edges[flipped].append(tile_id)
            else:
                edges[edge] = [tile_id]

free_edges = Counter([edges[x][0] for x in edges if len(edges[x]) == 1])
corner_pieces = [x for x in free_edges if free_edges[x] == 2]
answer1 = reduce(mul, map(int, corner_pieces))
print(f"Answer 1: {answer1}")

def rotate_tile(tile):
    return list(map("".join, zip(*reversed(tile))))

def flip_tile(tile):
    return list(reversed(tile))

def is_free_edge(edge):
    if edge not in edges: edge = flip_edge(edge)
    return len(edges[edge]) == 1

def visualize_tile(tile):
    return "\n".join(map("".join, tile))

def get_neighbors(tile):
    tile_id = [x for x in tiles if tiles[x] == tile][0]
    neighbors = [edges[edge] for edge in edges if tile_id in edges[edge]]
    neighbors = set([n for x in neighbors for n in x])
    neighbors.remove(tile_id)
    return list(neighbors)

def get_variations(tile):
    variations = []
    for flipped in range(0, 2):
        tile = flip_tile(tile)
        for rotations in range(0, 4):
            tile = rotate_tile(tile)
            variations.append(tile)
    return variations

width = int(sqrt(len(tiles)))
oriented_tiles = [[0 for y in range(0, width)] for x in range(0, width)]
# pick a corner piece
# the corner piece has two neighbors, one to the right and one to the bottom
neighbors = get_neighbors(tiles[corner_pieces[0]])
# generate all their flipped and rotated variations
# the corner is the first tile, the right neighbor the second, and the bottom the third
# we don't know yet which neighbor is which
c_vars = get_variations(tiles[corner_id])
n1_vars = get_variations(tiles[neighbors[0]])
n2_vars = get_variations(tiles[neighbors[1]])
variations = list(product(c_vars, n1_vars, n2_vars))
# on one of these, the following conditions are true:
# - the top edge of the corner is free
# - the left edge of the corner is free
# - the top edge of the right neighbor is free
# - the right edge of the corner matches the left edge of the right neighbor exactly
# - the left edge of the bottom neighbor is free
# - the bottom edge of the corner matches the top edge of the bottom neighbor exactly
def check_corner_var(c, n1, n2):
    if not is_free_edge(get_edge(c, 0)): return False
    if not is_free_edge(get_edge(c, 3)): return False
    if not is_free_edge(get_edge(n1, 0)): return False
    if not is_free_edge(get_edge(n2, 3)): return False
    if not get_edge(c, 1) == get_edge(n1, 3): return False
    if not get_edge(c, 2) == get_edge(n2, 0): return False
    return True

corner = list(filter(lambda x: check_corner_var(x[0], x[1], x[2]), variations))[0][0]
oriented_tiles[0][0] = corner

# given a starting piece in a row, find the right neighbor each time
# then find the bottom neighbor of the previous starting piece and do the next row

def get_neighbor(tile, which):
    n_which = (which + 2) % 4
    neighbors = get_neighbors(tile)
    edge = get_edge(tile, which)
    for n in neighbors:
        for v in get_variations(tiles[n]):
            if get_edge(v, n_which) == edge:
                return v

for row in range(0, width):
    for col in range(1, width):
        oriented_tiles[row][col] = get_neighbor(oriented_tiles[row][col - 1], 1)
    oriented_tiles[row + 1][0] = get_neighbor(oriented_tiles[row][0], 2)

for row in range(0, width):
    for col in range(0, width):
        print(visualize_tile(oriented_tiles[row][col]))
        print("\n")
