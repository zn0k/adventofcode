#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [int(x) for x in lines]

data = readInput()
pc = 0
c = 0
while pc >= 0 and pc < len(data):
  c += 1
  opc = pc
  pc += data[pc]
  data[opc] += 1

print(f"Solution 1: {c}")

data = readInput()
pc = 0
c = 0
while pc >= 0 and pc < len(data):
  c += 1
  opc = pc
  pc += data[pc]
  data[opc] += -1 if data[opc] >= 3 else 1

print(f"Solution 2: {c}")