#!/usr/bin/env python3

import sys

# read in entire file
with open(sys.argv[1], "r") as f: 
  input = f.read()

# split it into tuples of ranges (ints)
data = []
for r in input.split(","):
  data.append(tuple(map(int, r.split("-"))))

invalid = []
# go through the ranges
for start, end in data:
  # process each number in the range, inclusive of the end
  for i in range(start, end + 1):
    # turn that back into a string
    i = str(i)
    # split it at the midpoint
    mid = len(i) // 2
    # check if the two halves are the same
    if i[:mid] == i[mid:]:
      invalid.append(int(i))

print(f"Solution 1: {sum(invalid)}")

# function to determine if a string is solely made of
# repeating substrings
def is_invalid(s):
  # start with substring lengths of 1, building up to
  # half the input
  for i in range(1, len(s) // 2 + 1):
    # grab the substring of that lenght
    sub = s[:i]
    # check if we can multiply it to end up
    # at the length of the input
    if len(s) % len(sub) == 0:
      # we can, check if multplying it that
      # often gets us to the substring
      if sub * (len(s) // len(sub)) == s:
        return True
  return False

invalid = []
# go through the ranges
for start, end in data:
  # check each number in the range
  for i in range(start, end + 1):
    if is_invalid(str(i)):
      invalid.append(i)

print(f"Solution 2: {sum(invalid)}")