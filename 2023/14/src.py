#!/usr/bin/env python3

import sys

def get_rocks():
  with open(sys.argv[1], "r") as f:
    rocks = [list(line.strip()) for line in f.readlines()]
  return rocks

def tilt(rocks):
  # rotate so we can work on rows instead of columns
  # reverse the rows for later weighting when calculating load
  # A1 B1 ==> B1 B2
  # A2 B2     A1 A2
  rocks = list(reversed([list(reversed(row)) for row in zip(*reversed(rocks))]))

  for row in range(len(rocks)):
    for col in range(len(rocks[0])):
      if rocks[row][col] == "O":
        move_to = len(rocks[0])
        for back in range(col - 1, -1, -1):
          if rocks[row][back] in "#O" :
            move_to = back + 1
            break
          elif back == 0:
            move_to = 0
        if move_to < col:
          rocks[row][col] = "."
          rocks[row][move_to] = "O"

  return list(zip(*reversed(rocks)))

def score(rocks):
  total = 0
  for i in range(len(rocks)):
    total += rocks[i].count("O") * (len(rocks) - i)
  return total

rocks = tilt(get_rocks())
print(f"Solution 1: {score(rocks)}")

def cycle(rocks):
  # tilt north
  rocks = tilt(rocks)
  # tilt west, which is tilting north after rotating right 90 degrees
  rocks = tilt(list(zip(*reversed(rocks))))
  # and again, which is south
  rocks = tilt(list(zip(*reversed(rocks))))
  # and again, which is east
  rocks = tilt(list(zip(*reversed(rocks))))
  # rotate again so we're back to north
  return list(zip(*reversed(rocks)))

# try and find a larger cycle in the patterns
rocks = get_rocks()
patterns = [rocks]
cycle_start = 0
cycle_end = 0
while(True):
  cycle_end += 1
  rocks = cycle(rocks)
  if rocks in patterns:
    cycle_start = patterns.index(rocks)
    break
  patterns.append(rocks)

cycle_length = cycle_end - cycle_start
offset = cycle_end - cycle_length
target = ((1_000_000_000 - 1 - offset) % cycle_length) + offset + 1
print(f"Solution 2: {score(patterns[target])}")