import itertools
import functools
import re

with open("input.txt", "r") as f:
    paragraphs = f.read().split("\n\n")
    data = [x.rstrip() for x in paragraphs[1].split("\n")]
    rules_data = {}
    for line in paragraphs[0].replace('"', "").split("\n"):
        fields = line.rstrip().split(" ")
        key = fields[0].replace(":", "")
        rules_data[key] = fields[1::]

@functools.cache
def resolve_rule(x):
    def recurse(l):
        return list(map(lambda y: resolve_rule(y), l))
    def process(l):
        return list(map("".join, itertools.product(*l)))

    if rules_data[x] in [["a"], ["b"]]:
        return rules_data[x]
    if "|" in rules_data[x]:
        idx = rules_data[x].index("|")
        left = recurse(rules_data[x][0:idx])
        right = recurse(rules_data[x][idx + 1::])
        return process(left) + process(right)
    else:
        return process(recurse(rules_data[x]))

valid = {x: 1 for x in resolve_rule("0")}
matches = [x for x in data if x in valid]
print(f"Answer 1: {len(matches)}")

def make_regex(x, loop):
    regex = ""
    for r in rules_data[x]:
        if r in "ab|":
            regex += r
        else:
            if x == r: loop += 1
            if loop != max_depth:
                regex += make_regex(r, loop)
    return f"(?:{regex})"

max_depth = max(map(len, data))
regex = re.compile(f"^{make_regex('0', 0)}$")
matches = [x for x in data if re.match(regex, x)]
print(f"Answer 1: {len(matches)}")

rules_data["8"] = ["42", "|", "42", "8"]
rules_data["11"] = ["42", "31", "|", "42", "11", "31"]
regex = re.compile(f"^{make_regex('0', 0)}$")
matches = [x for x in data if re.match(regex, x)]
print(f"Answer 2: {len(matches)}")