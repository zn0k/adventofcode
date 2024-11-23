#!/usr/bin/env python3

import sys
from collections import defaultdict

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [l.split() for l in lines]

data = readInput()

initial = defaultdict(list)
bots = defaultdict(dict)
for cmd in data:
  if cmd[0] == "value":
    initial[int(cmd[5])].append(int(cmd[1]))
  else:
    bots[int(cmd[1])]["low"] = (cmd[5], int(cmd[6]))
    bots[int(cmd[1])]["high"] = (cmd[10], int(cmd[11]))
    bots[int(cmd[1])]["chips"] = []

for bot, chips in initial.items():
  bots[bot]["chips"] = chips

output_num = 0
for bot in bots.keys():
  if bots[bot]["low"][0] == "output":
    output_num = max(output_num, bots[bot]["low"][1])
  if bots[bot]["high"][0] == "output":
    output_num = max(output_num, bots[bot]["high"][1])

outputs = [0] * (output_num + 1)

solution1 = 0
while 0 in outputs:
  for bot in bots.keys():
    if len(bots[bot]["chips"]) == 2:
      if 61 in bots[bot]["chips"] and 17 in bots[bot]["chips"]:
        solution1 = bot
      for x in ["low", "high"]:
        if x == "low":
          chip = min(bots[bot]["chips"])
        else:
          chip = max(bots[bot]["chips"])
        if bots[bot][x][0] == "output":
          outputs[bots[bot][x][1]] = chip
        else:
          bots[bots[bot][x][1]]["chips"].append(chip)
        bots[bot]["chips"].remove(chip)

print(f"Solution 1: {solution1}")
print(f"Solution 2: {outputs[0] * outputs[1] * outputs[2]}")