with open("input.txt", "r") as f:
    steps = [s.replace("\n", "") for s in f.readlines()]

def gen_answer1():
    direction = "E"
    compass = ["N", "E", "S", "W"]
    while True:
        step = yield
        action, dist = step[0], int(step[1::])
        if action == "F": action = direction
        if action in "LR": 
            offset = int((-1 if action == "L" else 1) * (dist / 90))
            direction = compass[(compass.index(direction) + offset) % 4]
            yield (0, 0)
        else:
            if action in "SW": dist *= -1
            yield (dist, 0) if action in "NS" else (0, dist)

def gen_answer2():
    wp = [1, 10]
    while True:
        step = yield
        action, dist = step[0], int(step[1::])
        if action in "NESW":
            if action in "SW": dist *= -1
            if action in "NS": wp[0] += dist
            if action in "EW": wp[1] += dist
            yield (0, 0)
        elif action in "LR":
            for i in range(0, int(dist / 90)):
                if action == "L":
                    wp = [wp[1], -1 * wp[0]]
                else:
                    wp = [-1 * wp[1], wp[0]]
            yield (0, 0)
        else:
            yield (wp[0] * dist, wp[1] * dist)

def gen_loc(f):
    loc = (0, 0)
    s = f()
    next(s)
    while True:
        step = yield
        n = s.send(step)
        next(s)
        loc = (loc[0] + n[0], loc[1] + n[1])
        yield loc

def new_loc(g, step):
    next(g)
    return g.send(step)

def md(loc):
    return abs(loc[0]) + abs(loc[1])

for f in [gen_answer1, gen_answer2]:
    g = gen_loc(f)
    locs = [new_loc(g, step) for step in steps]
    print(md(locs[-1]))