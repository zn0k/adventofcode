#!/usr/bin/env python3

import sys
import numpy as np

def processLine(s):
  ws = s.split()
  match ws[0]:
    case "rect":
      x, y = ws[1].split("x")
      return ("rect", int(x), int(y))
    case "rotate":
      _, x = ws[2].split("=")
      return (ws[1], int(x), int(ws[-1]))

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [processLine(s) for s in lines]

data = readInput()

def rect(d, x_max, y_max):
  for x in range(x_max):
    for y in range(y_max):
      d[y][x] = 1
  return d

def row(d, y, l):
  d[y] = np.roll(d[y], l)
  return d

def column(d, x, l):
  d = d.T
  d[x] = np.roll(d[x], l)
  d = d.T
  return d

def pp(d):
  for i in range(len(d)):
    print("".join(map(str, map(int, d[i]))).replace("0", " ").replace("1", "#"))

display = np.zeros((6, 50))

for cmd, x, y in data:
  match cmd:
    case "rect":
      display = rect(display, x, y)
    case "row":
      display = row(display, x, y)
    case "column":
      display = column(display, x, y)

print(f"Solution 1: {int(sum(sum(display)))}")

pp(display)