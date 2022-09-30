def split_coordinates(c):
    x, y = c.split(",")
    return (int(x), int(y))

with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f.readlines()]
    instructions = []
    for line in lines:
        words = line.split()
        if words[0] == "turn":
            instructions.append((words[1], split_coordinates(words[2]), split_coordinates(words[4])))
        else:
            instructions.append((words[0], split_coordinates(words[1]), split_coordinates(words[3])))

lights = []
for x in range(0, 1000):
    row = []
    for y in range(0, 1000):
        row.append(0)
    lights.append(row)

def _set_lights(start, end, value, toggle):
    x1, y1 = start
    x2, y2 = end
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            if toggle:
                current = lights[x][y]
                new = 0 if current else 1
                lights[x][y] = new
            else:
                lights[x][y] = value

def turn_on(start, end):
    _set_lights(start, end, 1, False)

def turn_off(start, end):
    _set_lights(start, end, 0, False)

def toggle(start, end):
    _set_lights(start, end, 0, True)

for i in instructions:
    action, start, end = i
    if action == "on":
        turn_on(start, end)
    if action == "off":
        turn_off(start, end)
    if action == "toggle":
        toggle(start, end)

total = 0
for row in lights:
    total += row.count(1)

print(f"Solution 1: {total}")

def _set_lights2(start, end, value):
    x1, y1 = start
    x2, y2 = end
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            lights[x][y] += value
            if lights[x][y] < 0:
                lights[x][y] = 0

lights = []
for x in range(0, 1000):
    row = []
    for y in range(0, 1000):
        row.append(0)
    lights.append(row)

for i in instructions:
    action, start, end = i
    if action == "on":
        _set_lights2(start, end, 1)
    if action == "off":
        _set_lights2(start, end, -1)
    if action == "toggle":
        _set_lights2(start, end, 2)

total = 0
for row in lights:
    total += sum(row)

print(f"Solution 2: {total}")