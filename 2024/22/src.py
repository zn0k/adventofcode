#!/usr/bin/env python3

import sys
from collections import defaultdict

with open(sys.argv[1], "r") as f:
    seeds = [int(l.strip()) for l in f.readlines()]


# evolve a given seed over 2000 rounds
# returns the seed value followed by all values
def evolve(a, n):
    rounds = [a]
    for _ in range(n):
        x = a * 64
        a ^= x
        a %= 16777216
        x = a // 32
        a ^= x
        a %= 16777216
        x = a * 2048
        a ^= x
        a %= 16777216
        rounds.append(a)
    return rounds


# evolve each seed for 2000 rounds
secrets = [evolve(s, 2000) for s in seeds]

# sum up just the last values
part1 = sum(s[-1] for s in secrets)
print(f"Solution 1: {part1}")

# pull out the right-most digits
rs = [[x % 10 for x in s] for s in secrets]
# generate a list of deltas from value to value
ds = [[b - a for a, b in zip(r, r[1:])] for r in rs]

# use a dictionary to sum up the bananas for each sequence
part2 = defaultdict(int)
# march through all the buyers
for i in range(len(ds)):
    # keep track of sequences we've seen for this buyer
    seen = set()
    # march through all the sequences for this buyer
    for j, seq in enumerate(zip(ds[i], ds[i][1:], ds[i][2:], ds[i][3:])):
        # if we've seen this sequence before, ignore it
        if seq in seen:
            continue
        # pull out the bananas we'd get for this sequence and tally it
        # it's the same index + 4 due to the length of the sequence and the 
        # one-off difference due to the deltas being one shorter
        part2[seq] += rs[i][j + 4]
        # remember the sequence
        seen.add(seq)

part2 = max(part2.values())
print(f"Solution 2: {part2}")
