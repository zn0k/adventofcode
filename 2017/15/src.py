#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  lines = [l.split() for l in lines]
  return [int(l[-1]) for l in lines]

data = readInput()

def generator(seed, factor, picky=0):
  prev = seed
  while True:
    prev = (prev * factor) % 2147483647
    while picky > 0 and prev % picky != 0:
      prev = (prev * factor) % 2147483647
    yield prev

gen_a = generator(data[0], 16807)
gen_b = generator(data[1], 48271)

reps = 40_000_000
count = 0
for i in range(reps):
  a = next(gen_a)
  b = next(gen_b)
  vals = [bin(x)[::-1][0:16] for x in [a, b]]
  if vals[0] == vals[1]: count += 1

print(f"Solution 1: {count}")

gen_a = generator(data[0], 16807, 4)
gen_b = generator(data[1], 48271, 8)

reps = 5_000_000
count = 0
for i in range(reps):
  a = next(gen_a)
  b = next(gen_b)
  vals = [bin(x)[::-1][0:16] for x in [a, b]]
  if vals[0] == vals[1]: count += 1

print(f"Solution 2: {count}")