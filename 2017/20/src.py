#!/usr/bin/env python3

import sys
import numpy as np
from collections import Counter

def readInput(withDistance=True):
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  def parse(l):
    fields = l.split("=<")
    result = []
    for field in fields[1:]:
      nums = field.split(">")
      nums = [int(x) for x in nums[0].split(",")]
      result.append(np.array(nums))
    return tuple(result)
  if withDistance:
    return [(parse(l), 0) for l in lines]
  else:
    return [parse(l) for l in lines]

particles = readInput(withDistance=True)
for _ in range(300):
  for i in range(len(particles)):
    ((p, v, a), d) = particles[i]
    d = np.sum(np.abs(p))
    v += a
    p += v
    particles[i] = ((p, v, a), d)

distances = np.array([p[1] for p in particles])
print(f"Solution 1: {np.argmin(distances)}")

particles = readInput(withDistance=False)
for _ in range(300):
  for i in range(len(particles)):
    (p, v, a) = particles[i]
    v += a
    p += v
    particles[i] = (p, v, a)
  counts = Counter([tuple(p[0]) for p in particles])
  particles = [p for p in particles if counts[tuple(p[0])] == 1]

print(f"Solution 2: {len(particles)}")