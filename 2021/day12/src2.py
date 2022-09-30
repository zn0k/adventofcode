from collections import deque, defaultdict

with open("input.txt", "r") as f:
    edges = [tuple(e.split("-")) for e in [l.rstrip() for l in f]]
    successors = defaultdict(set)
    for x, y in edges:
        successors[x].add(y)
        successors[y].add(x)

def find_paths(node, seen, allow_small_cave_repeat):
    num_paths = 0
    if node == "end":
        return 1
    if node == "start" and len(seen):
        return 0
    if node.islower() and node in seen:
        if allow_small_cave_repeat:
            allow_small_cave_repeat = False
        else:
            return 0
    seen = seen | {node}
    for neighbor in successors[node]:
        num_paths += find_paths(neighbor, seen, allow_small_cave_repeat)
    return num_paths    

print(f"Solution 1: {find_paths('start', set(), False)}")
print(f"Solution 2: {find_paths('start', set(), True)}")