#!/usr/bin/env python3

import sys
from functools import reduce
from collections import Counter

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

data = readInput()

total = 0
rooms = []

for room in data:
  parts = room.split("-")
  sector, checksum = parts[-1].split("[")
  checksum = checksum[:-1]
  sector = int(sector)

  counter = Counter(reduce(lambda x, y: x + y, parts[:-1], ""))
  freqs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
  if "".join(map(lambda x: x[0], freqs[:5])) == checksum:
    total += sector
    rooms.append((parts[:-1], sector))

print(f"Solution 1: {total}")

def shiftLetter(l, x):
  n = ord(l) + x
  if n > ord('z'):
    n = ord('a') + n - ord('z') - 1
  return chr(n)

def shiftString(s, x):
  x = x % 26
  return "".join(map(lambda y: shiftLetter(y, x), s))

for parts, sector in rooms:
  name = " ".join(map(lambda x: shiftString(x, sector), parts))
  if name == "northpole object storage":
    print(f"Solution 2: {sector}")