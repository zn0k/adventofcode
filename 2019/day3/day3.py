from functools import reduce 

with open("input.txt", "r") as f:
    paths = [[x for x in line.rstrip().split(",")] for line in f.readlines()]

def line(o, d, dist):
    d, l = d[0], int(d[1::])
    if d == "R":
        return [(o[0] + x, o[1], dist + x) for x in range(1, l + 1)]
    if d == "L":
        return [(o[0] - x, o[1], dist + x) for x in range(1, l + 1)]
    if d == "U":
        return [(o[0], o[1] + x, dist + x) for x in range(1, l + 1)]
    if d == "D":
        return [(o[0], o[1] - x, dist + x) for x in range(1, l + 1)]

def map_wire(path):
    result = {}
    last = (0, 0)
    distance = 0
    for step in path:
        positions = line(last, step, distance)
        last = (positions[-1][0], positions[-1][1])
        distance = positions[-1][2]
        for p in positions:
            c = (p[0], p[1])
            d = p[2]
            if c not in result:
                result[c] = d
    return result

def manhattan_distance(x):
    return abs(x[0]) + abs(x[1])

wires = list(map(map_wire, paths))
wire_sets = list(map(set, map(lambda x: x.keys(), wires)))
crosses = reduce(lambda x, y: x.intersection(y), wire_sets)
closest_md = min(map(manhattan_distance, crosses))
print(f"Answer 1: {closest_md}")

def count_steps(x):
    return sum([w[x] for w in wires])

fewest_steps = min(map(count_steps, crosses))
print(f"Answer 2: {fewest_steps}")