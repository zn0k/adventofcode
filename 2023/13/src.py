#!/usr/bin/env python3

import sys


with open(sys.argv[1], "r") as f:
  data = f.read()
  chunks = [chunk.split("\n") for chunk in data.split("\n\n")]

# check a chunk for reflection
# return the number of lines above the reflection
# for part 2, take in the current direction, and previous reflection
# in the format of ("h|v", line)
def check_reflection(chunk, direction, ignore):
  for i in range(1, len(chunk)):
    top = chunk[0:i]
    bottom = chunk[i:]
    above = len(top)
    if len(top) < len(bottom):
      bottom = bottom[0:len(top)]
    if len(top) > len(bottom):
      top = top[len(top)-len(bottom):]
    bottom = list(reversed(bottom))
    if "".join(top) == "".join(bottom) and (direction, above) != ignore:
      return above
  return 0

def score(chunk, ignore=("h", -1)):
  # first check for a horizontal reflection
  val = check_reflection(chunk, "h", ignore=ignore)
  if val:
    return val * 100
  else:
    # didn't reflect horizontally. rotate right 90 degrees
    # then check for horizontal reflection again
    chunk = ["".join(x) for x in zip(*chunk[::-1])]
    return check_reflection(chunk, "v", ignore=ignore)


scores = list(map(score, chunks))
print(f"Solution 1: {sum(scores)}")

# let's try brute forcing it. runs in 0.04 seconds for step 1
# the biggest chunks are around 300 characters, so this should 
# still run in under 30 seconds. edit: runs in 0.2 seconds, that's fine
def iterate(idx, chunk):
  for y in range(len(chunk)):
    for x in range(len(chunk[0])):
      prior = chunk[y][x]
      if prior == ".":
        chunk[y] = chunk[y][0:x] + "#" + chunk[y][x+1:]
      else:
        chunk[y] = chunk[y][0:x] + "." + chunk[y][x+1:]
      # recover the previous reflection and its direction from the score
      if scores[idx] < 100:
        previous_reflection = ("v", scores[idx])
      else:
        previous_reflection = ("h", scores[idx] // 100)
      # get the other reflection
      val = score(chunk, ignore=previous_reflection)
      # found it, non-zero value
      if val:
        return val
      # not done yet, put it back together and go through another loop
      chunk[y] = chunk[y][0:x] + prior + chunk[y][x+1:]
  return 0

alternate_scores = list(map(lambda x: iterate(*x), enumerate(chunks)))
print(f"Solution 2: {sum(alternate_scores)}")