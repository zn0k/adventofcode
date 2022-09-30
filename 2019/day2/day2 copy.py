with open("input.txt", "r") as f:
    line = f.readlines()[0]
    initial = [int(op) for op in line.rstrip().split(",")]

def run(x, y):
    cur = 0
    program[1], program[2] = x, y
    while True:
        op = program[cur]
        if op == 99:
            break
        x, y = program[program[cur + 1]], program[program[cur + 2]]
        dest = program[cur + 3]
        if op == 1:
            program[dest] = x + y
        elif op == 2:
            program[dest] = x * y
        else:
            raise Exception(f"Unknown op code {op} at {cur}")
        cur += 4
    return program[0]

program = initial.copy()
print(f"Answer 1: {run(12, 2)}")

for i in range(0, 100):
    for j in range(0, 100):
        program = initial.copy()
        result = run(i, j)
        if result == 19690720:
            print(f"Answer 2: {i * 100 + j}")