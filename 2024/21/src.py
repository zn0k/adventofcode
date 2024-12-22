import sys
from functools import cache

with open(sys.argv[1], "r") as f:
    codes = [l.strip() for l in f.readlines()]


# function to map each button on an input pad to a position
# (0, 0) is the top left corner of the pad
def parse_pad(pad):
    result = {}
    for y, row in enumerate(pad):
        for x, button in enumerate(row):
            result[button] = (x, y)
    return result


# map the number and directional pad buttons
number_pad = parse_pad(["789", "456", "123", "X0A"])
directional_pad = parse_pad(["X^A", "<v>"])


# function to generate the directional moves to get from
# button a to button b given a specific pad
def get_moves(a, b, pad):
    # map buttons to positions
    ax, ay = pad[a]
    bx, by = pad[b]
    gap_x, gap_y = pad["X"]
    # get the necessary x- and y-axis movement
    dx, dy = bx - ax, by - ay

    # translate that to directional symbols
    x_moves = (">" if dx >= 0 else "<") * abs(dx)
    y_moves = ("v" if dy >= 0 else "^") * abs(dy)

    # don't have to move
    if dy == 0 and dx == 0:
        return [""]
    # only have to move on one axis
    elif dy == 0:
        return [x_moves]
    elif dx == 0:
        return [y_moves]
    # have to move around the gap on the keypad
    elif (ax, by) == (gap_x, gap_y):
        return [x_moves + y_moves]
    elif (bx, ay) == (gap_x, gap_y):
        return [y_moves + x_moves]
    # full movement
    else:
        return [x_moves + y_moves, y_moves + x_moves]


# function to build a sequence of moves given an input
def expand(seq, pad):
    result = []
    # we've always starting on the A button
    seq = "A" + seq
    for a, b in zip(seq, seq[1:]):
        result += [[p + "A" for p in get_moves(a, b, pad)]]
    return result


# function to recursively solve for button press sequences
# takes the initial input and the level of depth of recursion
@cache
def solve(seq, d):
    # final recursion level
    if d == 1:
        return len(seq)

    # check which keypad type to use based on the input sequence
    pad = number_pad if any(c in seq for c in "012345679") else directional_pad

    result = 0
    # expand the sequence
    for ps in expand(seq, pad):
        # recursively pick the shortest next sequence of moves this can expand to
        result += min(solve(p, d - 1) for p in ps)
    return result


part1 = 0
for c in codes:
    part1 += solve(c, 4) * int(c[:-1])
print(f"Solution 1: {part1}")

part2 = 0
for c in codes:
    part2 += solve(c, 27) * int(c[:-1])
print(f"Solution 2: {part2}")
