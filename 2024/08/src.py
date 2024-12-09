#!/usr/bin/env python3

import sys
from collections import defaultdict
from itertools import combinations

with open(sys.argv[1], "r") as f:
    m = [[x for x in l.strip()] for l in f.readlines()]

w, h = len(m), len(m[0])


def valid(p):
    if p.real < 0 or p.real >= w:
        return False
    if p.imag < 0 or p.imag >= h:
        return False
    return True


antennas = [
    (x + y * 1j, m[y][x])
    for y, row in enumerate(m)
    for x, _ in enumerate(row)
    if m[y][x] != "."
]

freq_lookup = defaultdict(list)
for pos, freq in antennas:
    freq_lookup[freq].append(pos)

part1, part2 = set(), set()

for freq, ps in freq_lookup.items():
    for a, b in combinations(ps, r=2):
        d = b - a
        for p in [a - d, b + d]:
            if not valid(p):
                continue
            part1.add(p)
        n = a
        while valid(n):
            part2.add(n)
            n -= d
        n = b
        while valid(n):
            part2.add(n)
            n += d

print(f"Solution 1: {len(part1)}")
print(f"Solution 2: {len(part2)}")
