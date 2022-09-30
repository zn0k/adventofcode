from functools import reduce, partial
from operator import or_, mul

def tests(conditions, val):
    result = reduce(or_, [c[0] <= val <= c[1] for c in conditions], False)
    return 0 if result else val

with open("input.txt", "r") as f:
    segments = f.read().split("\n\n")
    rules = {}
    for line in segments[0].split("\n"):
        key, value = line.split(": ")
        conditions = [tuple([int(y) for y in x.split("-")]) for x in value.split(" or ")]
        rules[key] = partial(tests, conditions)
    my_ticket = [int(x) for x in segments[1].split("\n")[1].split(",")]
    nearby_tickets = [[int(y) for y in x.split(",")] for x in segments[2].split("\n")[1::]]

def validate_ticket(ticket):
    invalid = sum([min([f(val) for f in rules.values()]) for val in ticket])
    return (invalid, ticket)

validated = [validate_ticket(t) for t in nearby_tickets]
invalid_sum = sum([t[0] for t in validated])
print(f"answer 1: {invalid_sum}")

def validate_column(rule, column):
    return len([v for v in column if rule(v) == 0]) == len(column)

valid_tickets = [t[1] for t in validated if t[0] == 0]
columns = [[t[i] for t in valid_tickets] for i, _ in enumerate(valid_tickets[0])]
possible = {rule: [i for i, col in enumerate(columns) if validate_column(rules[rule], col)] for rule in rules}

def match(mapped, rule):
    remaining = list(filter(lambda x: x not in used, possible[rule]))
    used.append(remaining[0])
    mapped[rule] = remaining[0]
    return mapped

used = []
mapped = reduce(match, sorted(rules.keys(), key=lambda x: len(possible[x])), {})
total = reduce(mul, [my_ticket[mapped[r]] for r in [r for r in rules if r.startswith("departure")]])
print(f"answer 2: {total}")