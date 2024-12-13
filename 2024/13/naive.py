import sys
import re

with open(sys.argv[1], "r") as f:
    chunks = f.read().split("\n\n")

part1 = 0
part2 = 0
for c in chunks:
    c = c.replace("+", "=")
    xs = list(map(int, re.findall(r"X=(\d+)", c)))
    ys = list(map(int, re.findall(r"Y=(\d+)", c)))
    for n in range(100):
        found = False
        for m in range(100):
            if n * xs[0] + m * xs[1] == xs[2] and n * ys[0] + m * ys[1] == ys[2]:
                part1 += n * 3 + m
                found = True
                break
        if found:
            break

print(f"Solution 1: {part1}")
