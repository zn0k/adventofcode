import pulp 

def EvaluateBlueprint(bp, minutes):
    _, c_ore, c_clay, c_obs, c_geode = bp
    # declare a problem where we want to maximize a resource
    problem = pulp.LpProblem("aoc2022-19", pulp.LpMaximize)
    # time series to iterate over, add a minute to keep data for next step even on last minute
    ts = list(range(minutes + 1)) 

    # declare variables for the resources
    ore = pulp.LpVariable.dicts("ore", ts, lowBound=0, cat=pulp.LpInteger)
    clay = pulp.LpVariable.dicts("clay", ts, lowBound=0, cat=pulp.LpInteger)
    obs = pulp.LpVariable.dicts("obs", ts, lowBound=0, cat=pulp.LpInteger)
    geode = pulp.LpVariable.dicts("geode", ts, lowBound=0, cat=pulp.LpInteger)
    # and robots, with one ore robot from the start
    r_ore = pulp.LpVariable.dicts("r_ore", ts, lowBound=0, cat=pulp.LpInteger)
    r_clay = pulp.LpVariable.dicts("r_clay", ts, lowBound=0, cat=pulp.LpInteger)
    r_obs = pulp.LpVariable.dicts("r_obs", ts, lowBound=0, cat=pulp.LpInteger)
    r_geode = pulp.LpVariable.dicts("r_geode", ts, lowBound=0, cat=pulp.LpInteger)
    # intialize resources to 0
    ore[0], clay[0], obs[0], geode[0] = 0, 0, 0, 0
    # same for robots, except we start with an ore bot
    r_ore[0], r_clay[0], r_obs[0], r_geode[0] = 1, 0, 0, 0

    # maximize for geodes
    problem += pulp.lpSum(geode)

    for i in range(minutes):
        # changes to resources
        # first, ore. that's current ore plus mined ore
        # minus the ore cost of all new robots
        problem += ore[i + 1] == (ore[i] + r_ore[i]) \
            - ((r_ore[i+1] - r_ore[i]) * c_ore) \
            - ((r_clay[i+1] - r_clay[i]) * c_clay) \
            - ((r_obs[i+1] - r_obs[i]) * c_obs[0]) \
            - ((r_geode[i+1] - r_geode[i]) * c_geode[0])
        # next, clay, in the same fashion
        problem += clay[i+1] == (clay[i] + r_clay[i]) \
            - ((r_obs[i+1] - r_obs[i]) * c_obs[1])
        # next, obsidian
        problem += obs[i+1] == (obs[i] + r_obs[i]) \
            - ((r_geode[i+1] - r_geode[i]) * c_geode[1])
        # and geodes
        problem += geode[i+1] == (geode[i] + r_geode[i])

        # constraints on construction of new robots
        # first, ore
        problem += ore[i] >= ((r_ore[i+1] - r_ore[i]) * c_ore) \
            + ((r_clay[i+1] - r_clay[i]) * c_clay) \
            + ((r_obs[i+1] - r_obs[i]) * c_obs[0]) \
            + ((r_geode[i+1] - r_geode[i]) * c_geode[0])
        # next, clay
        problem += clay[i] >= ((r_obs[i+1] - r_obs[i]) * c_obs[1])
        # and obisidian
        problem += obs[i] >= ((r_geode[i+1] - r_geode[i]) * c_geode[1])

        # constrain each round to only one new robot
        problem += (r_ore[i] + r_clay[i] + r_obs[i] + r_geode[i] + 1) >= \
            (r_ore[i+1] + r_clay[i+1] + r_obs[i+1] + r_geode[i+1])
        problem += r_ore[i+1] >= r_ore[i]
        problem += r_clay[i+1] >= r_clay[i]
        problem += r_obs[i+1] >= r_obs[i]
        problem += r_geode[i+1] >= r_geode[i]

    solver = pulp.getSolver("PULP_CBC_CMD", msg=0)
    problem.solve(solver)
    return geode[minutes].value() 

def parse(line):
    f = line.split()
    i = f[1].split(":")
    return [int(i[0]), int(f[6]), int(f[12]), (int(f[18]), int(f[21])), (int(f[27]), int(f[30]))]

with open("input.txt", "r") as f:
    blueprints = [parse(x) for x in f.readlines()]

total = 0
for bp in blueprints:
    total += EvaluateBlueprint(bp, 24) * bp[0]
print(f"Solution 1: {total}")

part2 = 1
for bp in blueprints[0:3]:
    part2 *= EvaluateBlueprint(bp, 32)
print(f"Solution 2: {part2}")