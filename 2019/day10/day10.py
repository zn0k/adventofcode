from math import gcd, pi, atan2
from functools import reduce, partial

with open("input.txt", "r") as f:
    lines = f.readlines()
    max_x = len(lines[0].rstrip()) - 1
    max_y = len(lines) - 1
    asteroids = set([(x, y) for y, line in enumerate(lines) for x, c in enumerate(line.rstrip()) if c != "."])

def calc_blocked(a, b):
    blocked = set()
    dx, dy = b[0] - a[0], b[1] - a[1]
    dx, dy, i = int(dx / gcd(dx, dy)), int(dy / gcd(dx, dy)), 0
    valid_x = [a[0]] if dx == 0 else range(0, b[0]) if dx < 0 else range(b[0], max_x + 1)
    valid_y = [a[1]] if dy == 0 else range(0, b[1]) if dy < 0 else range(b[1], max_y + 1)
    while True:
        i += 1
        new_x, new_y = a[0] + i * dx, a[1] + i * dy
        if not (0 <= new_x <= max_x and 0 <= new_y <= max_y): break
        if (new_x, new_y) in [a, b]: continue
        if new_x in valid_x and new_y in valid_y: blocked.add((new_x, new_y))
    return blocked

def calc_seen(a):
    others = asteroids.copy()
    others.remove(a)
    blocked = set()
    for other in others:
        blocked = blocked.union(calc_blocked(a, other))
    return others - blocked.intersection(others)

num_seen = map(lambda x: (x, len(calc_seen(x))), asteroids)
best = reduce(lambda x, y: x if x[1] > y[1] else y, num_seen)
print(f"Answer 1: {best}")

def calc_angle(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return atan2(dy, dx) + (pi / 2)
    
seen = calc_seen(best[0])
rank = partial(calc_angle, best[0])
ranked = map(lambda x: (x, rank(x)), seen)
ordered = sorted(ranked, key=lambda x: x[1])
fourth = list(filter(lambda x: x[1] < 0.0, ordered))
not_fourth = list(filter(lambda x: x[1] >= 0.0, ordered))
ordered = not_fourth + fourth

no200 = ordered[199]
print(f"Answer 2: {no200[0][0] * 100 + no200[0][1]}")