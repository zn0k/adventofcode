#!/usr/bin/env python3

import sys
from functools import reduce

def readInput():
  with open(sys.argv[1], "r") as f: 
    lines = [l.strip() for l in f.readlines()]
  return lines

data = readInput()

def splitLine(s):
  a = []
  b = []
  while "[" in s:
    x, y = s.split("[", 1)
    a.append(x)
    y, s = y.split("]", 1)
    b.append(y)
  a.append(s)
  return (a, b)

def hasABBA(s):
  for i in range(1, len(s) - 2):
    if s[i] == s[i + 1] and s[i - 1] == s[i + 2] and s[i] != s[i - 1]:
      return True
  return False

def supportsTLS(a, b):
  if any(map(hasABBA, b)): return False
  if any(map(hasABBA, a)): return True
  return False

count = 0
for line in data:
  a, b = splitLine(line)
  if supportsTLS(a, b):
    count += 1

print(f"Solution 1: {count}")

def findABAs(s):
  abas = []
  for i in range(1, len(s) - 1):
    if s[i - 1] == s[i + 1]:
      abas.append(s[i] + s[i - 1] + s[i])
  return abas

def supportsSSL(a, b):
  abas = [x for s in a for x in findABAs(s)]
  bs = " ".join(b)
  if any(map(lambda x: x in bs, abas)): return True
  return False

count = 0
for line in data:
  a, b = splitLine(line)
  if supportsSSL(a, b):
    count += 1

print(f"Solution 2: {count}")