#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [[int(x) for x in l.split()] for l in lines]

data = readInput()

def isLegal(sides):
  a, b, c = sides
  return (a + b > c and a + c > b and b + c > a)

legal = list(filter(isLegal, data))
print(f"Solution 1: {len(legal)}")

# quick and dirty "transpose"
new_data = []
for y in [0, 1, 2]:
  for x in range(0, len(data), 3):
    t = [data[x][y], data[x + 1][y], data[x + 2][y]]
    new_data.append(t)

legal = list(filter(isLegal, new_data))
print(f"Solution 1: {len(legal)}")