#!/usr/bin/env python3

with open("input.txt", "r") as f:
    def divide(items):
        half = len(items) // 2
        return (items[0:half], items[half:].strip())
    items = [divide(i) for i in f.readlines()]

def toNum(char):
    num = ord(char)
    if 65 <= num <= 90:
        return num - 64 + 26
    elif 97 <= num <= 122:
        return num - 96
    else:
        return 0

total = 0
for item in items:
    common = set(item[0]) & set(item[1])
    for char in common:
        total += toNum(char)

print(f"Solution 1: {total}")

total = 0
for i in range(0, len(items), 3):
    common = set(items[i][0]) | set(items[i][1])
    for j in [1, 2]:
        common &= (set(items[i + j][0]) | set(items[i + j][1]))
    for char in common:
        total += toNum(char)

print(f"Solution 2: {total}")
