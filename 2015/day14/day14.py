with open("input.txt", "r") as f:
    racers = []
    lines = [x.rstrip() for x in f.readlines()]
    for line in lines:
        tokens = line.split()
        racers.append((int(tokens[3]), int(tokens[6]), int(tokens[13]), tokens[0]))

race_length = 2503

def calculate(duration, x):
    speed, sprint, cooldown, name = x
    sprints = duration // (sprint + cooldown)
    distance = sprints * (speed * sprint)
    balance = duration - ((sprints) * (sprint + cooldown))
    if balance > 0:
        additional_seconds = sprint if balance > sprint else balance
        distance += additional_seconds * speed
    return (distance, name)

def max_func(x):
    return x[0]

highest = max([calculate(race_length, r) for r in racers], key=max_func)
print(f"Solution 1: {highest[0]}")

points = {x[3]: 0 for x in racers}

for x in range(1, race_length + 1):
    result = [calculate(x, r) for r in racers]
    highest = max(result, key=max_func)
    points[highest[1]] += 1

highest = max(points.values())
print(f"Solution 2: {highest}")