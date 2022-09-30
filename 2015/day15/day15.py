from functools import reduce

with open("input.txt", "r") as f:
    ingredients = []
    for line in [x.rstrip() for x in f.readlines()]:
        tokens = line.replace(":", "").replace(",", "").split()
        name, capacity, durability = tokens[0], int(tokens[2]), int(tokens[4])
        flavor, texture, calories = int(tokens[6]), int(tokens[8]), int(tokens[10])
        ingredients.append((name, capacity, durability, flavor, texture, calories))

def sums(length, total_sum):
    if length == 1:
        yield (total_sum,)
    else:
        for value in range(total_sum + 1):
            for permutation in sums(length - 1, total_sum - value):
                yield (value,) + permutation

ratios = list(sums(len(ingredients), 100))

def score_ratio(ratio, calorie_goal=None):
    if calorie_goal:
        calories = sum(map(lambda x: ratio[x] * ingredients[x][5], range(0, len(ratio))))
        if calories != calorie_goal:
            return 0
    capacity = sum(map(lambda x: ratio[x] * ingredients[x][1], range(0, len(ratio))))
    durability = sum(map(lambda x: ratio[x] * ingredients[x][2], range(0, len(ratio))))
    flavor = sum(map(lambda x: ratio[x] * ingredients[x][3], range(0, len(ratio))))
    texture = sum(map(lambda x: ratio[x] * ingredients[x][4], range(0, len(ratio))))
    scores = map(lambda x: 0 if x < 0 else x, (capacity, durability, flavor, texture))
    return reduce(lambda x, y: x * y, scores, 1)

scores = map(score_ratio, ratios)
highest = max(scores)
print(f"Solution 1: {highest}")

scores = map(lambda x: score_ratio(x, 500), ratios)
highest = max(scores)
print(f"Solution 2: {highest}")