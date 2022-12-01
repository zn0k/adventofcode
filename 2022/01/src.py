#!/usr/bin/env python3

with open("input.txt", "r") as f:
    elves = list()
    elf = list()
    for line in f.readlines():
        if line.rstrip():
            elf.append(int(line))
        else:
            elves.append(sum(elf))
            elf = list()

elves = sorted(elves)
print(f"Solution 1: {elves[-1]}\nSolution 2: {sum(elves[-4:-1])}")