from collections import Counter

def pair_up(polymer):
    return zip(polymer, polymer[1:])

def substitute(pair):
    a, b = pair
    return a + substitutions[a + b]

with open("input.txt", "r") as f:
    lines = f.readlines()
    polymer = lines[0].rstrip()
    substitutions = {}
    for line in lines[2:]:
        k, v = line.rstrip().split(" -> ")
        substitutions[k] = v

for x in range(10):
    polymer = "".join(map(substitute, pair_up(polymer))) + polymer[-1]

counts = list(map(lambda x: polymer.count(x), set(polymer)))
print(f"Solution 1: {max(counts) - min(counts)}")

with open("input.txt", "r") as f:
    lines = f.readlines()
    polymer = lines[0].rstrip()
    counter = Counter(polymer)
    pairs = Counter(map(lambda x: x[0] + x[1], pair_up(polymer)))
    substitutions = {}
    for line in lines[2:]:
        k, v = line.rstrip().split(" -> ")
        substitutions[k] = v

# way too slow
#for x in range(40):
#    print(f"on step {x}")
#    for i in range(1, 2 * len(polymer) - 1, 2):
#        polymer.insert(i, substitutions[polymer[i - 1] + polymer[i]])
#
#counts = list(map(lambda x: polymer.count(x), set(polymer)))
#print(f"Solution 2: {max(counts) - min(counts)}")

for x in range(40):
    # go through each pair
    for (first, second), count in pairs.copy().items():
        # get the letter to be inserted
        new = substitutions[first + second]
        # subtract the counts for the previous pair
        pairs[first + second] -= count
        # add the counts for the new pairs
        pairs[first + new] += count
        pairs[new + second] += count
        # count the new character
        counter[new] += count

print(f"Solution 2: {max(counter.values()) - min(counter.values())}") 