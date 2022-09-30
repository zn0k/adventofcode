from functools import reduce

with open("input.txt", "r") as f:
    ingredients = []
    allergens = {}
    for line in f.readlines():
        ing, aller = line.split(" (contains ")
        ing = ing.split(" ")
        aller = aller.replace(")", "").replace("\n", "").split(", ")
        ingredients.extend(ing)
        for a in aller:
            if a in allergens:
                allergens[a] = allergens[a].intersection(set(ing))
            else:
                allergens[a] = set(ing)

not_it = set(ingredients) - reduce(lambda x, y: x.union(y), allergens.values())
answer1 = sum([ingredients.count(x) for x in not_it])
print(f"Answer 1: {answer1}")

bad = set(ingredients) - not_it
mapped = {}
while(len(bad)):
    i = ""
    for a in allergens:
        if len(allergens[a]) == 1:
            i = list(allergens[a])[0]
            break
    mapped[i] = a
    bad.remove(i)
    for a in allergens:
        if i in allergens[a]:
            allergens[a].remove(i)
order = ",".join(sorted(mapped.keys(), key=lambda x: mapped[x]))
print(f"Answer 2: {order}")
