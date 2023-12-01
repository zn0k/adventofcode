#!/usr/bin/env python3

with open("input.txt", "r") as f:
    items = [l.strip() for l in f.readlines()]

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
    half = len(item) // 2
    common = set(item[0:half]) & set(item[half:])
    for char in common:
        total += toNum(char)

print(f"Solution 1: {total}")

total = 0
for group in zip(*[iter(items)] * 3):
    common = set(group[0]) & set(group[1]) & set(group[2])
    for char in common:
        total += toNum(char)

print(f"Solution 2: {total}")
