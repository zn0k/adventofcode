#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f:
    return [line.strip() for line in f.readlines()]

data = readInput()

def extract(line, findWords=False):
  patterns = { "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
  digits = []

  # build a scanner that extracts digits
  while len(line):
    found = False
    # check if it's a single digit
    for digit in patterns.values():
      if line.startswith(digit):
        # found a single digit. store it, and remove it from the beginning of the string
        digits.append(digit)
        line = line[1:]
        found = True
    if findWords:
      for word in patterns.keys():
        if line.startswith(word):
          # looking for words, and found one. store it.
          digits.append(patterns[word])
          # remove all but its last letter from the beginning of the string
          # so that words can run into one another
          line = line[len(word)-1:]
          found = True
    if not found:
      # didn't find anything, advance scanner by one character
      line = line[1:]

  if len(digits):
    return int(digits[0] + digits[-1])
  else:
    return 0
  
values = map(lambda x: extract(x, findWords=False), data)
print(f"Solution 1: {sum(values)}")

values = map(lambda x: extract(x, findWords=True), data)
print(f"Solution 2: {sum(values)}")