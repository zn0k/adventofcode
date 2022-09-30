with open("input.txt", "r") as f:
    steps = [x for x in f.read()]

move = {
    "^": lambda x: (x[0], x[1] + 1),
    "v": lambda x: (x[0], x[1] - 1), 
    ">": lambda x: (x[0] + 1, x[1]),
    "<": lambda x: (x[0] - 1, x[1])
}

s = (0, 0)
houses = set()
houses.add(s)
for step in steps:
    s = move[step](s)
    houses.add(s)

print(f"Solution 1: {len(houses)}")

s = (0, 0)
r = (0, 0)
houses = set()
houses.add(s)
for index, step in enumerate(steps):
    if index % 2 == 0:
        s = move[step](s)
        houses.add(s)
    else:
        r = move[step](r)
        houses.add(r)

print(f"Solution 2: {len(houses)}")