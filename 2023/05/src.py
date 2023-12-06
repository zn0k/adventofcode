#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
  sections = f.read().split("\n\n")
  
seeds = list(map(int, sections[0].split(": ")[1].split()))
mappings = [[[int(x) for x in line.split()] for line in s.split("\n")[1:]] for s in sections[1:]]

def translate(seed, mappings):
  def translate_step(seed, mappings):
    for destination, source, length in mappings:
      if source <= seed and seed < source + length:
        return destination + seed - source
    return seed
  
  for mapping in mappings:
    seed = translate_step(seed, mapping)
  return seed

mapped = map(lambda x: translate(x, mappings), seeds)

print(f"Solution 1: {min(mapped)}")
