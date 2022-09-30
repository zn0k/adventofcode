with open("input.txt", "r") as f:
    sues = {}
    for line in [x.rstrip() for x in f.readlines()]:
        num = int(line.split(" ")[1].replace(":", ""))
        sues[num] = {}
        rest = "".join(line.split(" ")[2:])
        properties = rest.split(",")
        for p in properties:
            left, right = p.split(":")
            sues[num][left] = int(right)

facts = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

for sue_num in sues:
    found = True
    for fact in facts:
        if fact in sues[sue_num]:
            if facts[fact] != sues[sue_num][fact]:
                found = False
    if found:
        print(f"Solution 1: {sue_num}")
        break

for sue_num in sues:
    found = True
    for fact in facts:
        if fact in sues[sue_num]:
            if fact == "cats" or fact == "trees":
                if facts[fact] >= sues[sue_num][fact]:
                    found = False
            elif fact == "pomeranians" or fact == "goldfish":
                if facts[fact] <= sues[sue_num][fact]:
                    found = False
            else:
                if facts[fact] != sues[sue_num][fact]:
                    found = False
    if found:
        print(f"Solution 2: {sue_num}")
        break        