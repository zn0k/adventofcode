#!/usr/bin/env python3

import sys
from itertools import cycle
from math import lcm

with open(sys.argv[1], "r") as f:
  lines = [line.strip() for line in f.readlines()]

instructions = list(lines[0])
node_map = {}
for line in lines[2:]:
  fields = line.replace("(", "").replace(")", "").replace(", ", ",").replace(" = ", ",").split(",")
  node_map[fields[0]] = (fields[1], fields[2])

def findCycle(node, stopCondition):
  move_map = {"L": 0, "R": 1}
  counter = 0
  for move in cycle(instructions):
    node = node_map[node][move_map[move]]
    counter += 1
    if stopCondition(node): break
  return counter

print(f"Solution 1: {findCycle('AAA', lambda x: x == 'ZZZ')}")

start_nodes = [node for node in node_map.keys() if node.endswith("A")]
cycle_lengths = [findCycle(node, lambda x: x.endswith("Z")) for node in start_nodes]

print(f"Solution 2: {lcm(*cycle_lengths)}")