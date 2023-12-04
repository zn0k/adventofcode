#!/usr/bin/env python3

import sys
from collections import deque

def readInput():
  with open(sys.argv[1], "r") as f:
    # list of list of characters, which can be addressed as (x,y) coordinates
    return [[*line.strip()] for line in f.readlines()]
  
manual = readInput()

# find the (x,y) coordinates of all cells that match the given condition
def findSymbols(condition):
  symbols = set()
  for y in range(len(manual)):
    for x in range(len(manual[0])):
      if condition(x, y):
        symbols.add((x, y))
  return symbols

# find all the symbols in the manual
symbols = findSymbols(lambda x, y: manual[y][x] not in ".0123456789")

# helper function to determine if a coordinate is in bounds
def valid(x, y):
  if x < 0 or x >= len(manual[0]): return False
  if y < 0 or y >= len(manual): return False
  return True

# find all adjacent digits given a starting set of symbols
def findDigits(symbols):
  # find all neighbors of cells that contain symbols
  def generateStartCells(symbols):
    start = set()
    for x, y in symbols:
      for neighbor in [(x-1,y),(x-1,y-1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1)]:
        if valid(*neighbor):
          start.add(neighbor)
    return start

  # create a queue, initially filled with neighbors of symbols
  # for each location, determine if it is a digit and mark it so
  # also find digit's neighbors to the left and right, and add those to the queue
  q = deque(generateStartCells(symbols))
  digits = set()
  while len(q):
    # get the candidate location from the queue
    x, y = q.popleft()
    # skip ahead if it's already been looked at to prevent loops
    if (x,y) in digits: continue
    # check if the character there is a digit
    if manual[y][x].isdigit():
      digits.add((x, y))
      # grab all its valid neighbors and add them to the queue
      if valid(x - 1, y): q.append((x - 1, y))
      if valid(x + 1, y): q.append((x + 1, y))
  return digits

digits = findDigits(symbols)

# clean up the manual given the location of good known digits
def cleanManual(digits):
  # create a manual with just valid digits in it
  clean = ["".join([manual[y][x] if (x, y) in digits else " " for x in range(len(manual[0]))]) for y in range(len(manual))]
  # split those numbers on spaces, flattening that list
  numbers = [x for line in map(lambda x: x.split(" "), clean) for x in line]
  # filter out the empty strings
  numbers = filter(lambda x: x != "", numbers)
  # map them to ints
  return list(map(int, numbers))

# sum up all the numbers in a cleaned up manual
print(f"Solution 1: {sum(cleanManual(digits))}")

# find the locations of all the '*' cells
symbols = findSymbols(lambda x, y: manual[y][x] == "*")
gears = []
# this time, go through them one by one and find the parts for just each gear
for symbol in symbols:
  # generate the cleaned up manual based on that gear position
  parts = findDigits([symbol])
  cleaned = cleanManual(parts)
  # check if the candidate is valid due to having exactly two neighbor numbers
  if len(cleaned) == 2:
    gears.append(cleaned[0] * cleaned[1])

print(f"Solution 2: {sum(gears)}")