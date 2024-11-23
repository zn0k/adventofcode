#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [l.split() for l in lines]

data = readInput()

def run():
  pc = 0
  while pc < len(data):
    match data[pc][0]:
      case "cpy": 
        x, y = data[pc][1:]
        c = registers[x] if x in registers else int(x)
        registers[y] = c
        pc += 1
      case "inc":
        x = data[pc][1]
        registers[x] += 1
        pc += 1
      case "dec":
        x = data[pc][1]
        registers[x] -= 1
        pc += 1
      case "jnz":
        x, y = data[pc][1:]
        c = registers[x] if x in registers else int(x)
        if c > 0:
          pc = pc + int(y)
        else:
          pc += 1

registers = {"a": 0, "b": 0, "c": 0, "d": 0}
run()
print(f"Solution 1: {registers['a']}")

registers = {"a": 0, "b": 0, "c": 1, "d": 0}
run()
print(f"Solution 2: {registers['a']}")