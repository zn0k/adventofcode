#!/usr/bin/env python3

with open("input.txt", "r") as f:
    input = [tuple(map(eval, chunk.split("\n"))) for chunk in f.read().split("\n\n")]

def cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return 1
        if a > b:
            return -1
        return 0
    if isinstance(a, list) and isinstance(b, list):
        for i in range(min(len(a), len(b))):
            result = cmp(a[i], b[i])
            if result != 0: return result 
        if len(a) < len(b):
            return 1
        if len(b) > len(a):
            return -1
        return 0
    if isinstance(a, list) and isinstance(b, int):
        return cmp(a, [b])
    if isinstance(a, int) and isinstance(b, list):
        return cmp([a], b)

sum = 0
for idx, pair in enumerate(input):
    if cmp(pair[0], pair[1]) == 1:
        sum += 1 + idx
print(sum)
