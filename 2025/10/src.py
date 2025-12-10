#!/usr/bin/env python3

import sys
from collections import deque

# that's the gnarliest parsing of 2025 so far
machines = []
with open(sys.argv[1], "r") as f:
    # split each line into components separated by spaces
    for components in [l.strip().split(" ") for l in f.readlines()]:
        # first one is the lights, turn them into a string bitmask 00101 etc
        lights = components[0][1:-1].replace(".", "0").replace("#", "1")
        # parse out buttons as lists of integers, but also as bit masks
        buttons = []
        bitmasks = []
        for button in components[1:-1]:
            positions = [int(x) for x in button[1:-1].split(",")]
            buttons.append(positions)
            bitmask = 0
            for p in positions:
                bitmask |= 1 << (len(lights) - p - 1)
            bitmasks.append(bitmask)
        # parse out joltages as tuples of integers, must be tuples to be used in a set
        joltages = tuple(int(x) for x in components[-1][1:-1].split(","))
        # and store the lights target as an integer, the bitmasks, the joltages, and raw buttons
        machines.append((int(lights, 2), bitmasks, joltages, buttons))

# BFS to solve for the lights
# each button press XORs the lights according to its bitmask
# distance walked is number of presses
def solve_machine(lights, buttons):
    # start at 0
    start = 0
    if start == lights:
        return 0
    q = deque([(start, 0)])
    visited = set([start])
    # and walk
    while q:
        state, distance = q.popleft()
        # for each possible button press, generate the next state
        for mask in buttons:
            next_state = state ^ mask
            if next_state == lights:
                # found it, return the number of presses needed to get here
                return distance + 1
            if next_state not in visited:
                # queue up the next possible presses if they don't lead us to 
                # a state we've already seen
                visited.add(next_state)
                q.append((next_state, distance + 1))
    return None

# solve all the light patterns
presses = [solve_machine(lights, buttons) for lights, buttons, _, _ in machines]
# and sum them
print(f"Solution 1: {sum(presses)}")

# this doesn't work, too slow :o(
# # same approach for reaching joltages
# def solve_joltages(joltages, buttons):
#     # have to use tuples for the visited set
#     start = tuple(0 for _ in range(len(joltages)))
#     if start == joltages:
#         return 0
#     q = deque([(start, 0)])
#     visited = set([start])
#     # start walking
#     while q:
#         state, distance = q.popleft()
#         for button in buttons:
#             # convert to a list so we can update it
#             new_state = list(state)
#             # get to use for/else!
#             # increase all the joltages according to the button
#             for p in button:
#                 new_state[p] += 1
#                 # early break if any of the joltages are higher than target
#                 if new_state[p] > joltages[p]:
#                     break
#             else:
#                 # doesn't get us to an impossible state
#                 new_state = tuple(new_state)
#                 if new_state == joltages:
#                     # got there
#                     return distance + 1
#                 # queue up next state
#                 if new_state not in visited:
#                     visited.add(new_state)
#                     q.append((new_state, distance + 1))
#     return None

# presses = [solve_joltages(joltages, buttons) for _, _, joltages, buttons in machines]
# print(f"Solution 2: {sum(presses)}")

from z3 import Int, Optimize, Sum, sat

def solve_joltages_z3(joltages, buttons):
    C = len(joltages)
    # get an optimizer
    opt = Optimize()
    # create one variable per button that represents the number of presses
    x = [Int(f"x_{i}") for i in range(len(buttons))]
    # constrain them to being non-negative
    for i in range(len(buttons)):
        opt.add(x[i] >= 0)
    # button presses must equal the target in joltages
    for i in range(len(joltages)):
        # get the variables that affect that joltage
        filtered = [x[j] for j in range(len(buttons)) if i in buttons[j]]
        if filtered:
            # add the constraint
            opt.add(Sum(filtered) == joltages[i])

    # minimize the total number of presses
    presses = Sum(x)
    opt.minimize(presses)

    # and solve
    if opt.check() != sat:
        return None

    model = opt.model()
    presses = 0
    for j in range(len(buttons)):
        presses += model.eval(x[j]).as_long()

    return presses

presses2 = [solve_joltages_z3(joltages, buttons) for _, _, joltages, buttons in machines]
print(f"Solution 2: {sum(presses2)}")
