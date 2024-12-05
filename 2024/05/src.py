#!/usr/bin/env python3

import sys
from itertools import repeat

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


# make a more correct version of the order of an update
def shuffle(update):
    # start with the first element in the update
    new_order = [update[0]]
    for page in update[1:]:
        # find the rule that covers the new page and the last page in the new order
        rule = [r for r in rules if page in r and new_order[-1] in r][0]
        # depending on the rule, insert the new page just before the last page
        # or append it
        if page == rule[0]:
            new_order = new_order[:-1] + [page] + [new_order[-1]]
        else:
            new_order = new_order + [page]
    return new_order


# keep shuffling the update until the order is valid
def reorder(update):
    while not (isValid(update)):
        update = shuffle(update)
    return update


# pull out the invalid updates and re-order them
invalid = [reorder(x) for x in updates if not (isValid(x))]
# pull out the middle pages
invalid = [x[len(x) // 2] for x in invalid]
print(f"Solution 2: {sum(invalid)}")
