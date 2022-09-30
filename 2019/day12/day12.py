import re
from itertools import combinations
from operator import add, mul
from functools import reduce

def initialize():
    with open("input_test.txt", "r") as f:
        lines = f.readlines()
        pattern = re.compile("[xyz]=(-?\d+)")
        moons = []
        for line in lines:
            coordinates = [int(c) for c in pattern.findall(line)]
            moons.append((tuple(coordinates), (0, 0, 0)))
    return moons

def apply_gravity_aspect(t):
    a, b = t
    return 1 if a < b else -1 if a > b else 0

def apply_gravity(a, b):
    return tuple(map(apply_gravity_aspect, zip(a, b)))

def apply_gravities(a, bs):
    pos, vel = a
    for b in bs:
        vel = add_vectors(vel, apply_gravity(pos, b[0]))
    return (add_vectors(pos, vel), vel)

def add_vectors(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def simulate(moons, steps=1, record=False):
    for i in range(1, steps + 1):
        moons = list(map(lambda x: apply_gravities(x, moons), moons))
        if record:
            for moon in moons:
                if moon in past:
                    past[moon].append(i)
                else:
                    past[moon] = [i]
    return moons

def calculate_energy(t):
    return reduce(add, map(abs, t[0])) * reduce(add, map(abs, t[1]))

moons = simulate(initialize(), steps=1000)
energy = reduce(add, map(calculate_energy, moons))
print(f"Answer 1: {energy}")

def find_loop(moons):
    past = {moon: 1 for moon in moons}
    print(f"past is {past}")
    i = 1
    while True:
        moons = list(map(lambda x: apply_gravities(x, moons), moons))
        for moon in moons:
            if moon in past and past[moon] == 1:
                past[moon] = i
                print(f"past is {past}")
        if sum(past.values()) > 4:
            break
        i += 1
    return past

result = find_loop(initialize())
print(result)