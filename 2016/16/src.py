#!/usr/bin/env python3

import sys

seed = "10011111011011001"

def fill(a, l):
    def gen(a):
      b = "".join(reversed(a))
      b = b.replace("1", "2")
      b = b.replace("0", "1")
      b = b.replace("2", "0")
      return a + "0" + b
    while len(a) < l:
        a = gen(a)
        a = a[:l]
    return a

def checksum(a):
    c = ""
    for i in range(0, len(a) - 1, 2):
        c += "1" if a[i] == a[i + 1] else "0"
    if len(c) % 2 == 0:
        c = checksum(c)
    return c

data = fill(seed, 272)
print(f"Solution 1: {checksum(data)}")

data = fill(seed, 35651584)
print(f"Solution 2: {checksum(data)}")