#!/usr/bin/env python3

import sys
import numpy as np
from operator import mul, add
from functools import reduce

# read in homework as strings, transposed
homework = np.genfromtxt(sys.argv[1], dtype=str).T
# pull out the operators
operators = homework[:, -1]
# ["*", "+", ...]

# drop operators and convert the rest to integers
homework = homework[:, :-1].astype(int)
# [[123, 45, 6], [328, 64, 98], ...]

# helper functions to reduce lists of integers
# using multiplication and addition
reduce_mul = lambda x: reduce(mul, x, 1)
reduce_add = lambda x: reduce(add, x, 0)
# map the operators to those functions
operators = list(map(lambda x: reduce_mul if x == "*" else reduce_add, operators))

# combine the data with the operator function
combined = [(operators[i], homework[i]) for i in range(len(homework))]
#[(reduce_mul, [123, 45, 6]), (reduce_add, [328, 64, 98]), ...]

# and apply the reducer to the list, sum to solve
solution1 = sum(map(lambda x: x[0](x[1]), combined))
print(f"Solution 1: {solution1}")

# lol, what even is this for part 2. columns aren't even aligned the same way
# read in raw text
with open(sys.argv[1], "r") as f:
    lines = [l.replace("\n", "") for l in f.readlines()]
    homework = lines[:-1]
    ops_line = lines[-1]

# get the column start indices from the line with the operators
idx = [i for i in range(len(ops_line)) if ops_line[i] != " "]
# add the length of a homework line
idx.append(len(homework[0]) + 1)
idx = list(zip(idx, idx[1:]))
# [(0, 4), (4, 8), (8, 12), ...]
# these are now the ranges for each column regardless of alignment

# extract substrings based on those ranges
def extract(line, idx):
    numbers = []
    for start, end in idx:
        sub = line[start:end-1]
        numbers.append(sub)
    return numbers

homework = list(map(lambda x: extract(x, idx), homework))
# [['123', '328', '051', '640'], ['045', '640', '387', '230'], ...]

# transpose to group the columns
homework = [list(row) for row in zip(*homework)]

# now transpose each list element to group columns again
# also concatenate the digits, and cast as an integer
homework = [
    [int("".join(list(row))) for row in zip(*problem)] 
    for problem in homework
]

# and now we can solve as above
# combine the data with the operator function
combined = [(operators[i], homework[i]) for i in range(len(homework))]
#[(reduce_mul, [1, 24, 356]), (reduce_add, [369, 248, 8]]), ...]

# and apply the reducer to the list, sum to solve
solution2 = sum(map(lambda x: x[0](x[1]), combined))
print(f"Solution 2: {solution2}")