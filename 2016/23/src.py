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
        pc += 1
        if y not in registers: continue
        registers[y] = c
      case "inc":
        x = data[pc][1]
        pc += 1
        if x not in registers: continue
        registers[x] += 1
      case "dec":
        x = data[pc][1]
        pc += 1
        if x not in registers: continue
        registers[x] -= 1
      case "jnz":
        x, y = data[pc][1:]
        c = registers[x] if x in registers else int(x)
        y = registers[y] if y in registers else int(y)
        if c > 0:
          pc = pc + y
        else:
          pc += 1
      case "tgl":
        x = data[pc][1]
        x = registers[x] if x in registers else int(x)
        x += pc        
        pc += 1
        if x < 0 or x >= len(data): continue
        match len(data[x]):
          case 2:
            match data[x][0]:
              case "inc":
                data[x][0] = "dec"
              case _:
                data[x][0] = "inc"
          case 3:
            match data[x][0]:
              case "jnz":
                data[x][0] = "cpy"
              case _:
                data[x][0] = "jnz"
 
registers = {"a": 7, "b": 0, "c": 0, "d": 0}
run()
print(f"Solution 1: {registers['a']}")


# solution 2 was done on paper
# c = 80 * 97 from the input
# solution is 12!+c