import itertools

def calculate_neighbor(x):
    p, d = x
    return tuple([p[x] + d[x] for x in range(0, len(p))])

def validate_point(p):
    for dim in range(0, len(p)):
        if not 0 <= p[dim] < size: return False
    return True

def get_neighbors(p):
    r = [-1, 0, 1]
    offsets = set(itertools.product(r, repeat=len(p)))
    offsets.remove(tuple([0 for x in range(0, len(p))]))
    neighbors = itertools.zip_longest([], offsets, fillvalue=p)
    neighbors = filter(validate_point, map(calculate_neighbor, neighbors))
    return list(neighbors)

def get_state(p):
    coordinates = list(p)
    element = data
    while len(coordinates):
        index = coordinates.pop(0)
        element = element[index]
    return element

def new_state(p):
    n = sum(map(get_state, get_neighbors(p)))
    return 1 if ((get_state(p) and n in [2, 3]) or (not get_state(p) and n == 3)) else 0

def iterate():
    print(".")
    r = range(0, size)
    if dimensions == 3:
        new = [[[new_state((x, y, z)) for z in r] for y in r] for x in r]
    elif dimensions == 4:
        new = [[[[new_state((x, y, z, w)) for w in r] for z in r] for y in r] for x in r]
    return new

iterations = 6
dimensions = 3

def initialize():
    with open("input.txt", "r") as f:
        lines = f.read().split("\n")
        size = len(lines[0]) + iterations * 2
        offset = int((size - len(lines[0])) / 2)
        r = range(0, size)
        if dimensions == 3:
            data = [[[0 for z in r] for y in r] for x in r]
        elif dimensions == 4:
            data = [[[[0 for w in r] for z in r] for y in r] for x in r]
        for x, line in enumerate(lines):
            for y, state in enumerate(line):
                state = 1 if state == "#" else 0
                if dimensions == 3:
                    data[x + offset][y + offset][offset + 1] = state
                elif dimensions == 4:
                    data[x + offset][y + offset][offset + 1][offset + 1] = state
        return (size, data)

size, data = initialize()
for step in range(0, iterations):
    data = iterate()

total = sum([sum([sum([z for z in y]) for y in x]) for x in data])
print(f"Answer 1: {total}")

dimensions = 4
size, data = initialize()
for step in range(0, iterations):
    data = iterate()

total = sum([sum([sum([sum([w for w in z]) for z in y]) for y in x]) for x in data])
print(f"Answer 2: {total}")