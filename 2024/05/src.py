#!/usr/bin/env python3

import sys
from itertools import repeat
from collections import defaultdict
from functools import cmp_to_key

with open(sys.argv[1], "r") as f:
    rules, updates = f.read().split("\n\n")

# [(47, 53), (97, 13), ...
rules = [tuple([int(y) for y in x.split("|")]) for x in rules.split("\n")]
# [[75, 47, 61, 53, 29], [97, 61, 53, 29, 13], ...
updates = [[int(y) for y in x.split(",")] for x in updates.split("\n")]


def isValid(update):
    # step through each page in the update
    for i in range(len(update)):
        # generate pairs of page numbers that the opposite
        # of how they appear in this update
        before = list(zip(repeat(update[i]), update[:i]))
        after = list(zip(update[i + 1 :], repeat(update[i])))
        # check if any of those pairs are in the rules
        # if so, that rule was violated, and the update is invalid
        if any([x in rules for x in before + after]):
            return False
    return True


valid = [x[len(x) // 2] for x in filter(isValid, updates)]
print(f"Solution 1: {sum(valid)}")

# create a lookup of what pages come after a specific one
lookup_after = defaultdict(list)
for l, r in rules:
    lookup_after[l].append(r)
# create a closure that acts as a cmp function for pages
sort_pages = lambda x, y: -1 if y in lookup_after[x] else 1

# pull out the invalid updates and re-order them
invalid = [sorted(x, key=cmp_to_key(sort_pages)) for x in updates if not (isValid(x))]
# pull out the middle pages
invalid = [x[len(x) // 2] for x in invalid]
print(f"Solution 2: {sum(invalid)}")
