from itertools import permutations

with open("input.txt", "r") as f:
    relations = {}
    lines = f.readlines()
    for line in lines:
        tokens = line.split()
        person1, direction, score, person2 = tokens[0], tokens[2], int(tokens[3]), tokens[10][0:-1]
        if direction == "lose":
            score *= -1
        if person1 not in relations:
            relations[person1] = {}
        relations[person1][person2] = score

def score_permutations():
    scores = []
    for permutation in permutations(relations.keys()):
        score = 0 
        for index, person in enumerate(permutation):
            if index == 0:
                score += relations[person][permutation[-1]] + relations[person][permutation[index + 1]]
            elif index == len(permutation) - 1:
                score += relations[person][permutation[index - 1]] + relations[person][permutation[0]]
            else:
                score += relations[person][permutation[index - 1]] + relations[person][permutation[index + 1]]
        scores.append(score)
    return scores

print(f"Solution 1: {max(score_permutations())}")

relations["Me"] = {}
for person in relations.keys():
    if person == "Me":
        continue
    relations["Me"][person] = 0
    relations[person]["Me"] = 0

print(f"Solution 2: {max(score_permutations())}")