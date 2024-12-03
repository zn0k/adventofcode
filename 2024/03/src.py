#!/usr/bin/env python3

import sys
import re

with open(sys.argv[1], "r") as f: 
  data = f.read()

products = [int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", data)]
print(f"Solution 1: {sum(products)}")

cleaned = re.sub(r"don't\(\).*?do\(\)", "", data + "do()", flags=(re.DOTALL | re.MULTILINE))
products = [int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", cleaned)]
print(f"Solution 2: {sum(products)}")