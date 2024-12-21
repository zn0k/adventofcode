#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
    chunks = f.read().split("\n\n")

parts = set(chunks[0].strip().split(", "))
targets = chunks[1].split("\n")

def count_matches(target, parts):
    n = len(target)
    # create a list to check whether substrings up to that 
    # index in the target can be formed from the parts
    # count the number of ways to get there
    checks = [0] * (n + 1)
    # can always form an empty string
    checks[0] = 1
    
    for i in range(n):
        if checks[i]:
            # try extending from current position using each available part
            for part in parts:
                part_length = len(part)
                if i + part_length > n:
                    # position so far plus part is longer than target
                    continue
                if target[i:i + part_length] == part:
                    # we can use this part to extend our match, mark that
                    checks[i + part_length] += checks[i]
    return checks[n]

matches = [count_matches(t, parts) for t in targets]
part1 = [x > 0 for x in matches]
print(f"Solution 1: {sum(part1)}")
print(f"Solution 2: {sum(matches)}")
