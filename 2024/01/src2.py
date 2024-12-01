#!/usr/bin/env python3

import numpy as np

data = np.loadtxt("input.txt")
left, right = np.sort(data.T)
print(int(np.sum(np.abs(left - right))))
print(int(np.sum([x * np.sum(x == right) for x in left])))