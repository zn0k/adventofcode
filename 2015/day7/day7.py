def to_num(a):
    if a.isnumeric():
        return int(a)
    else:
        return a

with open("input.txt", "r") as f:
    lines = [x.rstrip() for x in f.readlines()]
    sources = {}
    for line in lines:
        left, right = line.split(" -> ")
        left_words = left.split(" ")
        found = False
        for instruction in ["AND", "OR", "NOT", "LSHIFT", "RSHIFT"]:
            if instruction in left_words:
                if instruction == "NOT":
                    sources[right] = (to_num(left_words[0]), to_num(left_words[1]))
                else:
                    sources[right] = (left_words[1], to_num(left_words[0]), to_num(left_words[2]))
                found = True
                break
        if not found:
            sources[right] = ("NOOP", to_num(left_words[0]))

cache = {}

def resolve(what):
    if what in cache:
        return cache[what]
    else:
        if str(what).isnumeric():
            return what
        instruction = sources[what]
        action = instruction[0]
        if len(instruction) == 3:
            arg1, arg2 = resolve(instruction[1]), resolve(instruction[2])
        else:
            arg1 = resolve(instruction[1])
        if action == "AND":
            result = arg1 & arg2
        if action == "OR":
            result = arg1 | arg2
        if action == "LSHIFT":
            result = arg1 << arg2
        if action == "RSHIFT":
            result = arg1 >> arg2
        if action == "NOT":
            result = ~ arg1
        if action == "NOOP":
            result = arg1
        cache[what] = result
        return result

solution1 = resolve("a")
print(f"Solution 1: {solution1}")

cache = {}
sources["b"] = ("NOOP", solution1)
solution2 = resolve("a")
print(f"Solution 2: {solution2}")