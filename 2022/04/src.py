#!/usr/bin/env python3

with open("input.txt", "r") as f:
    pairs = [[list(map(int, field.split("-"))) for field in line.split(",")] for line in f.readlines()]

sets = list(map(lambda x: list(map(lambda y: set(range(y[0], y[1]+1)), x)), pairs))
subsets = list(map(lambda x: x[0] <= x[1] or x[1] <= x[0], sets)).count(True)
overlap = list(map(lambda x: not(x[0].isdisjoint(x[1])), sets)).count(True)
print(f"Solution 1: {subsets}\nSolution 2: {overlap}")