#!/usr/bin/env python3

import sys
import operator as op
from collections import defaultdict

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [l.split() for l in lines]

data = readInput()

# lookup for functions to perform comparison and addition/subtractions
ops = {">": op.gt, "<": op.lt, ">=": op.ge, "<=": op.le, "==": op.eq, "!=": op.ne,
       "inc": op.add, "dec": op.sub}

# keep track of any possible registers, initialized to 0
registers = defaultdict(lambda: 0)

for line in data:
  # pull out the fields of the instruction
  reg, f, arg, _, cmpreg, cmpf, cmparg = line
  # cast the numerical ones
  arg, cmparg = int(arg), int(cmparg)
  # perform the comparison
  result = ops[cmpf](registers[cmpreg], cmparg)
  # perform the inc/dec if the comparison succeeded
  if result: registers[reg] = ops[f](registers[reg], arg)
  # keep track of highest register value after this step
  part1 = max(registers.values())
  # and the highest ever
  part2 = max(part2, part1)

print(f"Solution 1: {part1}")
print(f"Solution 2: {part2}")