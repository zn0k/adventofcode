#!/usr/bin/env python3

import sys

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return [list(l) for l in lines]

def direction(x):
  match x:
    case "U": return (-1, 0)
    case "D": return (1, 0)
    case "L": return (0, -1)
    case "R": return (0, 1)

def move(a, b):
  x = a[0] + b[0]
  if keypad[x][a[1]] == 0: x = a[0]
  y = a[1] + b[1]
  if keypad[x][y] == 0: y = a[1]
  return (x, y)

data = readInput()
# 0s on the keypad mean moving to that location would be invalid
keypad = [[0, 0, 0, 0, 0], [0, 1, 2, 3, 0], [0, 4, 5, 6, 0], [0, 7, 8, 9, 0], [0, 0, 0, 0, 0]]
pos = (1, 1)
code = ""

for digit_moves in data:
  for m in digit_moves:
    pos = move(pos, direction(m))
  code += str(keypad[pos[0]][pos[1]])

print(f"Solution 1: {code}")

# just a more complex keypad...
keypad = [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0, 0],
          [0, 0, 2, 3, 4, 0, 0],
          [0, 5, 6, 7, 8, 9, 0],
          [0, 0, "A", "B", "C", 0, 0],
          [0, 0, 0, "D", 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]
pos = (3, 1)
code = ""

for digit_moves in data:
  for m in digit_moves:
    pos = move(pos, direction(m))
  code += str(keypad[pos[0]][pos[1]])

print(f"Solution 2: {code}")
