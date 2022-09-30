from itertools import permutations 

with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f.readlines()]
    distances = {}
    for line in lines:
        words = line.split(" ")
        a, b, d = words[0], words[2], int(words[4])
        if a not in distances:
            distances[a] = {}
        if b not in distances:
            distances[b] = {}
        distances[a][b] = d
        distances[b][a] = d

lengths = []
upper = len(distances.keys()) - 1
for p in permutations(distances.keys()):
    l = 0
    for i in range(0, upper):
        l += distances[p[i]][p[i + 1]]
    lengths.append(l)

print(f"Solution 1: {min(lengths)}")
print(f"Solution 2: {max(lengths)}")