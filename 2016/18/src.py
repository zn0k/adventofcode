#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

data = readInput()[0]
data = data.replace(".", "1").replace("^", "0")
rows = 10 if sys.argv[1] == "test.txt" else 40

floor = [[int(x) for x in data]]

def generate_row(row):
    new = []
    for i in range(len(row)):
        left = row[i - 1] if i >= 1 else 1
        center = row[i]
        right = row[i + 1] if i < len(row) - 1 else 1
        tile = 1
        if left == 0 and center == 0 and right == 1: tile = 0
        if left == 1 and center == 0 and right == 0: tile = 0
        if left == 0 and center == 1 and right == 1: tile = 0
        if left == 1 and center == 1 and right == 0: tile = 0
        new.append(tile)
    return new

for _ in range(rows - 1):
    floor.append(generate_row(floor[-1]))

safe = sum(map(lambda x: sum(x), floor))
print(f"Solution 1: {safe}")

floor = [[int(x) for x in data]]
rows = 400000
for _ in range(rows - 1):
    floor.append(generate_row(floor[-1]))

safe = sum(map(lambda x: sum(x), floor))
print(f"Solution 2: {safe}")