#!/usr/bin/env python

from itertools import combinations
import sys

# read in entire file by line
with open(sys.argv[1], "r") as f: 
    input = [l.strip() for l in f.readlines()]

def find_joltage(banks, size):
    # map each bank to its tuples of digits for all combinations
    banks = list(map(lambda x: list(combinations(x, size)), input))
    # join those to a single number, converting to integers
    banks = [[int("".join(x)) for x in b] for b in banks]
    # find the maximums and sum them
    return sum([max(b) for b in banks])
    
s1 = find_joltage(input, 2)
print(f"Solution 1: {s1}")

# of course that's part 2, and of course this won't scale. oh well.
def find_big_joltage(banks, size):
    # map each bank to its digits, as integers
    banks = [[int(x) for x in b] for b in banks]
    joltages = []
    # go through the banks
    for b in banks:
        joltage = []
        # start picking digits up to SIZE
        for i in reversed(range(size)):
            # reserve enough digits at the end to pick the size we need
            # the rest are candidates
            # edge case is i=0 as list[:-0] == []
            # that's the last digit, so just pick from all available
            candidates = b[:-i] if i > 0 else b
            # now pick the largest digit from the candidates
            largest = max(candidates)
            # store it as a string to make it easy to concatenate 
            joltage.append(str(largest))
            # and trim the candidates to the first occurrence
            # be easier with np.argmax, but hey
            b = b[candidates.index(largest)+1:]
        # concatenate all the digits we picked
        joltages.append(int("".join(joltage)))
    # and return the sum
    return sum(joltages)

s2 = find_big_joltage(input, 12)
print(f"Solution 2: {s2}")