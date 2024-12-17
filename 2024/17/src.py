#!/usr/bin/env python3

import sys
with open(sys.argv[1], "r") as f: 
  chunks = f.read().split("\n\n")

r = [c.split() for c in chunks[0].split("\n")]
r = {x[1][0]: int(x[2]) for x in r}
program = chunks[1].split("Program: ")[1]
program = list(int(x) for x in program.split(","))

def run(program, a, b, c):
  def combo(op):
    if op >= 4:
      return (a, b, c)[op - 4]
    else:
      return op

  ip = 0
  output = []

  while ip < len(program):
    opcode, operand = program[ip], program[ip + 1]
    match opcode:
      case 0:
        a //= 2 ** combo(operand)
      case 1:
        b ^= operand
      case 2:
        b = combo(operand) & 7
      case 3:
        if a:
          ip = operand - 2
      case 4:
        b ^= c
      case 5:
        output.append(combo(operand) & 7)
      case 6:
        b = a // (2 ** combo(operand))
      case 7:
        c = a // (2 ** combo(operand))
    ip += 2
  return ",".join(map(str, output))

print(f"Solution 1: {run(program, r['A'], r['B'], r['C'])}")