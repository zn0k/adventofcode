with open("input.txt", "r") as f:
    steps = f.read()

floor = 0 + steps.count("(") - steps.count(")")
print(f"Solution 1: {floor}")

floor = 0
position = 0
for x in steps:
    position += 1
    floor += (1 if x == "(" else -1)
    if floor < 0:
        break
print(f"Solution 2: {position}")