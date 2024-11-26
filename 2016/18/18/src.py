#!/usr/bin/env python3

import numpy as np
import math

seed = 3018458
#seed = 5

# create a list of elves playing
elves = np.arange(seed) + 1

# go until there's a winner
while len(elves) > 1:
    # check if there's an odd number of elves
    odd = False if len(elves) % 2 == 0 else True
    # remove every second elf as the elf before it takes its presents
    elves = elves[::2]
    # if we started with an odd number, the last elf takes the presents
    # of the first elf, so kick the first elf out
    if odd: elves = elves[1:]

# remaining elf is the winner
print(f"Solution 1: {elves[0]}")

# part 2 done on paper to discover the pattern the below formula expresses
x = 3 ** int(math.log(seed - 1, 3))
solution2 = seed - x + max(seed - 2 * x, 0)

print(f"Solution 2: {solution2}")