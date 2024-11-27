#!/usr/bin/env python3

import sys
from collections import deque

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

data = readInput()

password = list("abcdefgh")

for line in data:
  fields = line.split()
  cmd = f"{fields[0]} {fields[1]}"
  match cmd:
    case "swap position":
      i, j = int(fields[2]), int(fields[5])
      password[i], password[j] = password[j], password[i]
    case "swap letter":
      letter_a, letter_b = fields[2], fields[5]
      i, j = password.index(letter_a), password.index(letter_b)
      password[i], password[j] = password[j], password[i]
    case "rotate left" | "rotate right":
      i = int(fields[2])
      if fields[1] == "left": i *= -1
      password = deque(password)
      password.rotate(i)
      password = list(password)
    case "rotate based":
      letter = fields[-1]
      i = password.index(letter)
      i = i + (2 if i >= 4 else 1)
      password = deque(password)
      password.rotate(i)
      password = list(password)
    case "reverse positions":
      i, j = int(fields[2]), int(fields[4])
      password = password[:i] + list(reversed(password[i:j+1])) + password[j+1:]
    case "move position":
      i, j = int(fields[2]), int(fields[5])
      letter = password.pop(i)
      password = password[:j] + [letter] + password[j:]

password = "".join(password)

print(f"Solution 1: {password}")

password = list("fbgdceah")

for line in reversed(data):
  fields = line.split()
  cmd = f"{fields[0]} {fields[1]}"
  match cmd:
    case "swap position":
      i, j = int(fields[2]), int(fields[5])
      password[i], password[j] = password[j], password[i]
    case "swap letter":
      letter_a, letter_b = fields[2], fields[5]
      i, j = password.index(letter_a), password.index(letter_b)
      password[i], password[j] = password[j], password[i]
    case "rotate left" | "rotate right":
      i = int(fields[2])
      if fields[1] == "right": i *= -1
      password = deque(password)
      password.rotate(i)
      password = list(password)
    case "rotate based":
      letter = fields[-1]
      for i in range(len(password)):
        test = deque(password)
        test.rotate(i * -1)
        test = list(test)
        i = test.index(letter)
        i = i + (2 if i >= 4 else 1)
        scrambled = deque(test)
        scrambled.rotate(i)
        scrambled = list(scrambled)
        if scrambled == password:
          break
      password = test
    case "reverse positions":
      i, j = int(fields[2]), int(fields[4])
      password = password[:i] + list(reversed(password[i:j+1])) + password[j+1:]
    case "move position":
      i, j = int(fields[2]), int(fields[5])
      letter = password.pop(j)
      password = password[:i] + [letter] + password[i:]

password = "".join(password)

print(f"Solution 2: {password}")
