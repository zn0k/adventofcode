#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [l.split() for l in lines]

data = readInput()

def run(a):
  registers = {"a": a, "b": 0, "c": 0, "d": 0}
  pc = 0
  output = []
  while pc < len(data) and len(output) < 50:
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
      case "out":
        x = data[pc][1]
        c = registers[x] if x in registers else int(x)
        output.append(c)
        pc += 1
  solved = True
  for i in range(0, len(output), 2):
    if output[i] != 0:
      solved = False
      break
  for i in range(1, len(output), 2):
    if output[i] != 1:
      solved = False
      break
  return solved

a = 0
while True:
  solved = run(a)
  if solved:
    print(f"Solution 1: {a}")
    break
  a += 1