#!/usr/bin/env python3

import sys
from itertools import combinations
from z3 import Reals, Solver, sat

with open(sys.argv[1], "r") as f:
  data = [l.strip().split("@ ") for l in f.readlines()]
  process = lambda x: list(map(int, x.split(", ")))
  data = [(process(x[0]), process(x[1])) for x in data]

if sys.argv[1] == "test.txt":
  min_x = min_y = 7
  max_x = max_y = 27
else:
  min_x = min_y = 200_000_000_000_000
  max_x = max_y = 400_000_000_000_000

counter = 0
for a, b in combinations(data, 2):
  (ax, ay, _), (avx, avy, _) = a
  (bx, by, _), (bvx, bvy, _) = b
  ma = avy / avx
  mb = bvy / bvx
  if ma == mb: continue
  ca = ay - (ma * ax)
  cb = by - (mb * bx)
  ix = (cb - ca) / (ma - mb)
  iy = ma * ix + ca
  if (ix < ax and avx > 0): continue
  if (ix > ax and avx < 0): continue
  if (ix < bx and bvx > 0): continue
  if (ix > bx and bvx < 0): continue
  if min_x <= ix <= max_x and min_y <= iy <= max_x: counter += 1

print(f"Solution 1: {counter}")

(ax, ay, az), (avx, avy, avz) = data[0]
(bx, by, bz), (bvx, bvy, bvz) = data[1]
(cx, cy, cz), (cvx, cvy, cvz) = data[2]
x, y, z = Reals("x y z")
vx, vy, vz = Reals("vx vy vz")
t1, t2, t3 = Reals("t1 t2 t3")
s = Solver()

equations = [
  x + t1 * vx == ax + t1 * avx,
  x + t2 * vx == bx + t2 * bvx,
  x + t3 * vx == cx + t3 * cvx,
  y + t1 * vy == ay + t1 * avy,
  y + t2 * vy == by + t2 * bvy,
  y + t3 * vy == cy + t3 * cvy,
  z + t1 * vz == az + t1 * avz,
  z + t2 * vz == bz + t2 * bvz,
  z + t3 * vz == cz + t3 * cvz,
]

s.add(*equations)
if s.check() == sat:
  model = s.model()
  solution2 = sum([model[var].as_long() for var in [x, y, z]])
  print(f"Solution 2: {solution2}")
