#!/usr/bin/env python3

from functools import reduce

with open("input.txt", "r") as f:
    games = [tuple(l.split()) for l in f.readlines()]

lookup = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
lookup2 = {"X": 0, "Y": 3, "Z": 6}

def score1(x):
    p1, p2 = x
    if (lookup[p2] == lookup[p1] + 1) or (p1 == "C" and p2 == "X"):
        return 6
    if lookup[p1] == lookup[p2]:
        return 3
    return 0

def score2(x):
    def sub(x): return lookup[x] - 1 if lookup[x] - 1 >= 1 else 3
    def add(x): return lookup[x] + 1 if lookup[x] + 1 <= 3 else 1
    p1, move = x
    result = 0
    if move == "X": return sub(p1)
    if move == "Y": return lookup[p1]
    return add(p1)

sol1 = reduce(lambda x, y: (score1(y) + lookup[y[1]]) + x, games, 0)
sol2 = reduce(lambda x, y: (score2(y) + lookup2[y[1]]) + x, games, 0)

print(f"Solution 1: {sol1}\nSolution 2: {sol2}")