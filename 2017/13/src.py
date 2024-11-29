#!/usr/bin/env python3

import sys
from itertools import cycle
from math import gcd

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  def process(line):
    col, depth = line.split(": ")
    return [int(col), int(depth)]
  return [process(line) for line in lines]

def create_cycle(l):
  if l == 0: return cycle([True])
  return cycle([False] + [True] * (l - 1 + l - 2))

layers = readInput()
num_layers = max(x[0] for x in layers) + 1
depths = {k: v for k, v in layers}
firewall = [create_cycle(0)] * num_layers
for x, y in layers:
  firewall[x] = create_cycle(y)
firewall = zip(*firewall)

pos = -1
severity = 0
while pos < (num_layers - 1):
  pos += 1
  safe = next(firewall)
  if not safe[pos]:
    severity += pos * depths[pos]

print(f"Solution 1: {severity}")

# solve analytically instead of simulating it
# cycle length for scanners is 2 * (range - 1)
# scanner position at any time t is t % (2 * (range - 1))
# so for all layers, (delay + depth) % (2 * (range - 1)) must be not equal to 0
# go count up delay values checking for that condition
delay = 0
while True:
  if all((delay + d) % (2 * (r - 1)) != 0 for d, r in layers):
    break
  delay += 1

print(f"Solution 2: {delay}")