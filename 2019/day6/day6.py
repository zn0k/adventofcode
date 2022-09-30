with open("input.txt", "r") as f:
    orbits = {}
    for line in f.readlines():
        left, right = line.rstrip().split(")")
        orbits[right] = left

def expand(obj):
    if orbits[obj] == "COM":
        return [orbits[obj]]
    else:
        return [orbits[obj]] + expand(orbits[obj])

expanded = {obj: expand(obj) for obj in orbits.keys()}
checksum = sum(map(lambda x: len(expanded[x]), expanded.keys()))
print(f"Answer 1: {checksum}")

me = set(expanded["YOU"])
santa = set(expanded["SAN"])
common = me.intersection(santa)
unique = me.union(santa) - me.intersection(santa)
print(f"Answer 2: {len(unique)}")