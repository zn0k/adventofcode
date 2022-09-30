import math

with open("input.txt", "r") as f:
    modules = [int(x) for x in f.readlines()]

def calc(x):
    return math.floor(x / 3) - 2

answer = sum(map(calc, modules))
print(f"Answer 1: {answer}")

def calc_recursive(x):
    total = 0
    fuel = calc(x)
    total += fuel
    while fuel > 0:
        fuel = calc(fuel)
        if fuel > 0: total += fuel
    return total

answer = sum(map(calc_recursive, modules))
print(f"Answer 2: {answer}")