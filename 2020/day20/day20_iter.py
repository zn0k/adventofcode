from collections import Counter
from functools import reduce, cache
from operator import mul
from itertools import product
from math import sqrt
import re

with open("input.txt", "r") as f:
    paragraphs = f.read().split("\n\n")
    tiles = {}
    for paragraph in paragraphs:
        lines = paragraph.split("\n")
        tile_id = lines[0].split(" ")[1][0:-1]
        tiles[tile_id] = lines[1::]

def flip_edge(edge):
    # flip a given edge
    return "".join(reversed(edge))

def get_edge(tile, which):
    # get one of the four edges of a tilel
    # 0 is the top edge, 1 the right, 2 the bottom, and 3 the left
    if which == 0: return tile[0]
    if which == 1: return "".join([tile[x][-1] for x in range(0, 10)])
    if which == 2: return tile[-1]
    if which == 3: return "".join([tile[x][0] for x in range(0, 10)])

# get the four edges of each tile and store it in a dictionary
# for each edge, also check if its flipped version has already been stored
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

# pull out all edges that only are associated with one tile
# put the tile ID associated with them into a counter
# this counts the number of free edges each tile with at least one free edge hass
free_edges = Counter([edges[x][0] for x in edges if len(edges[x]) == 1])
# pull out the corner pieces, they have two free edges
corner_pieces = [x for x in free_edges if free_edges[x] == 2]
# multiple their IDs
answer1 = reduce(mul, map(int, corner_pieces))
print(f"Answer 1: {answer1}")

# bah. assemble the image after all

def rotate_tile(tile):
    return list(map("".join, zip(*reversed(tile))))

def flip_tile(tile):
    return list(reversed(tile))

def is_free_edge(edge):
    if edge not in edges: edge = flip_edge(edge)
    return len(edges[edge]) == 1

def get_neighbors(tile_id):
    neighbors = [edges[edge] for edge in edges if tile_id in edges[edge]]
    neighbors = set([n for x in neighbors for n in x])
    neighbors.remove(tile_id)
    return list(neighbors)

def get_variations(tile):
    for flipped in range(0, 2):
        tile = flip_tile(tile)
        for rotations in range(0, 4):
            tile = rotate_tile(tile)
            yield tile

width = int(sqrt(len(tiles)))
# prepare a data structure that will contain the sorted, properly oriented tiless
oriented_tiles = [[0 for y in range(0, width)] for x in range(0, width)]
# pick a corner piece
# the corner piece has two neighbors, one to the right and one to the bottom
corner_id = corner_pieces[0]
neighbors = get_neighbors(corner_id)
# look for the combination that has the corner first, the right neighbor second
# and the bottom neighbor third
# for that combination, the following conditions are true:
# - the top edge of the corner is free
# - the left edge of the corner is free
# - the top edge of n1 is free
# - the right edge of the corner matches the left edge of n1 exactly
# - the left edge of n2 is free
# - the bottom edge of the corner matches the top edge of n2 exactly

found = False
for cv in get_variations(tiles[corner_id]):
    for n1v in get_variations(tiles[neighbors[0]]):
        for n2v in get_variations(tiles[neighbors[1]]):
            if not get_edge(cv, 1) == get_edge(n1v, 3): continue
            if not get_edge(cv, 2) == get_edge(n2v, 0): continue
            if not is_free_edge(get_edge(cv, 0)): continue
            if not is_free_edge(get_edge(cv, 3)): continue
            if not is_free_edge(get_edge(n1v, 0)): continue
            if not is_free_edge(get_edge(n2v, 3)): continue
            corner, found = cv, True
            break
        if found: break
    if found: break

oriented_tiles[0][0] = (corner_id, corner)

# now that the top left piece is correctly oriented, finding the rest is not hard
# for each row, given the starting piece, find the neighbors, then orient them
# until a left edge matches the right edge exactly. fill the row, then find the
# bottom neighbor of the row starting piece as the next row's starting piece

# first, write a function that determines the correct neighbor variant 
# given a tile and a specific edge to match on
def get_neighbor(t, which):
    tile_id, tile = t
    n_which = (which + 2) % 4
    neighbors = get_neighbors(tile_id)
    edge = get_edge(tile, which)
    for n in neighbors:
        for v in get_variations(tiles[n]):
            if get_edge(v, n_which) == edge:
                return (n, v)

# now work through the grid
for row in range(0, width):
    for col in range(1, width):
        oriented_tiles[row][col] = get_neighbor(oriented_tiles[row][col - 1], 1)
    if row < width - 1:
        oriented_tiles[row + 1][0] = get_neighbor(oriented_tiles[row][0], 2)

# now remove all the edges
def trim_tile(t):
    tile_id, tile = t
    return [line[1:-1] for line in tile[1:-1]]

oriented_tiles = [[trim_tile(cell) for cell in row] for row in oriented_tiles]

# now combine the tiles into one large image
image = []
for row in range(0, width):
    for cell_row in range(0, len(oriented_tiles[0][0][0])):
        image_line = ""
        for cell in range(0, width):
            image_line += oriented_tiles[row][cell][cell_row]
        image.append(image_line)

# regexs yield a wrong result. maybe things overlap?
# do things manually
# first, construct the pattern and record at which index position a # is needed
width = len(image[0])
pattern = "#" + "." * (width - 19)
pattern += "#....##....##....###" + "." * (width - 19)
pattern += "#..#..#..#..#..#"
indexes = [i for i, c in enumerate(pattern) if c == "#"]

# this function takes a substring and checks if there are # in all 
# required positions
def is_monster(s):
    for i in indexes:
        if s[i] != "#": return False
    return True

# create all variations of the image, as it may need to be flipped and rotated
variations = get_variations(image)
for variation in variations:
    # combine the image into one line, and go through it character by character
    # for each of them, check if it's the beginning of a sea monster
    one_line = "".join(variation)
    monsters = 0
    start = 0
    while start <= (len(one_line) - len(pattern)):
        offset = start + len(pattern)
        if is_monster(one_line[start:offset]): monsters += 1
        start += 1
    # only one variation has monsters
    if monsters:
        # this one does. subtract the # for monsters from the total number of #
        roughness = one_line.count("#") - (monsters * pattern.count("#"))
        print(f"Answer 2: {roughness}")
        break