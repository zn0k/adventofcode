#!/usr/bin/env python3

import sys
from bisect import insort


def checksum(disk):
    chksum = 0
    for i, d in enumerate(disk):
        if d is not None:
            chksum += i * d
    return chksum


def expand(disk):
    free = []
    used = []
    file_id = 0
    offset = 0
    is_file = True
    for length in disk:
        if is_file:
            used.append([file_id, length, offset])
            file_id += 1
        else:
            free.append([offset, length])
        offset += length
        is_file = not (is_file)
    return (used, free)


with open(sys.argv[1], "r") as f:
    input = [int(x) for x in f.read().strip()]

used, free_list = expand(input)
total_length = 0
for i in range(0, len(input), 2):
    total_length += input[i]

free = []
for offset, length in free_list:
    for i in range(length):
        free.append(offset + i)

part1 = [0] * total_length

free_offset = free[0]
for i in range(len(used) - 1, 0, -1):
    if len(free) == 0 or free_offset > total_length:
        break
    file = used.pop()
    while file[1] > 0:
        if len(free) == 0:
            break
        free_offset = free.pop(0)
        if free_offset > total_length:
            break
        part1[free_offset] = file[0]
        file[1] -= 1
    if file[1] > 0:
        used.append(file)

for file in used:
    for j in range(file[2], file[2] + file[1]):
        part1[j] = file[0]

print(f"Solution 1: {checksum(part1)}")

used, free_list = expand(input)
free = {k: [] for k in range(0, 10)}
for offset, length in free_list:
    free[length].append(offset)

for i in range(len(used) - 1, 0, -1):
    min_free_offset = used[i][2]
    for j in range(used[i][1], 10):
        if len(free[j]) and free[j][0] < min_free_offset:
            min_free_offset = free[j][0]
            min_free_length = j
    if min_free_offset < used[i][2]:
        used[i][2] = min_free_offset
        free[min_free_length].pop(0)
        if min_free_length > used[i][1]:
            new_free_offset = min_free_offset + used[i][1]
            insort(free[min_free_length - used[i][1]], new_free_offset)

last_file = sorted(used, key=lambda x: x[2])[-1]

part2 = [0] * (last_file[1] + last_file[2])
for file in used:
    for j in range(file[2], file[2] + file[1]):
        part2[j] = file[0]

print(f"Solution 2: {checksum(part2)}")
