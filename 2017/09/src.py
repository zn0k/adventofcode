#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

data = readInput()

# meh, spaghetti code. i don't enjoy this type of puzzle
def process_stream(data):
  score = 0
  total = 0
  garbage = False
  ignore_next = False
  clear_after = False
  garbage_chars = 0
  for i in range(len(data)):
    if ignore_next: clear_after = True
    match data[i]:
      case "{":
        if not garbage:
          score += 1
        else:
          if not ignore_next:
            garbage_chars += 1
      case "}":
        if not garbage:
          total += score
          score -= 1
        else:
          if not ignore_next:
            garbage_chars += 1
      case "<":
        if not garbage:
          garbage = True
        else:
          if not ignore_next:
            garbage_chars += 1
      case "!":
        if garbage and not ignore_next:
          ignore_next = True
      case ">":
        if garbage and not ignore_next:
          garbage = False
      case _:
        if garbage and not ignore_next:
          garbage_chars += 1
    if clear_after:
      clear_after = False
      ignore_next = False
  return (total, garbage_chars)

total, garbage_chars = process_stream(data[-1])
print(f"Solution 1: {total}")
print(f"Solution 2: {garbage_chars}")