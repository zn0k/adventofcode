import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
 
from IntCode import IntCode

with open("input.txt", "r") as f:
    line = f.readlines()[0]
    initial = [int(op) for op in line.rstrip().split(",")]

p = initial.copy()
p[1], p[2] = (12, 2)
ic = IntCode(p)
p = ic.run()
print(f"Answer 1: {p[0]}")

for i in range(0, 100):
    for j in range(0, 100):
        p = initial.copy()
        p[1], p[2] = (i, j)
        ic = IntCode(p)
        p = ic.run()
        if p[0] == 19690720:
            print(f"Answer 2: {i * 100 + j}")