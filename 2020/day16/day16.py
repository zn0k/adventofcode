with open("input.txt", "r") as f:
        segments = f.read().split("\n\n")
        rules = {}
        for line in segments[0].split("\n"):
            key, value = line.split(": ")
            conditions = [tuple([int(y) for y in x.split("-")]) for x in value.split(" or ")]
            rules[key] = conditions
        my_ticket = [int(x) for x in segments[1].split("\n")[1].split(",")]
        nearby_tickets = [[int(y) for y in x.split(",")] for x in segments[2].split("\n")[1::]]

def validate(val, conditions):
    for c in conditions:
        if val >= c[0] and val <= c[1]:
            return True
    return False

invalid = 0
valid_tickets = []
for t in nearby_tickets:
    valid_ticket = True
    for val in t:
        valid = False
        for rule in rules:
            if validate(val, rules[rule]):
                valid = True
        if not valid:
            invalid += val
            valid_ticket = False
    if valid_ticket:
        valid_tickets.append(t)
print(f"answer 1: {invalid}")

possible_rule_mappings = {}
for rule in rules:
    possible = []
    for i in range(0, len(valid_tickets[0])):
        values = [t[i] for t in valid_tickets]
        valid = [validate(x, rules[rule]) for x in values].count(True)
        if valid == len(valid_tickets):
            possible.append(i)
    possible_rule_mappings[rule] = possible
rule_mappings = {}
used = []
for rule in sorted(rules.keys(), key=lambda x: len(possible_rule_mappings[x])):
    remaining = list(filter(lambda x: x not in used, possible_rule_mappings[rule]))
    if len(remaining) == 1:
        used.append(remaining[0])
        rule_mappings[rule] = remaining[0]
total = 1
for rule in [rule for rule in rules if rule.startswith("departure")]:
    total *= my_ticket[rule_mappings[rule]]
print(f"answer 2: {total}")