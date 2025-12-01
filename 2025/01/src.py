#!/usr/bin/env python3

import sys
from collections import deque

# read in steps to take
with open(sys.argv[1], "r") as f: 
  lines = [l.strip() for l in f.readlines()]
data = [(x[0], int(x[1:])) for x in lines]
# data is now [("L", 68), ("L", 30), ...]

# initialize password
password = 0
# tumbler is a deque with the 99 numbers
tumbler = deque(range(100))
# tumbler starts at 50
tumbler.rotate(50)

# go through the steps
for direction, num in data:
  # for R, rotate right, for L, rotate left
  num = num if direction == "R" else -num
  # move dial
  tumbler.rotate(num)
  # check if dial was 0, if so, increase password
  if tumbler[0] == 0:
    password += 1

print(f"Solution 1: {password}")

# ok, so i was being too cute using a deque
# reset tumbler and password
tumbler = 50
password = 0
# go throught the steps
for direction, num in data:
    # see if we're going left or right
    delta = num if direction == "R" else -num
    # if right, add 1, if left, subtract 1
    offset = 1 if delta > 0 else -1
    # naively simulate the clicks, one by one
    for _ in range(abs(delta)):
        # modulo 100 to reset at boundaries
        tumbler = (tumbler + offset) % 100
        # see if we crossed zero
        if tumbler == 0:
            password += 1

print(f"Solution 2: {password}")
