#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

def extractMarker(s):
  m, s = s.split(")", 1)
  parts = m.split("x", 1)
  return (int(parts[0]), int(parts[1]), s)

data = readInput()[0]
expanded = 0
while "(" in data:
  prefix, data = data.split("(", 1)
  expanded += len(prefix)
  c, f, data = extractMarker(data)
  cd = data[:c]
  data = data[c:]
  expanded += len(cd * f)
expanded += len(data)

print(f"Solution 1: {expanded}")

data = readInput()[0]
expanded = 0
while "(" in data:
  prefix, data = data.split("(", 1)
  expanded += len(prefix)
  c, f, data = extractMarker(data)
  cd = data[:c]
  data = (cd * f) + data[c:]
expanded += len(data)

print(f"Solution 2: {expanded}")