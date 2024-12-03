#!/usr/bin/env python3

import sys
import re

with open(sys.argv[1], "r") as f: 
  data = f.read()

products = [int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", data)]
print(f"Solution 1: {sum(products)}")

enabled = True
products = []
matches = re.findall(r"mul\((\d+),(\d+)\)|(do)\(\)|(don't)\(\)", data)
for match in matches:
  if enabled and match[0] and match[1]:
    products.append(int(match[0]) * int(match[1]))
  else:
    if match[2] == "do": enabled = True
    if match[3] == "don't": enabled = False

print(f"Solution 2: {sum(products)}")