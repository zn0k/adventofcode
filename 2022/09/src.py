#!/usr/bin/env python3

directions = {"U": (0, 1), "D": (0, -1), "L":  (-1, 0), "R": (1, 0)}

with open("input.txt", "r") as f:
    moves = [tuple(line.split()) for line in f.readlines()]

def add(a, b): return (a[0] + b[0], a[1] + b[1])
def touching(a, b): return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1
def left(a, b): return a[0] < b[0]
def right(a, b): return a[0] > b[0]
def up(a, b): return a[1] > b[1]
def down(a, b): return a[1] < b[1]

def move_rope(moves, num_knots):
    ks = [(0, 0) for _ in range(num_knots)]
    visited = {(0, 0): True}
    for move in moves:
        direction, times = move
        for _ in range(int(times)):
            ks[0] = add(ks[0], directions[direction])
            for i in range(num_knots - 1):
                if not touching(ks[i], ks[i+1]):
                    if left(ks[i], ks[i+1]): ks[i+1] = add(ks[i+1], directions["L"])
                    if right(ks[i], ks[i+1]): ks[i+1] = add(ks[i+1], directions["R"])
                    if up(ks[i], ks[i+1]): ks[i+1] = add(ks[i+1], directions["U"])
                    if down(ks[i], ks[i+1]): ks[i+1] = add(ks[i+1], directions["D"])
            visited[ks[-1]] = True
    return len(visited)

print("Solution 1:", move_rope(moves, 2))
print("Solution 2:", move_rope(moves, 10))