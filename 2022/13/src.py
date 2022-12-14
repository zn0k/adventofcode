#!/usr/bin/env python3

import json
from functools import cmp_to_key

with open("input.txt", "r") as f:
    input = [tuple(map(json.loads, chunk.split("\n"))) for chunk in f.read().split("\n\n")]

def cmp(a, b, prefix=""):
    if isinstance(a, int) and isinstance(b, int):
        if a < b: return -1
        if a > b: return 1
        return 0
    if isinstance(a, list) and isinstance(b, list):
        for i in range(min(len(a), len(b))):
            result = cmp(a[i], b[i], prefix + "  ")
            if result != 0: return result 
        if len(a) < len(b): return -1
        if len(a) > len(b): return 1
        return 0
    if isinstance(a, list) and isinstance(b, int): return cmp(a, [b], prefix + "  ")
    if isinstance(a, int) and isinstance(b, list): return cmp([a], b, prefix + "  ")

sum = 0
for idx, pair in enumerate(input):
    if cmp(pair[0], pair[1]) == -1: sum += 1 + idx
print(f"Solution 1: {sum}")

packets = [p for t in input for p in t]
packets.extend([[[2]], [[6]]])
packets = sorted(packets, key=cmp_to_key(cmp))
print("Solution 2: {}".format((packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)))