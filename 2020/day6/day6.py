import collections

with open("input.txt", "r") as f:
    
    blocks = f.read().split("\n\n")
    groups = []
    for block in blocks:
        groups.append(block.split("\n"))

def flatten(xs):
    # take a list of lists and flatten it into one list
    return [x for ys in xs for x in ys]

def count_any(xs):
    # flatten the list of members in a group
    # then transform it into a set, which only have unique values
    # then count the number of values
    return len(set(flatten(xs)))

anyone_count = sum(list(map(count_any, groups)))
print(f"Sum of counts for anyone is {anyone_count}")

def count_common(xs):
    # flatten the list of members in a group
    # then transform it into a counted collection
    # then pull out those with a count equal to the group members
    # then count how many there ares
    num_members = len(xs)
    counted = collections.Counter(flatten(xs))
    return len([x for x, y in counted.items() if y == num_members])

common_count = sum(list(map(count_common, groups)))
print(f"Sum of counts for commons is {common_count}")