#!/usr/bin/env python3

import sys
import numpy as np

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [int(x) for x in lines[0].split()]

data = np.array(readInput())
  
cache = {}
count = 0
l = len(data)
while bytes(list(data)) not in cache:
  # cache the current state
  cache[bytes(list(data))] = count
  # get the index of the data bank with the most blocks
  i = data.argmax()
  # retrieve that value
  val = data[i]
  # and set that bank to zero
  data[i] = 0
  # figure out what to add to each bank
  x = val // l
  data += x
  # figure out how many more blocks remain
  x = val % l
  # assume it's a slice that fits into the rest
  end = i + 1 + x
  # does it, tho?
  if end > l:
    # nope, truncate at the end
    left = end - l
    end -= left
    # write out from the beginning
    data[0:left] += 1
  # and write out what fits from this block to the end
  data[i+1:end] += 1
  # increase the count
  count += 1

print(f"Solution 1: {count}")
print(f"Solution 2: {count - cache[bytes(list(data))]}")