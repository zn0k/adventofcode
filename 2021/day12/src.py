from collections import deque

with open("input.txt", "r") as f:
    edges = [tuple(e.split("-")) for e in [l.rstrip() for l in f]]
    successors = {node: set() for node in set([node for edge in edges for node in edge])}
    for x, y in edges:
        successors[x].add(y)
        successors[y].add(x)

def find_paths(start, end, is_valid):
    paths = []
    horizon = deque()
    horizon.appendleft([start])
    while len(horizon):
        path = horizon.pop()
        for neighbor in successors[path[-1]]:
            new_path = path.copy()
            new_path.append(neighbor)
            if neighbor == end:
                paths.append(new_path)
                continue
            if is_valid(path, neighbor):
                horizon.appendleft(new_path)
    return paths

def part1(path, neighbor):
    return neighbor.isupper() or neighbor not in path

def part2(path, neighbor):
    if neighbor == "start": return False
    if neighbor.islower():
        small_caves = list(filter(lambda x: x.islower(), path))
        small_caves.append(neighbor)
        return len(set(small_caves)) + 1 >= len(small_caves)
    return True

paths = find_paths("start", "end", part1)
print(f"Solution 1: {len(paths)}")

paths = find_paths("start", "end", part2)
print(f"Solution 2: {len(paths)}")