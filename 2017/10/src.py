#!/usr/bin/env python3

import sys
import numpy as np
from functools import reduce

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [int(x) for l in lines for x in l.split(",")]

def readInput2():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines[0]

lengths = np.array(readInput())

elements = 256
data = np.arange(elements)

pos = 0
skip = 0

for length in lengths:
  data[0:length] = data[0:length][::-1]
  data = np.roll(data, (length + skip) * -1)
  pos += length + skip
  skip += 1

data = np.roll(data, pos)
print(f"Solution 1: {data[0] * data[1]}")

def knot_hash(input):
  lengths = [ord(x) for x in input] + [17, 31, 73, 47, 23]
  pos, skip = 0, 0
  data = np.arange(256)
  for _ in range(64):
    for length in lengths:
      data[0:length] = data[0:length][::-1]
      data = np.roll(data, (length + skip) * -1)
      pos += length + skip
      skip += 1
  data = np.roll(data, pos)
  dense = [reduce(np.bitwise_xor, data[p:p+16]) for p in range(0, 256, 16)]
  return "".join(["%02x" % x for x in dense])

data = readInput2()
print(f"Solution 2: {knot_hash(data)}")
