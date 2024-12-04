#!/usr/bin/env python3

import sys
import numpy as np

matrix = np.genfromtxt(sys.argv[1], dtype="U1", delimiter=1)

# extract all diagonals from a given matrix
def diagonals(matrix):
    rows, cols = matrix.shape
    result = []
    for diag in range(-(rows - 1), cols):
        result.append(np.diagonal(matrix, offset=diag))
    return result

# get all rows, columns and diagonals
lines = [row for row in matrix] \
      + [col for col in matrix.T] \
      + diagonals(matrix) \
      + diagonals(np.fliplr(matrix))
# merge them into strings
lines = ["".join(line) for line in lines]
# now count the instances of XMAS and SAMX in each
count = sum([line.count("XMAS") + line.count("SAMX") for line in lines])
print(f"Solution 1: {count}")

# that's no good for part 2. just find all A's by marching coordinates
# then check their diagonals and make sure they have adjacent S's and M's
count = 0
for y in range(1, len(matrix) - 1):
    for x in range(1, len(matrix[y]) - 1):
        if matrix[y][x] == "A":
            match = True
            for (dx1, dy1), (dx2, dy2) in [((-1, -1), (1, 1)), ((1, -1), (-1, 1))]:
                diagonal = (matrix[y + dy1][x + dx1], matrix[y + dy2][x + dx2])
                if "M" not in diagonal or "S" not in diagonal: match = False
            if match: count += 1 
print(f"Solution 2: {count}")